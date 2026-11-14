# Round 5 editor notes

Oath & Action Edition 06, Phase 3, round 5. Editor (`oa-editor`), November 14, 2026, under `work/handoffs/phase-3/20261114_Phase-3-Round-5-Brief.md` (the editor's row and its "Editor" paragraph bind). Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/7633c399-b692-5041-be92-a87ecd098fbf/scratchpad/phase-3/round-5/editor/`. Written as I go; the container can restart.

The owners read the "Words for ..." sections directly. Each gives the words an owner needs before it draws, and later each row of the words pass gives the file, the field, the old words and the new, and why. The owner applies them; once an owner reports finished, I write straight into its word fields (D3-669) and log each change here. I never touch a key that picks a mark or an ink (V22).

## Status

- 01:52 UTC. **Group 18 and the two extras' words are in `14-chapter.json`.** The engineer's plan row for group 18 landed ("Three charts in full", 14.142 to 14.144) with the plan's `extras`; my generator now writes group 18 with its line and, under R5-2a, an `extras` list with each extra's printed label and caption: "Choose a chart" and "The four data palettes, step by step" (the plan's working "The data palettes, specified" gives way, as its note says), each with the caption under "Words for ...". Every check passes; a second run changes no file (hashes). Returning to the main session; I read the rulings, the research lead's facts and each item as it lands.
- 01:51 UTC. **First words posted for every owner** under the five "Words for ..." sections: the selection guide's label, caption and tier words; group 18's title and line and the three rules' working titles; chapter 11 group 2's title and line and the intro's sentence; the palette specification's label, caption and proof labels; chapter 15 groups 5 and 6's titles and lines. `phase3_ch14_rules_build.py` now reads group 18's line and lists only the 16 family questions in the opener, so the engineer's plan row cannot stop it; two runs wrote nothing new. Waiting on: the data lead's rulings (a) to (d), the engineer's R5-1 to R5-3, the research lead's "Facts for owners" (the trackers' step names and end words), and items as they land.
- 01:42 UTC. Started. Read `CLAUDE.md`, my role file, chapter 02's writing rules, the round 5 brief and my round 4 notes; the decision log from D3-1840 to DR-276. Working tree at `a813cf38`. Next: the facts behind each "Words for ..." section, then the sections themselves, within the half hour.

## Summary

- **Words for owners, first set (01:51 UTC).** Five sections below, each read again as rulings and drafts land.
- **Generator ready for group 18.** The opener takes only the plan's family groups, and `GROUP_LINES[18]` holds group 18's working line; on today's plan the generator writes nothing new.
- **Chapter 14's intro** waits until the selection guide and the three charts exist (task 2); a draft is under "Chapter 14's intro" below.

## Words for the selection guide maker

Written at 01:50 UTC, before the data lead's ruling (a) and the engineer's R5-2 contract; I read them again when they land and change a row here only if a ruling makes it untrue. Every tier count below is by script on the plan file: 56 core and 41 extended forms, each with a finished specimen (`spec_id`), and 22 reference and 8 avoid forms, each a sketch (`status: sketch`). The guide prints no tier word anywhere today except "a reference form" in reference entries' rule text and "Form to avoid" on avoid sketches, so the caption is where a reader first meets the four words, and it defines them (H02).

| Field | Words | Why |
|---|---|---|
| Label (now in `14-chapter.json`'s `extras`, R5-2a) | Choose a chart | Keep the brief's words. They are the action a reader came for, in three words, and they repeat the chapter's own instruction ("Start from the reader’s question to choose a chart") and Rule 14.1's "choose the form". A label that names the contents, "Every form, by the question it answers", is the fallback if the design director wants this extra labeled like chapter 11's and 05's ("The six steps", "The seven colors") |
| Caption (the same) | Every form in this chapter sits under the question it answers, and each name leads to its entry. Core forms, the ones we use most, come first, then extended forms for a story that needs them, and both kinds show a finished example. A reference form, drawn as a sketch, suits a narrower job, and a form to avoid misleads, so its entry shows the form to use in its place. | Says what the plate holds and how to read the word after each name. Facts by the plan file and the coverage plan's section 2: core and extended forms have finished specimens, reference and avoid forms have sketches, and each avoid entry names the form to use instead (DR-240). Three sentences of different shapes and lengths (W03, W13); "the ones we use most" and "for a story that needs them" take the coverage plan's tier meanings into plain words |
| Tier word printed after each name | Core; Extended; Reference; Avoid | One word each, capitalized as a tag; the caption has already said what each means. Rule 14.130's plan tier, "Extended, interactive", prints "Extended": the form's name, "Filterable lookup table", already says it is live, and the coverage plan counts it among the 41 extended forms |
| Each link's accessible name, if the accessibility lead's specification asks for the tier in words | Ranked bar, core form; Lollipop, extended form; Run chart, reference form; Radar chart, form to avoid | The forms' plan names, unchanged, then the tier in the words the guide already uses ("a reference form" in entry text, "Form to avoid" on the avoid plates). The accessibility lead sets whether the rule number joins the name; if it does, it follows the tier: "Radar chart, form to avoid, Rule 14.24" |
| Order under each question | Core, then Extended, Reference, Avoid; inside a tier, the plan's rule order | The brief's own order for ruling (a), which the data lead may change; the caption's second sentence says "Core forms ... come first" and changes with it |
| Question headings | The 16 questions exactly as the opener prints them, each with its family name, as in "Which is bigger, and how do they rank?" and "Comparison" | R5-2: the groups are the family questions as the chapter prints them. The opener writes them from the plan's group titles (first letter raised), so read them from there, never retype them |
| The plate's alt, if the manifest needs one | Every one of the 127 forms in this chapter, under the 16 reader questions that open its groups, each named with its tier and linked to its entry, beside a small drawing of the form. | The plate is live text, so its alt only says what the drawing set is; the names themselves are read from the links |

Two words to keep out of the plate: "tier" (a studio word; the caption never needs it) and "avoid form" (say "form to avoid", as the avoid plates do).

## Words for the complex examples maker

Written at 01:50 UTC, before the data lead's rulings (c) and (d). Each working title states the rule's lesson as an instruction, as chapter 14's rule titles do, in 15 words or fewer (counted by script). I read each again against the ruling and the drafted entry, and change it only where they make it untrue.

**Group 18.** The title goes in the plan file (the engineer's, R5-1) and the line in my generator, where it already sits as a working line (`GROUP_LINES[18]`, below).

| Field | Words | Why |
|---|---|---|
| Group 18 title (plan file `groups[17].title`) | Three charts in full | The brief's words, and they say what the group holds. Group 18 opens on no reader question, so it takes no "Family: question?" form, like group 1's "Every chart" |
| Group 18 line (`GROUP_LINES[18]` in `phase3_ch14_rules_build.py`) | Each chart here puts several of the chapter’s forms and rules together on one subject, with its table and its files. They show the monthly change in payroll jobs with the survey’s margin of error, two loops from our systems atlas that share a variable, and three reforms that act on one housing loop. | Two sentences on different frames (W13). The list holds the three charts the facts hold, each in its own shape (W12). "Payroll jobs" is S14's measure line; Loop R8 is "Housing scarcity strengthens owners’ incentive to restrict building", and R-06 is an election reform, so "reforms that act on one housing loop" is true where "three housing reforms" would not be |

**The three rules' working titles.**

| Rule | Working title | Words | Why |
|---|---|---|---|
| 14.142, S14 in full | Mark the survey’s margin on a monthly chart, and name the changes that pass it. | 15 | DR-239 makes the two drops past the margin S14's named mark, and "shrank in seven of the 57 months charted" stays true beside it, so the lesson is to let the margin decide which moves the chart names. If ruling (c) makes the average the lesson instead: "Set a noisy monthly count against its average, and mark the months still preliminary." (14) |
| 14.143, Loops B4 and R10 | Step through two loops one connection at a time, from the variable they share. | 14 | Variable C3, "Risk of losing office", is the one variable both loops hold. Rule 15.15 ("Follow a variable two loops share through each loop in turn.") and Rule 15.19 ("Step a reader through a loop one connection at a time, with a still sequence.") hold the two halves of this lesson, so the entry's rule should cite both by number and say what the chart in full adds: both loops in one stepper, the still sequence and the table |
| 14.144, R-06, R-30 and R-38 on Loop R8 | Compare reforms effect by effect, with every qualifier kept and no total score. | 13 | Two lessons the brief names: the atlas's ordinal effects compared one outcome at a time with no summed score (Rules 15.16 and 15.21), and the qualifiers ("+L local", "+S delayed", "+M renter-owner", "+S sector", "+S renters") kept whole. "Effect" in place of "measure", since in a civic guide a measure is also a bill or a ballot question. The rule text defines "qualifier" at first use (H02), as the words after an effect's code that say where or when it holds |

**For every word in these entries.** Read each atlas value by script, with "as of October 15, 2026" beside any status or route (R5-4). Name each ID with its type word the first time (H11): Loop B4, "Electoral consequences can improve public performance"; Loop R10, "Safe seats shift accountability to small primary electorates"; Variable C3, risk of losing office; Loop R8, "Housing scarcity strengthens owners’ incentive to restrict building"; Reform R-06, "Hold local elections alongside November races"; Reform R-30, "More homes allowed by right near jobs"; Reform R-38, "Limits on pricing software using rivals’ data" (the atlas stores a straight apostrophe; the guide prints it curled, as S37 does). S14's figures keep the approved wording of its entry and of chapter 02 (DR-239): "shrank in seven of the 57 months charted" and "Only the October 2025 and February 2026 drops pass the survey’s margin of error."

## Words for the tracker designer

Written at 01:50 UTC. Group 2's title and line come first, since they need no step names. The step names and end words wait for the research lead's "Facts for owners" (`work/handoffs/phase-3/20261114_Round-5-Research-Notes.md`, not posted at 01:50); I add them here when the facts land.

| Field | Now | Words | Why |
|---|---|---|---|
| Chapter 11 group 2 title | Records requests and agency rules | Records requests, agency rules, ballot measures and court cases | A reader who scans the contents for a court case finds the words. A list of four, the four trackers the group holds (W12); a heading may be a phrase |
| Chapter 11 group 2 line | A request for public records and a federal agency’s rule each move through six steps of their own, drawn with the tracker’s marks. | A records request, a federal agency’s rule, a ballot measure and a court case each move through six steps of their own, drawn with the bill tracker’s marks. Each ends in words that say how it came out, with the date. | The first sentence keeps the approved line's frame and adds the two trackers. The second holds for all four: Rule 11.8 ends a request "with the date", Rule 11.9 says how a rule ended "with the date", and R5-7 says a decided or certified item says so in words. "The bill tracker’s marks" is Rule 11.8's own phrase. Once the research lead posts the facts I read it again: if the ballot measure tracker is a state's and the court case tracker a federal one, the line says "a state ballot measure" and "a federal court case", as it already says "a federal agency’s rule" |
| Chapter 11 intro, second paragraph, first sentence | Trackers come first: they show how far a bill has come in six numbered steps, and the same marks then follow a records request or an agency rule. | Trackers come first: they show how far a bill has come in six numbered steps, and the same marks then follow a records request, an agency rule, a ballot measure and a court case. | The intro names what the chapter holds, and today it leaves out the two new trackers. Only the list changes |

**A question for you, on Rule 11.12 (old 11.10).** Its title, "Say a wait or a later step in words, and keep the count at six.", reads as a rule for every tracker in group 2, and after DR-274 it follows the court case tracker. Its words are a records request's and an agency rule's ("every request still counts to six", "an agency’s question to the requester", "the Federal Register for a rule"). If a ballot measure's or a court case's waits follow it too (a stay, a signature count under review), its first sentence should give one example from each; if they do not, its title should name the processes it covers, such as "Say a request’s or a rule’s wait in words, and keep the count at six." Your call with the data lead's ruling (f); I write the words once you say which.

### The trackers' step names and end words (02:16 UTC)

From the research lead's "Facts for owners", item 1 (read at 02:13), and the data lead's ruling (f). The step names stay as the research lead proposed them: each is a plain name for what happens, as Rule 11.1's are. The end words change where the law's word would stop a newcomer, as Rule 11.1's failure plate teaches ("The steps take the clerk’s names"), and where one verb family already runs through group 2: Rule 11.8 ends a request "Withdrawn by the requester" and an appeal "Upheld" or "Reversed and sent back", so the new trackers say the same thing the same way. Each end prints with its date, as group 2's line says. The source column is the research lead's; I add no fact.

**Rule 11.10, the ballot measure**

| Step | Name | In words |
|---|---|---|
| 1 | Filed | The sponsors file the measure’s full text with the attorney general |
| 2 | Title and summary | The attorney general clears the measure and writes the title and summary that petitions and ballots carry |
| 3 | Signatures | The sponsors gather signatures, and election officials count and check them |
| 4 | Legislature | The Legislature votes on the measure first, where the state’s initiative is indirect; under a slash where it goes straight to the ballot |
| 5 | On the ballot | The state’s election officer certifies the measure for the ballot |
| 6 | Vote | The voters decide, and the state certifies the result |

| Where it ends | Draft words now (`11-icons.json`) | Words | Why |
|---|---|---|---|
| Step 2 | Not certified by the attorney general | Not certified by the attorney general | The law's verb, "if he shall certify", and plain enough; the rule's text gives the reason a measure fails it (proper form, an excluded subject, the same measure at either of the last two state elections) |
| Steps 1 to 5 | Withdrawn by its proponents | Withdrawn by its sponsors | "Sponsors" is the everyday word for the people who file a measure; "proponents" is California's legal term, which the rule's text may give once. The same frame as "Withdrawn by the requester" |
| Step 3 | Did not qualify: too few valid signatures | Too few valid signatures to qualify | One phrase with no colon; it keeps the law's verb, "fails to qualify" |
| Step 4 | Enacted by the Legislature | Passed by the Legislature | Plain, and true in every state the research read (Ohio's own words are "passed by the general assembly"). The draft's "which makes it law with no vote of the people" goes further than the sources read: in Michigan and Ohio such a law is still "subject to referendum", and Massachusetts's path after enactment was not read. Say instead: "The voters do not vote on it." |
| Step 4, a legislative referral (not an end) | Referred by the Legislature | Sent to the voters by the Legislature | Says what the Legislature did, in words a newcomer uses |
| Step 5 | Removed from the ballot by a court | Removed from the ballot by a court | Stands |
| Step 6, after certification | Passed; Failed | Approved by voters; Rejected by voters | The law's own verbs ("approved by a majority", "approval or rejection"), and they name who decided (W02), so a reader never mixes the voters' vote with "Passed by the Legislature" at step 4. Each with the date of the vote and the date it was certified, then when it takes effect: "Approved by voters on November 3, certified on November 25. Takes effect December 25." *Illustrative* |
| Step 6, Massachusetts's 30 percent rule | (none) | Not approved by voters, then the sentence: "Most voters said yes, but Massachusetts also needs yes votes equal to 30 percent of all ballots cast." | "Rejected" would be untrue when most voters said yes; the sentence gives the rule from Amendment Article LXXXI |
| Step 6, before certification (current, not an end) | Step 6 of 6: Vote. The count stays unofficial until the state certifies it. | Step 6 of 6: Vote. The count is unofficial until the state certifies it, set for November 25. *Illustrative* | Ruling (f): the step stays current until certification. The date tells a reader when to look again, and "set for" claims only the schedule |

**Rule 11.11, the court case**

| Step | Name | In words |
|---|---|---|
| 1 | Filed | One side sues the other in a federal district court, the trial court |
| 2 | Trial court ruling | The trial court decides, with or without a trial, unless the case settles or is dismissed |
| 3 | Appeal | The side that lost asks a court of appeals to review the ruling |
| 4 | Appeals court ruling | Three judges of the court of appeals decide |
| 5 | Supreme Court petition | The side that lost asks the Supreme Court to hear the case, and the Court agrees or declines |
| 6 | Supreme Court ruling | The Supreme Court decides |

| Where it ends | Draft words now | Words | Why |
|---|---|---|---|
| Step 2, a judgment | (a sentence in the rule) | Decided for the plaintiff; Decided for the defendant; with ", without a trial" where the court granted summary judgment | The rule's text defines the two words once (H02): the plaintiff is the side that sued, the defendant the side it sued. The judgment's own word for who won |
| Step 2, by agreement | Settled | Settled by the parties | Names who acted (W02) |
| Step 2, by the plaintiff | Dismissed | Withdrawn by the plaintiff | A voluntary dismissal (Rule 41(a)) is the plaintiff's act, in group 2's "Withdrawn by" frame |
| Step 2, by the court | Dismissed | Dismissed by the court | Rule 41(b) and Rule 12(b)(6); the court acts, so it is named |
| Steps 4 and 6 | Affirmed; Reversed; Vacated; Modified | Upheld; Reversed; Vacated; Modified; each followed by the court, as in "Upheld by the appeals court" | "Upheld" is the plain word for "affirmed", the one Rule 11.8 already prints for an appeal; "Reversed" and "Modified" are plain as they stand. "Vacated" has no plain word that 28 U.S.C. 2106 does not already use for something else ("set aside" is its own verb there), so it stays, and the rule's text glosses it once: "Vacated, which cancels the ruling below". **For the data lead:** ruling (f) says the court's own word; this keeps every verb but one as the court enters it and maps "affirmed" to "Upheld" one for one, which the rule's text says. If the ruling holds "Affirmed" on the face, it prints "Affirmed" and the gloss moves to the text |
| Steps 4 and 6, a remand | and sent back | Reversed and sent back; Vacated and sent back; then the sentence "The trial court takes the case up again." | Rule 11.8's own phrase; the marks never move back (ruling (f)) |
| Step 4 | Appeal dismissed | Appeal withdrawn, where the parties agree or the side that appealed asks (FRAP 42(b)); Appeal dismissed by the court, otherwise | The research lead's source for this end is Rule 42(b), a party's act, which "withdrawn" says |
| Step 5 | Review denied by the Supreme Court | Petition denied by the Supreme Court, then the sentence "The appeals court’s ruling stands." | The docket's own word for the petition the step names, and plain. The rule's title then reads "...and never call a denied petition a ruling", or better, in the positive (W09): "Follow a court case through six steps, and end a denied petition at step 5." (14 words) |
| Step 6, a tie | (none) | Upheld by a tie vote, then "The lower court’s ruling stands." | The Court's "affirmed by an equally divided Court", in plain words, with the U.S. Courts page's own sentence |
| Steps 5 and 6, by agreement | (none) | Withdrawn by the parties | Supreme Court Rule 46.1's dismissal by agreement |
| Step 2, never appealed | (a square on step 2) | Decided for the plaintiff on March 3, with the sentence "No appeal was filed in the 30 days the law allows." *Illustrative* | Says what ended the line, in words, as ruling (f) asks |

### Rule 11.12's words for all four trackers (D3-1879)

The main session's call on ED5-2: Rule 11.12 covers the ballot measure and court case trackers too. The title stands ("Say a wait or a later step in words, and keep the count at six."), since it already names no tracker. The rest, for `apply_systems_ch11.py`:

| Field | Now | Words | Why |
|---|---|---|---|
| `rule[0]` | A wait inside a step, such as an agency’s question to the requester, a fee estimate or an extension of up to 10 working days, shows as words under the step it falls in. It never adds a mark, so every request still counts to six. A step outside the agency, such as mediation by the National Archives or a lawsuit, follows the end words as a sentence with its date. | A wait inside a step shows as words under the step it falls in and never adds a mark, so every tracker in this group still counts to six. A records request may wait on the requester’s answer, a fee estimate or an extension of up to 10 working days, and a draft agency rule may wait on review at the White House. A ballot measure may need a second round of signatures after the Legislature declines to act, and a court case may pause while a court of appeals hears an appeal of an order on an injunction. Anything after the end words, such as a lawsuit over a request or a rule, a case sent back to the trial court, or a legislature’s repeal of a measure the voters approved, follows them as a sentence with its date. | Names all four kinds, each with a wait its own source names: 5 U.S.C. 552(a)(6) for requests (as now), Executive Order 12866, section 6(b)(2), for a draft rule (it sets a review time, "within 90 calendar days after the date of submission", which the order lets the reviewers extend, so the words give no number), the second round of signatures in Massachusetts and Ohio, and 28 U.S.C. 1292(a)(1) for an injunction's appeal. The research lead's file gives each. The last sentence keeps the old one's job for every kind; Massachusetts's "the general court may amend or repeal a law approved by the people" is the source for the repeal |
| `rule[1]` | A status taken from the agency’s own tracking service, or from the Federal Register for a rule, needs no mark. A status we piece together ourselves, such as a wait we learn of from the agency’s letter, carries a warning ... | A status taken from the deciding body’s own record needs no mark: an agency’s tracking service, the Federal Register for a rule, the state election office’s notice for a ballot measure, or the court’s docket for a case. A status we piece together ourselves, such as a wait we learn of from an agency’s letter, carries a warning with the date we checked it, drawn as Rule 11.17 draws every warning: “Warning: Checked April 20. The agency may have acted since.” | Ruling (f)'s records, one per kind. The warning's example stays a request's, since the plates show requests |
| `why.text[0]`, second sentence | A count that changed from one request to the next would stop readers from comparing them. | A count that changed from one item to the next would stop readers from comparing them. | The rule now covers four kinds of item |
| Spec "Waits, in words" | “Waiting on you”, a fee estimate or an extension, under the step it falls in, with its date | “Waiting on you”, a fee estimate or an extension on a request; a second round of signatures on a ballot measure; an appeal of an injunction on a court case; each under the step it falls in, with its date | One example a kind; the rule has the rest |
| Spec "After the agency" | Mediation or a lawsuit, in a sentence after the end words | Label: "After the end". Value: Mediation, a lawsuit, a case sent back or a repeal, in a sentence after the end words | The label named one kind of tracker |
| `why.basis` | 5 U.S.C. 552(a)(6); design judgment | 5 U.S.C. 552(a)(6); Executive Order 12866; 28 U.S.C. 1292(a)(1); design judgment | The new examples' sources |

"Declines to act" in `rule[0]` follows the sources' cases: Massachusetts asks for the second round when the General Court does not enact the measure, and Ohio when the General Assembly does not pass it, passes it amended or takes no action within four months.

## Words for the engineer

The palette specification's words (R5-3, DR-234, DR-236), written at 01:50 UTC before the data lead's ruling (b), which sets the palettes, grounds and proofs; I change these only where the ruling makes them untrue. Facts by script: Rule 14.5 names "the four data palettes" (sequential Verdigris, diverging pair B, the four group inks with Stone hatched, the Stone magnitude steps); `tokens.json` holds each one `onNewsprint` and `onCharcoal`; chapter 05 already has an extra labeled "Every palette pair, measured" (after Rule 05.5), so this label must differ; Rule 05.7 prints the color-vision measure and chapter 05's sources cite the simulation model (Machado and others, 2009, severity 1.0); Rule 13.4 is "Draw a connection’s grade in the atlas’s line code."; Rule 26.7 is the token table.

| Field | Words | Why |
|---|---|---|
| Label (now in `14-chapter.json`'s `extras`, R5-2a) | The four data palettes, step by step | Rule 14.5's own name for them, and it says what the plate adds to the rule: every step. Differs from chapter 05's "Every palette pair, measured" |
| Caption | Each of the four palettes appears with its job and its steps, and each step with its token name, its value and its contrast on every ground we approve it for. Gray and three color-blind simulations follow each palette, then the line code for evidence grades from Rule 13.4. The table in Rule 26.7 lists every token. | Three sentences that name what the plate holds, in the order R5-3 gives. "On every ground we approve it for" holds whichever grounds ruling (b) sets. "Simulations" claims only what the proof is (W20). Rule 26.7 sends a reader to the token list, so the plate need not repeat it (R5-3: "Chapter 26’s table stays the token list") |
| Proof labels on the plate | Gray; Red-blind (protanopia); Green-blind (deuteranopia); Blue-blind (tritanopia) | Plain names first, the term after it once (H02). At severity 1.0 the model simulates full loss of one kind of cone, which is what "red-blind" says. If the plate shows a partial severity, the label says "weak red vision" and so on |
| A note under the proofs, if the plate has room | Simulated with the model chapter 05 cites, at full strength. | One line names the method once and points to its source, which chapter 05's source list already prints in full |
| Job words, one per palette | Sequential: one measure, from low to high. Diverging, pair B: above and below a midpoint. Groups: up to four named groups, in this order. Magnitude: size with no direction. | Rule 14.5's own words for each job, cut to a phrase for a label |

## Words for the systems designer

Chapter 15's groups 5 and 6, written at 01:50 UTC from the round 1 rule plan (`work/handoffs/phase-3/20261112_Round-1-Systems-Designer-Notes.md`), the atlas's route list and the rerun file. I read both lines again against your plates as they land.

| Field | Now (plan) | Words | Why |
|---|---|---|---|
| Group 5 title | Routes to change as workflows | Routes to change, stage by stage | "Workflow" is our word; "stage by stage" says what the three rules draw. If you keep the plan's title, the line below still fits |
| Group 5 line | (none) | A reform can travel through eleven routes, from a city council to a constitutional amendment, and each route here carries its official source and the date it was checked. The federal statute’s route is drawn whole, from a bill’s introduction to its repeal or expiry, and each tracker’s six steps are matched to the stages they fold together. | The first clause is the atlas's own sentence on its routes ("A reform can travel through eleven routes, from a city council to a constitutional amendment."). The rest names Rules 15.24, 15.22 and 15.23: the research lead's FS stages run from "Introduction and committee" to "Repeal or sunset" (`work/research/20261111_Policy-Workflow-Sources.md`), and "expiry" is the plain word for a sunset; Rule 11.1 says six steps "fold some procedure together". The 113 undated entries belong to reforms' routes, not to the eleven routes' own stages, so "the date it was checked" is true of every route on the plate. Two sentences on different frames (W13) |
| Group 6 title | Earlier drawings | Earlier drawings of the atlas | Says whose drawings, so a reader does not take them for this guide's |
| Group 6 line | (none) | Earlier drawings of the atlas record what we once showed, and the model holds the values. The table lists each place a drawing disagrees with the model or could be misread, with the model’s value, how we settled it and the rule where this guide applies the answer. | Rule 15.14's spec already calls an earlier drawing "A record, never evidence"; the line says the same thing in the positive (W09). "Disagrees ... or could be misread" covers R5-6's conflicts and ambiguities (the ID rows are pages where two IDs collide, not wrong values). The list of three is the table's three columns (W12) |

## Chapter 14's intro (draft, applied once the items exist)

The intro now says "Fourteen rules come first", which stops being true when the selection guide opens the chapter, and says every entry has "a finished example that our chart kit draws", which was never true of the 30 reference and avoid sketches. The draft, for the first paragraph of `intro` in `phase3_ch14_rules_build.py`; the second paragraph stands:

> This chapter sets how Oath & Action shows numbers. It opens with a guide to choosing a chart, every form listed under the question it answers. Fourteen rules then hold for every chart, with the four data palettes set out step by step after the rule on color. Each of the 127 forms has its own entry, grouped by its question, with when to use it and what to use instead. A core or extended form shows a finished example that our chart kit draws from frozen data, with its table as live text, and a reference form or a form to avoid is drawn as a sketch. Three charts in full close the chapter, each putting several forms and rules together on one subject.

Sentence lengths 8, 16, 21, 25, 35 and 18 words, on six different frames (W03, W13). In the same pass, once the guide's anchor is set: the opener's caption ("Each group of this chapter opens with the question a reader brings") becomes "Each family of forms opens with the question a reader brings, and its forms answer it.", since groups 1 and 18 open on none; and Rule 14.1's sentence "Each group of this chapter opens with one of those questions" and its "Question to form" spec point to the guide that opens the chapter.

## Routine calls

- D3-xxx | Chapter 14's opener lists the plan's groups that carry a family section, so groups 1 and 18 never enter it | Group 18 opens on no reader question, and a plan row for it would otherwise stop the generator on its title and its missing drawing
- D3-xxx | Group 18's working line sits in `GROUP_LINES[18]` before the engineer's plan row lands | The generator writes every plan group's line, and a missing one stops it
- D3-xxx | The selection guide keeps the label "Choose a chart" | The chapter's own instruction and Rule 14.1 say "choose"; three words name the reader's action
- D3-xxx | The selection guide's tier words are Core, Extended, Reference and Avoid, defined once in its caption, and Rule 14.130's "Extended, interactive" prints "Extended" | The guide prints no tier word before this plate, so its caption is the first use (H02); the form's name already says it is live
- D3-xxx | `14-chapter.json` carries an `extras` list with the selection guide's and the palette specification's printed label and caption, written by `phase3_ch14_rules_build.py` | R5-2a: the editor's words there take the place of each generator's draft; working words until rulings (a) and (b) and the drafts land
- D3-xxx | The palette specification's label is "The four data palettes, step by step" | Rule 14.5's own name for the palettes, and chapter 05 already labels an extra "Every palette pair, measured"
- D3-xxx | Rule 14.144's working title says "effect" where the brief says "measure" | In a civic guide a measure is also a bill or a ballot question, and the atlas calls each column an effect

## Requests

- **ED5-1, to the engineer. Closed at 01:52 UTC.** Group 18's title "Three charts in full" is in the plan's new row as I asked, and my generator now writes the group with its line into `14-chapter.json`; the opener stays at its 16 questions. The two extras' printed labels and captions are in `14-chapter.json`'s `extras` (R5-2a), so the palette plate prints "The four data palettes, step by step".
- **ED5-2, to the tracker designer.** The question on Rule 11.12 (old 11.10) under "Words for the tracker designer": does it cover the new trackers' waits?

## Tested

- `phase3_ch14_rules_build.py` run as committed at 01:46 UTC: every check passes, and `git status` shows no entry or specimen of mine changed. After the two edits (opener filter, group 18 line), run again: the same counts (14 rules, 29 plates, 13 specs, 68,936 bytes, opener 5,009 bytes) and still no file of mine changed.
- The same generator with group 18 added to the plan in memory only (`sim_g18.py` in my scratch folder), `--check-only`: every check passes, the opener lists 16 questions, and the chapter's groups end 16, 17, 18.
- At 01:52 UTC, after the plan's group 18 row and my `extras` list: the generator's checks pass (14 rules, 29 plates, opener 5,009 bytes); `14-chapter.json` gains group 18 (before Rule 14.142, with its line) and `extras`, and nothing else of mine changes; a second run leaves every `14-*.json` and `s-14-*` plate of mine byte for byte (hashes before and after).
- Word counts of the four working titles by script: 15, 14, 14 and 13.
- These notes, by script: no em dash and no U+2011.

## Not tested

- The engineer's chapter build with group 18 in the plan, which waits for the row.
- Any word here against a built plate: none of the round 5 items exists yet.
