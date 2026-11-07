# Apply pass: red team, brand, evidence and nonpartisanship

Oath & Action Edition 06, Phase 2, November 7, 2026. Written by the research lead (`.claude/agents/oa-research-lead.md`), with the creative director's brand knowledge, for the "Brand, evidence and nonpartisanship" lens of `20261107_Apply-Pass-Review-Brief.md`. I reviewed the page at commit c6106e6, `work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html`, rendered in Playwright Chromium, and checked its claims against `20261107_Apply-Pass-Research.md` and the primary records I could open. I edited no guide file, board or ledger, and committed nothing.

## Verdict

Two items block showing Dustin the board. Both are cheap to fix.

- **BE-01, Must fix.** Chapter 11 tells readers that at a committee hearing "anyone can speak or send written testimony". The rules of the House and the Senate say otherwise: committees hear the witnesses they call. Chapter 01's H.R. 7008 card then draws that step as a slash on a real bill, so a reader learns that the public lost its chance to speak on it.
- **BE-02, Must fix.** Rule 01.11's new title asks writers to "report the counts as the record gives them". Its correct plate shows Texas and California, one case each, with no count. Our atlas lists more mid-decade redraws for the same loop, and nobody has counted them by party. Until someone does, the plate may teach the even pairing DR-93 rules out.

Everything else holds against the record: the 2020 example's quotations and pages, the H.R. 7008 card's six steps, both first mentions of the bill, and Rule 02.25's Senate count. The Should fix items below tighten wording to the record and make one call into a standing rule.

## Findings

### Must fix

**BE-01 | Chapter 11, the six steps (`s-11-steps`), Rule 11.1's reason, step 5's line; through them, chapter 01's H.R. 7008 card (`s-01-pieces`) and chapter 11's federal example**

What the page says:
- Step 2: "The committee holds a public hearing, where anyone can speak or send written testimony."
- Step 5: "Its own committee often holds a hearing first, where the public can speak again".
- Rule 11.1's reason: "The hearing keeps a step of its own because it is where the public is invited to speak, and a bill that skips it is news."
- Rule 11.1 applies the six steps to federal bills ("President on a federal one"), and chapter 01's card applies them to H.R. 7008, with step 2 slashed.

What the record shows for Congress:
- **House.** House Rules and Manual, 119th Congress (H. Doc. 118-187, govinfo HMAN-119), rule XI, clause 2:
  - Hearings are open to the public to attend (2(g)(2)(A)).
  - The chair announces each hearing a week ahead (2(g)(3)(A)).
  - "witnesses who appear before it" file written statements in advance (2(g)(5)(A)).
  - The minority may "call witnesses selected by the minority" for at least one day (2(j)(1)).
- **Senate.** Standing Rules of the Senate (S. Doc. 113-18, revised to January 24, 2013), rule XXVI, paragraphs 4(a), 4(b) and 4(d), follow the same model.
- Neither set of rules gives a member of the public a right to speak or to file testimony.
- The one hearing on record for H.R. 7008's subject heard invited witnesses: the legal policy director of the Manhattan Institute and a specialist at the Congressional Research Service (H. Rept. 119-479, footnotes 6 and 7).
- I found no source for "a bill that skips it is news". The House's own rule XIII, clause 3(c)(6)(A), lets a committee designate a related hearing "used to develop or consider" a bill, which is the route H.R. 7008 took.

Why it blocks: on a federal bill the definition is false. Applied to a real bill that passed the House on a near party-line vote, the slash plus the definition reads as a charge the record does not support. DR-93 rules out a finding hardened past its evidence.

The change I ask for (systems designer, `apply_systems_ch11.py`). The interim wording below needs no new research:
- Step 2: "The committee holds a hearing and takes testimony on the bill. Who can testify depends on the legislature; a bill's own page says how to take part."
- Step 5: delete "where the public can speak again".
- Rule 11.1's reason: "The hearing keeps a step of its own because it is where a committee takes testimony on the bill." Drop "and a bill that skips it is news" unless someone sources it.
- A line that says anyone can speak may return only for legislatures the research lead has checked, and only scoped to them.

**BE-02 | Chapter 01, Rule 01.11, correct plate (`s-01-11-correct`)**

What the page says:
- Title: "Show a case from each party that uses a mechanism, and report the counts as the record gives them."
- Second paragraph: "When the record shows one party using a mechanism more, report it that way, with the counts".
- The rule calls Loop R4a "the test case". The plate shows Texas and California, one case each, with no count.

What the record shows:
- Our atlas's own case text for R4a (`20261105_Atlas-Editorial-Data.json`, `loops`, R4a, `case`) records more than the two. It says "After Louisiana v. Callais (April 29, 2026), four Southern states redrew maps that removed majority-Black districts", and it names Missouri's 2025 map.
- The November 6 research report quotes the Supreme Court's order of December 4, 2025 (No. 25A608): "several States have in recent months redrawn their congressional districts in ways that are predicted to favor the State's dominant political party."
- Nobody has counted these redraws by the party of the majority that drew each map. I did not count them either (Not tested).

Why it blocks: the plate does not do what its own title asks. If the count falls more on one side, the correct plate of the rule that teaches DR-93 is the even pairing DR-93 rules out.

The change I ask for:
1. The research lead counts the 2025 to 2026 congressional redraws in R4a's case record by the party of the majority that drew each map, with a primary source for each, and logs the count.
2. If one party leads, the editor adds one sourced line under the two cases in their form, for example "Of the N mid-decade congressional redraws our atlas records for 2025 and 2026, X were drawn by Republican-led legislatures and Y by Democratic-led ones."
3. If the count is even, the caption says so and gives its source.

The two cases and the failure plate stay.

### Should fix

**BE-03 | Chapter 01, H.R. 7008 card, note line; chapter 11, Rule 11.2**

What the card says: "Step 2 never happened, because the committee held no hearing on this bill. Its report cites only a hearing held November 19, 2025, before the bill was filed."

What the record shows:
- The report says (H. Rept. 119-479, "Related Hearing"): "Pursuant to clause 3(c)(6) of rule XIII, the following hearing was used to develop H.R. 7008".
- For a bill taken up under a special rule, House rule XIII, clause 3(c)(6)(A), requires "a designation of at least one committee or subcommittee hearing that was used to develop or consider such bill".
- So the House counts that hearing for this purpose, and our tracker does not.

Assessment:
- The slash is a fair reading of DR-108. The research lead flagged it as a call.
- No decision logs that call, and no rule says how to draw a hearing on the subject held before a bill was filed. The next writer could draw the same facts the other way, which breaks one standard.
- "only" adds a judgment the report does not make.

The change I ask for:
- Log the call, and add one sentence to Rule 11.2's For builders that applies to every bill: "A hearing on the bill's subject held before the bill was filed does not fill step 2; the step's note names it."
- Card: "Step 2 never happened: the committee held no hearing on this bill. Its report names a November 19, 2025 hearing on the STOCK Act, held before the bill was filed, as the one used to develop it."

**BE-04 | Chapter 01, the 2020 example (`s-01-uneven`), "a July 2022 review by eight conservatives, among them two former U.S. senators and three former federal appeals judges"**

What the guide does elsewhere: Rule 01.16 names the holders of a reading "by role and affiliation". Its plate does this by institution only, "Economists at Harvard University" and "Economists at the Economic Policy Institute", with no political tag on either.

What this example does: it puts a political tag on one source's authors, in the body. There it works as a credential: board A's card gave as its reason "Its key finding comes from a review written by conservatives". That makes the source's politics part of the evidence, against DR-93's one way of describing sources.

Nothing is lost by dropping the tag from the body. The source line already prints the review's subtitle, "The Conservative Case that Trump Lost and Biden Won the 2020 Presidential Election", and the authors' own statement of party ties.

The change I ask for (editor, `guide_editor_ch01.py`):
- Describe the authors by role: "a July 2022 review by eight former officials and lawyers, among them two former U.S. senators and three former federal appeals judges".
- If the studio wants to keep the tag, the house rule it implies goes to Dustin first: print every source's stated politics wherever we cite it, the Economic Policy Institute included.

**BE-05 | Chapter 01, the 2020 example's caption**

What the caption says: "they add no case from another party to even the count".

The problem: the example names a campaign and "Donald Trump and his supporters", and no party, as Rule 01.13 asks. The caption assigns the case to a party that the lines never name.

The change I ask for: "and they add no counter-case to even the count, as Rule 01.11 asks."

**BE-06 | Chapter 01, the 2020 example, "counted 64 cases that Donald Trump and his supporters brought in six battleground states"**

What the review says: the words are its own, "Of the 64 cases brought by Trump and his supporters" (printed page 3).

What its own lists show: the research lead found that its addenda include suits filed before the election and cases others began. I found two of those rows myself:
- the Secretary's petition, 149 MM 2020 (printed page 60);
- the Democratic Party's suit listed as Republican Party of Pennsylvania v. Degraffenreid (printed page 59).

The problem: the source line covers the number ("The count of 64 cases is the review's own"). The "brought" clause still reads in our voice.

The change I ask for: "counted 64 cases it says Donald Trump and his supporters brought in six battleground states".

**BE-07 | Chapter 11, Rule 11.3 and its specifications**

What the rule says: "Once the governor or the President signs it, all six steps fill, and the words say 'Became law on'". Stopped covers "a veto that stands".

What the record shows: a federal bill also becomes law in two other ways (U.S. Constitution, Article I, section 7):
- two thirds of each House override a veto;
- the President does not return it "within ten Days (Sundays excepted)" while Congress sits.

Step 6's line already says lawmakers can override, but no state or wording covers a bill that became law over a veto.

The change I ask for (systems designer): "Once it becomes law, by signature, by a vote to override a veto or without a signature where the constitution allows, all six steps fill, and the words say how, as in 'Became law on April 2, over the governor's veto.'"

**BE-08 | Chapter 11, Rule 11.1, "A chamber is one half of a legislature, the House or the Senate"**

The problem: several states call one chamber the Assembly or the House of Delegates, and Nebraska's legislature has a single chamber. I know this but did not open a primary list.

The change I ask for:
- "A chamber is one house of a legislature, such as the House or the Senate."
- Carry Nebraska's route to stage B as a question. Step 5 there is neither "never happened" nor "not yet".

**BE-09 | Chapter 11, Rule 11.1's federal example, "Bill H.R. 3120, Passport wait times", labeled Illustrative**

What the record shows: H.R. 3120 is a real bill in the 119th Congress, the same Congress as H.R. 7008 on the same page. govinfo's bill status titles it "To improve the review and effectiveness of the cost of living adjustments to pay and benefits for members of the Armed Forces and civilian employees of the Department of Defense whose permanent duty station is located in the 19th Congressional District of California".

The problem: anyone who crops the label off the plate puts false status words on a real bill.

The change I ask for (systems designer):
- Give invented federal bills a number that cannot match a bill in the current Congress.
- Write that convention into Rule 11.1's For builders.

**BE-10 | Chapter 01, Rule 01.6 failure plate (`s-01-6-failure`)**

What the plate shows: "What the Senate vote on the Stop Insider Trading Act means for you / One vote, 53 to 47, and what comes next." This is a real bill and a real count, set as a finished card, and it carries no "Failure case: do not publish" band. D2-308 requires that band on a failure plate that someone could mistake for our work.

The risk: anyone who clips the card repeats the bare count without either provision, the framing DR-98 and board A's A14 were written to stop.

The change I ask for (editor):
- Add the band.
- Then either name both provisions in the deck, or switch the plate to an invented bill with one Illustrative label.

### Notes

**BE-11 | The 2020 example, word order.** At 390 px a line starts with "Lost, Not Stolen, a July 2022 review". The title has a comma of its own, and set roman with no marks it reads as part of the sentence. Chapter 06 keeps italic for quotations, so the fix is word order: "A July 2022 review titled Lost, Not Stolen, written by ..., counted 64 cases ...".

**BE-12 | Rule 02.25, "The office that decides" row.**
- The row reads "The committee chair decides which bills get a hearing."
- The House's rules back it: the chair announces each hearing (rule XI, clause 2(g)(3)(A)). Yet the row carries no source, while the rows beside it do.
- DR-123 approved the wording, so I ask only for a source line, for example "Rules of the House of Representatives, 119th Congress, rule XI, clause 2(g)(3)", or a scope of "In Congress".
- Some state legislatures hear every bill. I did not check them.

**BE-13 | The H.R. 7008 card's red "Follow this bill" button.** Rule 11.4's specifications say "In a list or on a card: A text link at least 44 px tall; the red button waits for the bill's own page". That row sits under the take-part mark, and the card's ask is a sign-up, so the row may not apply here. Still, a reader who compares the two chapters sees a red button where chapter 11 says a card takes a link. Rule 11.4 should say whether a card's other ask may take the red button. Rule 05.3 holds on the card: one working red.

**BE-14 | A risk for Dustin, and what not to do about it.** Chapter 01's one worked example of a finding that falls on one side falls on one candidate's side. Under DR-93 the remedy is never a second example added from the other side. The rotation log and BE-02's count are the defense. I record this so no one adds a counterweight later.

**BE-15 | The record supports DR-98 and D2-406.**
- In the Senate's debate of September 30, 2026, the majority leader described the bill as pairing "a stock purchase ban for Members of Congress and a voter ID measure" (page S5190).
- Senator Van Hollen called it "the so-called Stop Insider Trading Act" and "a political scam" (page S5198).
- I read these pages from my own text extraction of the Senate section.
- Both sides describe two provisions, and the guide's deck states both. The tracker's name is the bill's official short title, and the deck gives the context.
- No change.

## Checked against the record, and holds

**The 2020 example.**
- Both files match the research lead's (SHA-256 `39aafed6...` for the opinion, `e10e5fcc...` for the review).
- Opinion, page 21: "The Campaign never alleges that any ballot was fraudulent or cast by an illegal voter."
- Opinion, page 9: "the Campaign asks us for an injunction to prevent the certified vote totals from taking effect."
- Opinion, page 21: "we deny an injunction pending appeal."
- Opinion, page 1: the caption reads "SECRETARY COMMONWEALTH OF PENNSYLVANIA", filed November 27, 2020, and "NOT PRECEDENTIAL".
- Review, printed page 3: "failed to produce substantive evidence to make their case", "far too few votes to overturn the results" and "has worked in Republican politics, been appointed to office by Republicans, or is otherwise associated with the Party".
- Review, printed page 1: "We are political conservatives". The cover reads "July, 2022".
- Roles hold on lostnotstolen.org's signatory pages: Danforth and Smith as former U.S. senators; Luttig, McConnell and Griffith as former federal appeals judges.
- The source line's page numbers are right.

**H.R. 7008's card, all six steps.**
- Sources: the bill status file (updated October 1, 2026), H. Rept. 119-479, the introduced and House-passed texts, and the Congressional Record.
- Step 1, Filed: January 12, 2026.
- Step 2, Hearing: no hearing in the committee's activities.
- Step 3, Committee vote: ordered reported 7 to 4 on January 14, 2026, on a text with section 2 only.
- Step 4, First chamber: passed 232 to 198 on July 22, 2026, with section 3, the photo ID section.
- Step 5, Second chamber: received July 23, placed on the calendar August 6, and cloture failed 53 to 47 on September 30, as Vote 253 on page S5199.
- After September 30: no mention of the bill in the Senate pages or Daily Digests of October 29 and November 5, and the Senate's program for November 9 is H.R. 2347.
- Step 6, President: ahead.
- The marks match the record: slash on 2, heavy ring on 5, fine ring on 6, and "President" in the key (DR-128).

**First mentions (DR-98, D2-406).**
- Only chapters 01 and 02 name the bill. I searched every section's rendered text.
- Both first mentions read "as the House passed it" with both provisions.
- The provisions match the House-passed text: section 2's new Sec. 13152(a), "no covered individual may purchase a covered investment", where a covered individual is a Member, a spouse or a dependent child; and section 3, photo ID for federal elections.
- Neither the introduced nor the reported text holds a photo ID section, so "as the House passed it" is needed.

**Rule 02.25's Senate count (DR-126).**
- Page S5199 prints "[Rollcall Vote No. 253 Leg.]", yeas 53, nays 47, and the three-fifths ruling. All 100 senators voted, so 60 is three-fifths.
- I matched the 100 names to the congress-legislators roster (current file, retrieved November 7, 2026). Result: 53 yeas, all Republican; 45 Democratic nays; two independent nays (King and Sanders).
- One name needed care. The Record lists "Graham", and the roster's South Carolina Republicans are Tim Scott and Darline Graham Nordone, whose term began July 14, 2026. Either way the vote is a Republican's.

**DR-125 and DR-124 wording.**
- Chapter 01's opening paragraph, Rule 01.11's added sentence and reason, Rule 01.12's "the spread of examples" and Rule 01.20's "in a hinge headline" match board A's A13 card word for word.
- Rule 05.7 carries DR-124's three sentences exactly. "rather skip" appears nowhere.

**Words that must not appear on a reader page.** None in the rendered text or the alt and ARIA text: "Signal Grid", "of 9", "nine stages", "Gate", "condensed", "Board" with a number, "stage" with a letter, DR or D2 codes, "I155", and em dashes.

## Tested

- Rendered the page in Playwright Chromium at 1440 px and wrote out every section's visible text and every alt, ARIA and title string. Searched that text by script.
- Captured the H.R. 7008 card at 1440 and 390 px at twice size, the 2020 example at 1440 and 390 px, Rule 02.25's table at 1440 px and chapter 11's steps table at 1440 and 390 px. Looked at each.
- Downloaded the Third Circuit's opinion from govinfo.gov and Lost, Not Stolen through lostnotstolen.org's download link. Converted both to text by page and found each quotation by script. Opened the review's home page and five signatory pages.
- Downloaded and parsed H.R. 7008's bill status XML; H. Rept. 119-479; the introduced and House-passed texts; the Senate section of the Record for September 30, October 29 and November 5, 2026; and the Daily Digests for October 29 and November 5.
- Downloaded the congress-legislators current roster (JSON) and matched the roll call names to it by script.
- Searched the House Rules and Manual for the 119th Congress (govinfo HMAN-119) and the Standing Rules of the Senate (S. Doc. 113-18) for the hearing and witness rules. Read Article I, section 7, in govinfo's copy of the Constitution (CDOC-110hdoc50).
- Checked govinfo's bill status for H.R. 3120, S. 2045, S. 412 and S. 876 in the 119th Congress.
- Read atlas issue I155 and Loop R4a in the atlas editorial data.

## Not tested

- How state legislatures take testimony, and which hear every bill. This bears on BE-01's state wording and BE-12.
- The party count of R4a's redraws (BE-02).
- A primary list of state chamber names and Nebraska's route (BE-08).
- House Roll Call 280 by party. The page prints only 232 to 198.
- senate.gov, congress.gov, bioguide and court sites. I did not try them.
- Rule 05.3 and DR-97's labels on every view: I looked at the views named above and rely on `guide_check.js` for the rest.
- Screen readers, other browsers, and 1,024 and 360 px.
- Real readers.

## Claims I could not verify

- Whether "Graham" on page S5199 is Darline Graham Nordone. Her roster entry and the Record agree on party, so the count holds either way.
- The page numbers I give for the floor statements in BE-15, which come from my text extraction's page headers.
- The transcript of the November 19, 2025 hearing.
- The outcomes of the review's other 63 cases.
- Whether any congressional committee invites written statements from the public as a standing practice. The rules I read neither require nor forbid it.

## Change log

- Created: `work/handoffs/phase-2/20261107_Apply-Pass-Red-Team-Brand-Evidence.md` (this file).
- Modified: none.
- Downloads went to a folder of their own in the session scratchpad, and my scripts sat in a separate folder. Nothing was committed or pushed.
