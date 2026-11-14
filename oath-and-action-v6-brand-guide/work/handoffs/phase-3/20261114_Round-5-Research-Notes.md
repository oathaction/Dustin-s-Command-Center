# Round 5 research notes

Oath & Action Edition 06, Phase 3, round 5, November 14, 2026. Research lead (`oa-research-lead`), under `work/handoffs/phase-3/20261114_Phase-3-Round-5-Brief.md`, the research lead's row and bullet. Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/7633c399-b692-5041-be92-a87ecd098fbf/scratchpad/phase-3/round-5/research/`. Written as I go, since the container can restart.

## Status

- 01:50 UTC. Item 1 written under "Facts for owners": the ballot measure and court case frames, six steps each, with end words and sources read today. Adding the same rows to the workflow sources file next, then item 2.
- 01:41 UTC. Started. Read `CLAUDE.md`, the role file, the round 5 brief in full, the workflow sources file, round 4's research notes and the three reconciliation files. Working on item 1, the two new trackers' steps, first.

## Summary

To come.

## Facts for owners

### 1. The two new trackers (for the tracker designer)

Written 01:50 UTC. Every source below was fetched from this container on November 14, 2026, between 01:43 and 01:47 UTC, saved in its own download folder under scratch (`dl/ballot/`, `dl/court/`, each with `fetch-log.tsv` giving status, bytes and SHA-256) and read as text by `python3 -I`. A quote is copied from that text. The same rows, with fuller quotes, are in the workflow sources file under "Round 5: the ballot measure and court case trackers". The step names are my proposals in plain words for the editor and the data lead's ruling (f); the end words come from the law's own verbs, put plainly. Each frame keeps six steps (DR-108), uses the slash for a step that never happened and a square where an item stops, and says a decided or certified end in words (R5-7).

#### Rule 11.10, the ballot measure: a citizen initiative in six steps

States differ, so the frame is built from four states' constitutions and one election office: Massachusetts (an indirect initiative: the Legislature votes first), California (a direct initiative: it goes straight to the ballot), Ohio and Michigan (indirect, for laws). Massachusetts's and California's texts were read in full today; Ohio's and Michigan's sections were read in full.

| Step | Proposed name | What happens, and the law's words | Source | Checked |
|---|---|---|---|---|
| 1 | Filed | The proponents file the measure's full text with the official the law names. Massachusetts: the petition "shall first be signed by ten qualified voters of the commonwealth and shall be submitted to the attorney-general not later than the first Wednesday of the August before the assembling of the general court". California: a written request to the Attorney General for "a circulating title and summary" (Elec. Code 9001, as the guide gives it) | Massachusetts Constitution, Amendment Article XLVIII, The Initiative, II, Section 3, as replaced by Amendment Article LXXIV, Section 1, https://malegislature.gov/Laws/Constitution ; California Secretary of State, Statewide Initiative Guide, revised January 2026, Step Two, https://elections.cdn.sos.ca.gov/ballot-measures/pdf/statewide-initiative-guide.pdf | 2026-11-14 |
| 2 | Title and summary | The attorney general clears the measure and writes the words petitions and ballots carry. Massachusetts: the attorney general certifies "that the measure and the title thereof are in proper form for submission to the people", that it is not substantially the same as a measure at either of the two preceding state elections, and that it "contains only subjects not excluded from the popular initiative"; each petition carries "a fair, concise summary, as determined by the attorney-general". California: the Attorney General prepares "a circulating title and summary, which will be the official summary of the proposed initiative measure" (Elec. Code 9004(a)), and "No petition may be circulated prior to the official summary date" (Elec. Code 9014) | Same two sources | 2026-11-14 |
| 3 | Signatures | The proponents gather signatures and file them; election officials count and check them. Massachusetts: the first round is filed "not later than the first Wednesday of the following December". California: a raw count, then a random sample; under 95 percent projected valid, "the proposed initiative measure fails to qualify for the ballot"; between 95 and 110 percent, every signature is checked (a "full check") | Massachusetts, as step 1; California guide, Chapter II, Verification of Signatures (Elec. Code 9030, 9031) | 2026-11-14 |
| 4 | Legislature | Indirect initiative only. The Legislature votes on the measure as filed. Massachusetts: "a vote shall be taken by yeas and nays in both houses before the first Wednesday of May upon the enactment of such law in the form in which it stands in such petition"; if it fails to enact it, a second round of signatures, "not less than one half of one per cent of the entire vote cast for governor", is filed between the first Wednesday of June and the first Wednesday of July. Ohio: if the General Assembly does not pass it, or passes it amended, or takes no action "within four months", a supplementary petition of three percent more electors sends it to the voters. Michigan: the Legislature must enact or reject it "without change or amendment within 40 session days", and may "reject any measure so proposed by initiative petition and propose a different measure upon the same subject", in which case "both measures shall be submitted" | Massachusetts Amendment Article LXXXI, Section 2 (replacing XLVIII, The Initiative, V, Section 1); Ohio Constitution, Article II, Section 1b, https://codes.ohio.gov/ohio-constitution/section-2.1b ; Michigan Constitution of 1963, Article II, Section 9, https://www.legislature.mi.gov/Laws/MCL?objectName=mcl-Article-II-9 | 2026-11-14 |
| 5 | On the ballot | The state's election officer certifies the measure for the ballot. California: the Secretary of State "will issue a certificate of qualification on the 131st day before the next statewide general election certifying that the initiative measure, as of that date, is qualified for the ballot" (Elec. Code 9033(b)). Massachusetts: once the second round is filed, "the secretary of the commonwealth shall submit such proposed law to the people at the next state election" | California guide, Chapter III, Qualified for the Ballot; Massachusetts Amendment Article LXXXI, Section 2 | 2026-11-14 |
| 6 | Vote | The voters decide, and the result is certified before the measure takes effect. California: "An initiative measure approved by a majority vote takes effect the fifth day after the Secretary of State certifies the election results, unless the initiative measure provides otherwise" (Cal. Const., art. II, sec. 10(a), as the guide gives it). Massachusetts: a law passes only if approved "by voters equal in number to at least thirty per cent of the total number of ballots cast at such state election and also by a majority of the voters voting on such law", and "shall take effect in thirty days after such state election" unless the law says otherwise. Ohio: approved measures "shall take effect thirty days after the election". Michigan: a law approved by the people takes effect "10 days after the date of the official declaration of the vote" | California guide, Chapter IV, Initiative Effective Date; Massachusetts Amendment Article LXXXI, Section 2; Ohio Article II, Section 1b; Michigan Article II, Section 9 | 2026-11-14 |

**How the three kinds fit the six steps.**
- **Direct initiative** (California): steps 1, 2, 3, 5 and 6; step 4 keeps a slash, since no legislature votes on it. California's Legislature does hold a joint public hearing, but "cannot amend it or prevent it from appearing on the ballot" (Elec. Code 9007, as the guide gives it, Step Two). My suggestion for ruling (f): the slash on step 4 with that sentence as words under it, since the step's meaning is a vote that can change the outcome.
- **Indirect initiative** (Massachusetts, Ohio, Michigan): all six steps. The second round of signatures that follows the Legislature's failure to act (Massachusetts, Ohio) shows as words under step 4, with its deadline, as Rule 11.10 (old numbering) puts a wait inside the step it falls in, so the count stays at six. If the Legislature enacts the measure, it ends there as law: the words say "Enacted by the Legislature on" and the date, and steps 5 and 6 keep slashes. In Michigan and Ohio a law the Legislature enacts this way is "subject to referendum" (their words). A competing measure the Legislature adds (Michigan; Massachusetts's "legislative substitute", XLVIII, III, Section 2) is a sentence under step 4.
- **Legislative referral**: the Legislature votes to put the measure on the ballot, so no petition exists: steps 1 to 3 keep slashes, step 4 fills with "Referred by the Legislature" and the date, then steps 5 and 6. Ohio: amendments "agreed to by three-fifths of the members elected to each house" go to the voters (Ohio Constitution, Article XVI, Section 1, https://codes.ohio.gov/ohio-constitution/section-16.1 , read 2026-11-14). Massachusetts: a legislative amendment needs "a majority of all the members elected" in joint session in two successive General Courts before it goes to the people (XLVIII, The Initiative, IV, Sections 4 and 5). The time a referral spent as a bill belongs to the bill tracker.

**End words, from the law's own verbs.**

| Where it ends | End words (proposed) | From | Source |
|---|---|---|---|
| Step 2 | "Not certified by the attorney general" | Massachusetts: the measure may be filed only "if he shall certify" | XLVIII, II, Section 3, as replaced by LXXIV |
| Steps 1 to 5 | "Withdrawn by its proponents" | California: proponents "may withdraw their measure at any time before the initiative qualifies for the ballot on the 131st day before the statewide general election" (Elec. Code 9033, 9604) | California guide, Withdrawal of Initiative Measure |
| Step 3 | "Did not qualify: too few valid signatures" | California: "fails to qualify for the ballot" (Elec. Code 9030(f), 9031) | California guide, Chapter II |
| Step 4 | "Enacted by the Legislature" | Massachusetts ("enact"), Michigan ("enacted by the legislature"), Ohio ("passed by the general assembly") | LXXXI, Section 2; Michigan II, 9; Ohio II, 1b |
| Step 5 | "Removed from the ballot by a court" | Courts hear challenges before the vote; Ohio gives its Supreme Court "exclusive, original jurisdiction in all cases challenging the adoption or submission of a proposed constitutional amendment" referred by the General Assembly | Ohio XVI, 1. The other states' court routes were not read today |
| Step 6 | "Passed" and "Failed", each with the date; then "Certified" with its date; then when it takes effect | The constitutions' "approved by a majority", "approval or rejection" and "certifies the election results" | As step 6 above |
| Step 6, Massachusetts only | "Failed: most voters said yes, but too few ballots" (wording for the editor) | A law needs a majority of those voting on it and yes votes equal to 30 percent of all ballots cast | LXXXI, Section 2 |

Before certification, a count is unofficial. Alaska's 2026 measure is the guide's own example: an unofficial count on November 10, 2026, and a target date to certify of November 25, 2026 (workflow sources file, BI; research ledger P7-036a). So a measure that leads on election night reads as counted, not passed, until the state certifies it; the exact words are for ruling (f). After the end words, the law allows more: the Legislature may amend or repeal a passed law in Massachusetts ("the general court may amend or repeal a law approved by the people", XLVIII, General Provisions, VI), only with voter approval in California unless the measure allows it (art. II, sec. 10(c), as the guide gives it), and only by three-fourths of each house in Michigan unless the measure says otherwise; no governor's veto reaches an initiated law in Ohio or Michigan. These follow the end words as a sentence, as Rule 11.10 (old numbering) does for a lawsuit after a records request.

Out of this frame: a popular referendum on a law the Legislature passed (Massachusetts, Ohio and Michigan have one), which could use steps 1 to 3, 5 and 6 with step 4 under a slash; local measures, which follow each city's charter; Alaska's petition steps, since its constitution pages refused the reader today (a certificate error at ltgov.alaska.gov and no answer from akleg.gov).

#### Rule 11.11, the court case: a federal civil case in six steps

A federal civil case runs through three courts, and each court has a step where a party asks and a step where the court decides. Title 28 sets the courts' powers and time limits; the Federal Rules of Civil and Appellate Procedure and the Supreme Court's own rules set the steps.

| Step | Proposed name | What happens, and the law's words | Source | Checked |
|---|---|---|---|---|
| 1 | Filed | "A civil action is commenced by filing a complaint with the court." A case under federal law starts in a district court, the federal trial court: "The district courts shall have original jurisdiction of all civil actions arising under the Constitution, laws, or treaties of the United States." | Federal Rules of Civil Procedure, Rule 3 (edition of December 1, 2025), https://www.uscourts.gov/sites/default/files/document/federal-rules-of-civil-procedure.pdf ; 28 U.S.C. 1331, https://www.govinfo.gov/content/pkg/USCODE-2024-title28/html/USCODE-2024-title28-partIV-chap85-sec1331.htm | 2026-11-14 |
| 2 | Trial court ruling | Motions, discovery and, absent a settlement, a trial; the case ends here with a judgment the clerk enters. "The court shall grant summary judgment if the movant shows that there is no genuine dispute as to any material fact"; "Absent a settlement, the court will schedule a trial" | FRCP Rules 41, 56 and 58; U.S. Courts, "Civil Cases", https://www.uscourts.gov/about-federal-courts/types-cases/civil-cases | 2026-11-14 |
| 3 | Appeal | The losing party files a notice of appeal. "The courts of appeals ... shall have jurisdiction of appeals from all final decisions of the district courts"; the notice is due "within thirty days after the entry of such judgment", or 60 days when the United States, an agency or an officer is a party | 28 U.S.C. 1291, https://www.govinfo.gov/content/pkg/USCODE-2024-title28/html/USCODE-2024-title28-partIV-chap83-sec1291.htm ; 28 U.S.C. 2107(a) and (b), https://www.govinfo.gov/content/pkg/USCODE-2024-title28/html/USCODE-2024-title28-partV-chap133-sec2107.htm ; Federal Rules of Appellate Procedure, Rule 4(a)(1) (edition of December 1, 2024) | 2026-11-14 |
| 4 | Appeals court ruling | A panel of three judges decides. A court of appeals "may affirm, modify, vacate, set aside or reverse any judgment, decree, or order of a court lawfully brought before it for review, and may remand the cause". The full court may rehear a case ("en banc"), which "is not favored". The decision takes effect when the court's mandate issues: "The mandate is effective when issued" | 28 U.S.C. 2106, https://www.govinfo.gov/content/pkg/USCODE-2024-title28/html/USCODE-2024-title28-partV-chap133-sec2106.htm ; FRAP Rules 40 and 41(c); U.S. Courts, "Appeals", https://www.uscourts.gov/about-federal-courts/types-cases/appeals | 2026-11-14 |
| 5 | Supreme Court petition | The losing party asks the Supreme Court to hear the case. "Review on a writ of certiorari is not a matter of right, but of judicial discretion"; a petition is timely "within 90 days after entry of the judgment", and a justice may extend that by up to 60 days. The Court grants or denies the petition by order | Rules of the Supreme Court of the United States, adopted February 17, 2026, effective March 16, 2026, Rules 10, 13.1, 13.5 and 16, https://www.supremecourt.gov/filingandrules/2026RulesoftheCourt_WEB.pdf ; 28 U.S.C. 1254(1) and 2101(c) | 2026-11-14 |
| 6 | Supreme Court ruling | Briefs, oral argument, then the Court's decision, with the same powers as step 4 (28 U.S.C. 2106). "When there is a tie vote, the decision of the lower Court stands." The Court sends its judgment to the lower court "32 days after entry of the judgment" unless the time changes | 28 U.S.C. 2106; Supreme Court Rules 16.2 and 45.3; U.S. Courts, "Supreme Court Procedures", https://www.uscourts.gov/about-federal-courts/educational-resources/about-educational-outreach/activity-resources/supreme-1 | 2026-11-14 |

**Slashes and squares.** A case decided at step 2 and never appealed keeps steps 3 to 6 under slashes once the time to appeal has passed, as Rule 11.8's step 6 does for a records request. A petition the Supreme Court denies keeps step 6 under a slash; the words say the appeals court's ruling stands (Rule 16.3: "Whenever the Court denies a petition for a writ of certiorari, the Clerk will prepare, sign, and enter an order to that effect"). A case that skips the court of appeals keeps steps 3 and 4 under slashes: a direct appeal from a three-judge district court (28 U.S.C. 1253, which the Supreme Court must hear), or review before the appeals court decides (Rule 11; 28 U.S.C. 2101(e)), which keeps step 4 alone under a slash. A case that ends by settlement or dismissal ends its line on a square at the step where it stopped.

**End words, from the law's own verbs.**

| Where it ends | End words (proposed) | From | Source |
|---|---|---|---|
| Step 2 | "Settled", with the date the parties filed to dismiss | "a stipulation of dismissal signed by all parties who have appeared"; "litigants often agree to a 'settlement'" | FRCP 41(a)(1)(A)(ii); "Civil Cases" |
| Step 2 | "Dismissed", or "Dismissed by the plaintiff" | FRCP 41(a) and (b); Rule 12(b)(6), "failure to state a claim upon which relief can be granted" | FRCP 12(b), 41 |
| Step 2 | "Decided", with the date and for whom; "without a trial" where the court granted summary judgment | FRCP 56(a), 58 | FRCP |
| Steps 4 and 6 | "Affirmed", "Reversed", "Vacated", "Modified" | 28 U.S.C. 2106's own verbs | 28 U.S.C. 2106 |
| Steps 4 and 6 | "Sent back to the lower court" (remanded), joined to the verb before it: "Reversed and sent back" | "may remand the cause and direct the entry of such appropriate judgment" | 28 U.S.C. 2106 |
| Step 4 | "Appeal dismissed" | "The circuit clerk must dismiss a docketed appeal if the parties file a signed dismissal agreement"; "An appeal may be dismissed on the appellant's motion" | FRAP 42(b) |
| Step 5 | "Review denied" (the line ends; step 6 under a slash) and "Review granted" (on to step 6) | Rule 16.2 and 16.3 | Supreme Court Rules |
| Step 6 | "Affirmed by an equally divided Court" | "When there is a tie vote, the decision of the lower Court stands" | "Supreme Court Procedures" |
| Steps 5 and 6 | "Dismissed" | "whenever all parties file with the Clerk an agreement in writing that a case be dismissed ... the Clerk ... will enter an order of dismissal" | Supreme Court Rule 46.1 |

**Remand.** A remand sends the case back down; it does not end it. Rule 11.8's records request has the same shape after an appeal ("Reversed and sent back"). My suggestion for ruling (f): print the end words at the step that decided ("Reversed and sent back on June 2"), keep the marks where they are, and add a sentence that the lower court takes the case up again, as Rule 11.10 (old numbering) adds a step outside the agency as a sentence. The marks never move backward.

**Inside a step, as words.** An order on an injunction before the final judgment can be appealed at once: the courts of appeals hear appeals from "Interlocutory orders ... granting, continuing, modifying, refusing or dissolving injunctions" (28 U.S.C. 1292(a)(1)). Many cases over a law or a rule run this way, so a preliminary injunction and its appeal show as words under step 2, and steps 3 and 4 track the appeal from the final judgment. A rehearing by the full appeals court shows as words under step 4. A petition for rehearing in the Supreme Court is due within 25 days (Rule 44.1), words under step 6.

**Limits for the plate's note.** This frame is a federal civil case. A criminal case starts by indictment or information under the criminal rules, and the government may not appeal an acquittal (U.S. Courts, "Appeals": "the government may not appeal if a defendant is found not guilty"). A case in a state court follows that state's courts, and reaches the U.S. Supreme Court only on a federal question from the state's highest court. Real cases (Loper Bright, among them) stay in chapter 15's court workflow (CRT) as the steps' source, as Q5-4 set.

**Currency.** The Supreme Court's rules changed on March 16, 2026; the workflow sources file cited the 2023 edition for Rule 10. By script, Rules 10, 11, 13, 16 and 44 to 46 read the same in both editions once the "fi" letters the 2023 file drops are set aside; the 2026 revisions touched Rules 14, 15, 24, 29 and 48 (the Court's own revisions file). Title 28 was read in govinfo's 2024 edition; the Law Revision Counsel's viewer returned 404 at every address tried today, so no section was compared with its current release (Not tested). The appellate rules' current file on uscourts.gov has no text layer a script can read; the December 1, 2024 edition was read instead, and its Rules 4, 40, 41 and 42 are quoted.

### 2. The 11 routes (for the systems designer, Rules 15.22 and 15.24)

To come.

### 3. The reconciliation rows (for the systems designer, Rule 15.25)

To come.

### 4. ED4-7, S92's sidecar source line

To come.

## Routine calls

## Requests

## Tested

## Not tested

## Claims I could not verify
