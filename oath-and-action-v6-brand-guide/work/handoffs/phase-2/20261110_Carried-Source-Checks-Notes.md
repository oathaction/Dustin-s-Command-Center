# Carried source checks for Rule 01.11's plate

Research lead, November 10, 2026. Plate: `work/build/guide/specimens/s-01-11-correct.html` (chapter 01, Rule 01.11). These are the three source checks carried from the round 2 research notes (`20261110_Stage-B-Round-2-Research-Notes.md`, "Not verified") and D2-968, plus Missouri's status.

Status: complete. In short, all three claims hold, and the plate needs no wording change. Virginia's House of Delegates had 51 Democrats and 48 Republicans, with one seat vacant, when it gave the amendment its first passage on October 29, 2025, 51 to 42. The Senate followed on October 31, 21 to 16, and every yes vote in both chambers came from a Democrat. The California court's order is Document 216 in Case 2:25-cv-10616, "Filed 01/14/26", in the Central District of California. Ohio's commission minutes say "By a vote of 7-0, the motion passed." Missouri's Secretary of State still posts only unofficial results for November 3, 2026.

## 1. Virginia's 2025 House of Delegates

**Claim as printed:** "Virginia’s Democratic-led legislature sought a ninth through a constitutional amendment, and the state’s supreme court voided the statewide vote of April 21, 2026, in which voters approved it."

**What was open:** the round 2 notes checked the 2026 House (64 Democrats, 36 Republicans) and the Senate (21 Democrats, 19 Republicans), but not the House of Delegates that gave the amendment its first passage in October 2025.

### The resolution and its dates

| Fact | Source, URL | What the source says |
|---|---|---|
| Resolution number and session | Enrolled text, HJ6007ER, https://lis.blob.core.windows.net/files/1081143.PDF (SHA-256 `2f129185...a7c006c`) | "2024 SPECIAL SESSION I", "HOUSE JOINT RESOLUTION NO. 6007", "Proposing an amendment to Section 6 of Article II of the Constitution of Virginia ... relating to apportionment; congressional districts; limited authority of the General Assembly to modify." |
| Dates of first passage | Same enrolled text | "Agreed to by the House of Delegates, October 29, 2025" and "Agreed to by the Senate, October 31, 2025" |
| House vote, from the House's own record | House of Delegates, Minutes, "Wednesday, October 29, 2025", Special Session I, https://house.vga.virginia.gov/minutes/2028 (SHA-256 `36c9b490...b1aa35e7d`) | "HJ 6007 - Agreed to (Y-51 N-42 A-0)". Earlier the same day: "Leaves of Absence granted: Delegates Ennis, Knight, Marshall, and Runion" |
| Both chambers' votes, from LIS | LIS data file for the 2024 Special Session I (session code 20242), https://lis.blob.core.windows.net/lisfiles/20242/HISTORY.CSV (SHA-256 `ab9821d4...b86e37c9`). LIS's Learning Center describes these files and their address at https://help.lis.virginia.gov/data/index.asp | "H Agreed to by House (51-Y 42-N 0-A)", dated "10/29/2025", vote reference 2429597. "S Agreed to by Senate (21-Y 16-N 0-A)", dated "10/31/2025", vote reference SV90. Also "S Senator Head, Christopher T.  Amendments rejected (16-Y 21-N 0-A)" and "H Assigned Chapter 5 (Effective 10/31/2025 )" |
| Second passage, for comparison | LIS data file, 2026 regular session, https://lis.blob.core.windows.net/lisfiles/20261/HISTORY.CSV (SHA-256 `46a19424...e6cd95c2`) | HJ4: "H Agreed to by House (62-Y 33-N 1-A)" on "1/14/2026"; "S Agreed to by Senate (21-Y, 18-N, 0-A)" on "1/16/2026"; "H Assigned Chapter 976" |
| The court's description of both votes | Supreme Court of Virginia, Scott v. McDougle, Record No. 260127, opinion of "MAY 8, 2026", https://www.vacourts.gov/static/opinions/opnscvwp/1260127.pdf (SHA-256 `0b9afcc4...ef330a8f27d`) | "On October 31, 2025, during a disputed 2024 Special Session, the General Assembly approved by a party-line vote a proposed amendment to the Constitution of Virginia". "During the 2026 Regular Session that began in January, the General Assembly again voted by a party-line vote to approve the proposed amendment." |

### The House's party count in October 2025

| Fact | Source, URL | What the source says |
|---|---|---|
| Party of every 2025 member | House of Delegates History (DOME), House Clerk's Office, 2025 member list, https://history.house.virginia.gov/members?session=272, and each of its 100 member pages, for example https://history.house.virginia.gov/members/9977. Each page has a "service by session" table with a "Party" column. I read the 2025 row by script | 51 rows "Democrat" and 49 rows "Republican", one member per district |
| The one seat that changed hands during 2025 | C. Todd Gilbert, district 33, https://history.house.virginia.gov/members/8672 | "Sessions Served: 2006 - July 14, 2025"; 2025 row "Republican". The 2026 list shows Justin L. Pence in district 33 from "January 14, 2026". No other 2025 member's service ends before the term ends |
| Count on October 29, 2025 | Arithmetic from the two rows above | 99 members seated: 51 Democrats, 48 Republicans, district 33 vacant |
| How each member voted, by party | LIS vote file, https://lis.blob.core.windows.net/lisfiles/20242/VOTE.CSV (SHA-256 `d6ed56a8...c3aee2e0`), and member file, https://lis.blob.core.windows.net/lisfiles/20242/Members.csv (SHA-256 `aa37d58a...b317e90`), joined by script to DOME's party for 2025 | Vote 2429597 lists 99 members: 51 "Y", all Democrats; 42 "N", all Republicans; 6 "X" (not voting), all Republicans. LIS lists one member as "Ellen H. Campbell"; DOME lists district 36's member, a Republican serving since 2023, as "Ellen H. McLaughlin". I treated them as the same person, because no other Campbell or McLaughlin appears in DOME's 2025 list |

### The Senate on October 31, 2025

The round 2 notes counted today's Senate, 21 Democrats and 19 Republicans. Two senators who voted in October 2025 have since left, so I checked the October vote member by member.

| Fact | Source, URL | What the source says |
|---|---|---|
| How each senator voted, by party | LIS vote SV90 (same files as above), joined by script to the "Party:" field of the Senate's member directory, https://apps.senate.virginia.gov/Senator/index.php | 40 senators in the vote. 21 "Y": 19 are listed today as "Party: Democrat", and the other two, Adam P. Ebbin and Ghazala F. Hashmi, no longer serve. 16 "N" and 3 "X": all 19 are listed as "Party: Republican" |
| Ebbin's party | Virginia Department of Elections, Elections Database, candidate page, https://historical.elections.virginia.gov/candidate/13649 | "Adam Paul Ebbin", "Democratic"; his 2023 general election opponent is listed as Sophia C. Moshasha |
| Hashmi's party | Same database, 2025 Lieutenant Governor contest, https://historical.elections.virginia.gov/contest/164997 | "Ghazala F. Hashmi", "Democratic" |

So the Senate that gave the first passage had 21 Democrats and 19 Republicans, and its 21 yes votes were all Democrats'.

**Verdict: holds.** Democrats held majorities in both chambers at both passages: House 51 to 48 with one seat vacant and Senate 21 to 19 in October 2025; House 64 to 36 and Senate 21 to 19 in January 2026. In the first passage every yes vote came from a Democrat, and the Supreme Court of Virginia calls both passages party-line votes. "Democratic-led legislature" is accurate for both. No wording change.

URLs checked November 10, 2026.

## 2. Tangipa v. Newsom, order of January 14, 2026

**Claim as printed (California's source line):** "Tangipa v. Newsom, U.S. District Court for the Central District of California, order of January 14, 2026"

| Fact | Source, URL | What the source says |
|---|---|---|
| Case name, court, number, document and filing date | The order itself, reproduced at App. 1 to App. 117 of the applicants' appendix in Supreme Court No. 25A839, https://www.supremecourt.gov/DocketPDF/25/25A839/392124/20260120125033680_20260120_SCOTUS_Appendix%201_FINAL.pdf (SHA-256 `48556b69...7a991abd`). Each page carries the district court's own filing stamp | "Case 2:25-cv-10616-JLS-WLH-KKL Document 216 Filed 01/14/26 Page 1 of 117". Caption: "UNITED STATES DISTRICT COURT CENTRAL DISTRICT OF CALIFORNIA", "DAVID TANGIPA, et al., Plaintiffs, and UNITED STATES OF AMERICA, Plaintiff-Intervenor, v. GAVIN NEWSOM, in his official capacity as the Governor of California, et al., Defendants" |
| The panel | Same | "Before: Hon. Josephine L. Staton, Hon. Wesley L. Hsu, Hon. Kenneth K. Lee", "Opinion by Judge Staton", "Dissent by Judge Lee". The opinion calls the panel "This three-judge panel" |
| What the order did | Same, title and conclusion | Title: "ORDER DENYING PLAINTIFFS’ MOTION FOR PRELIMINARY INJUNCTION (Doc. 15) AND DENYING PLAINTIFF-INTERVENOR’S MOTION FOR PRELIMINARY INJUNCTION (Doc. 29)". Conclusion, page 70: "For the foregoing reasons, the Court DENIES Challengers’ Motions for Preliminary Injunction." |
| What the plate takes from it | Same, page 2 | "The stated goal of the ERRA was to counter the actions of Texas and pick up an additional five Democratic seats." The opinion also refers to "the Democratic supermajority in the California state legislature" |
| What followed | Same appendix, App. 131: Document 220, "Filed 01/16/26". Supreme Court, Order List, "WEDNESDAY, FEBRUARY 4, 2026", https://www.supremecourt.gov/orders/courtorders/020426zr_3eb4.pdf (SHA-256 `64698442...b5b8767`) | The district court: "A majority of the Court having so voted, Plaintiffs’ application for an injunction pending appeal, Doc. 218, is DENIED. DATED: January 16, 2026". The Supreme Court, in "25A839 TANGIPA, DAVID, ET AL. V. NEWSOM, GOV. OF CA, ET AL.": "The application for writ of injunction pending appeal presented to Justice Kagan and by her referred to the Court is denied." |
| Lower court as the Supreme Court records it | Supreme Court docket, No. 25A839, https://www.supremecourt.gov/search.aspx?filename=/docket/docketfiles/html/public/25a839.html | "Lower Ct: United States District Court for the Central District of California", "Case Numbers: (2:25-cv-10616)" |

Where the record comes from: the copy I read is the court's filed document, stamp and all, as a party reproduced it in a Supreme Court filing. I did not read it on the district court's own docket (PACER) or on cacd.uscourts.gov. A search limited to cacd.uscourts.gov returned a court calendar entry for "CV 25-10616-JLS-WLH-KKL: David Tangipa, et al. v. Gavin Newsom, et al." (snippet only, official domain; I did not open it).

**Verdict: holds.** The case name, court and date are right, and the order denied both motions for a preliminary injunction against the Proposition 50 map. No wording change. The case number is No. 2:25-cv-10616 if the editor ever wants it, but the plate's other sources carry no case or docket numbers, so I propose none.

URLs checked November 10, 2026.

## 3. Ohio's commission minutes

**Claim as printed (How we counted):** "Ohio’s redistricting commission, five Republicans and two Democrats, adopted its map 7 to 0 on October 31, 2025, the deadline the state constitution set, and the constitution required at least two votes from each party’s members."

| Fact on the plate | Source, URL | What the source says |
|---|---|---|
| "adopted its map 7 to 0" | Ohio Redistricting Commission, "Unapproved Minutes-October 31, 2025" (document 1256), https://www.redistricting.ohio.gov/api/documents/1256/download (SHA-256 `2ffdd4c2...1bafa1ab05f1`, the same file the round 2 notes read) | "E. Motion to adopt proposed Congressional redistricting plan. Co-Chair Stewart moved that the Ohio Redistricting Commission adopt the Congressional redistricting plan that he presented to the Commission and which was uploaded on the Ohio Redistricting Commission’s website by Commission Staff on October 30, 2025, as the Congressional redistricting plan for the State of Ohio. Senator Timken seconded. By a vote of 7-0, the motion passed." Also "Members Absent: None" |
| The roll call | Commission transcript, "Ohio Redistricting Commission Transcript - October 31, 2025" (document 1255), https://www.redistricting.ohio.gov/api/documents/1255/download (SHA-256 `f6798b8b...52249791`) | "Yes" from Antonio, Stewart, DeWine, LaRose, Faber, Timken and Isaacsohn, in that order. Staff then: "Having received a unanimous vote by members of the Ohio Redistricting Commission, as well as two affirmative votes from members of each of the two largest political parties in the Ohio General Assembly, as required by Article 19, Section 1E of the Ohio Constitution, the congressional district plan for the state of Ohio is adopted and will remain effective until the year 2031." |
| "on October 31, 2025" | Minutes heading | "MINUTES – OCTOBER 31, 2025 AT 10:00 AM" |
| "the deadline the state constitution set" | Ohio Constitution, Article XIX, Section 1(E), "Effective: January 1, 2021", Ohio Laws and Administrative Rules, https://codes.ohio.gov/ohio-constitution/section-19.1 (SHA-256 `d06727a7...0826078`) | The commission "shall adopt a congressional district plan not later than the last day of October of that year". The commission's convening notice (document 1046, SHA-256 `851f71ba...86d4ae7d`) cites "Article XI, Section 1 and Article XIX, Section 1 of the Ohio Constitution", and the transcript cites "Article 19, Section 1E" |
| "required at least two votes from each party’s members" | Same section, 1(E) | "by the affirmative vote of four members of the commission, including at least two members of the commission who represent each of the two largest political parties represented in the general assembly" |
| "five Republicans and two Democrats" | The commission's member data, https://www.redistricting.ohio.gov/api/members (SHA-256 `c3442e47...c230e7f1`), gives each member's title but no party. Party comes from the Ohio House directory, https://ohiohouse.gov/members/directory, and the Ohio Senate directory, https://ohiosenate.gov/members, read through the fetch tool, which summarizes; and from the Supreme Court of Ohio, 2022-Ohio-65, paragraph 10, https://www.supremecourt.ohio.gov/rod/docs/pdf/0/2022/2022-Ohio-65.pdf (SHA-256 `d3355d2d...b817f265`) | Fetch tool: Stewart "District 12", "R"; Isaacsohn "District 24", "D"; Timken "District 29 \| R"; Antonio "District 23 \| D". The court: "Governor Mike DeWine, Secretary of State Frank LaRose, Auditor of State Keith Faber ... who are members of the Republican party". The October 31, 2025 minutes list the same three officers as members. That makes five Republicans and two Democrats |

Two points on the record itself. The commission posts the October 31 minutes as "Unapproved Minutes". Its meetings data (https://www.redistricting.ohio.gov/api/meetings) lists no meeting after October 31, 2025, so no later meeting has approved them. The file the commission labels "Minutes" under the October 31 meeting (document 1241) holds the October 30 minutes, which the commission approved on October 31 ("Without objection, the minutes were approved").

**Verdict: holds.** Each fact matches the commission's minutes and transcript and Article XIX, Section 1(E). The plate's "at least two votes from each party’s members" shortens the constitution's "at least two members ... who represent each of the two largest political parties" accurately, since only two parties sit on the commission. No wording change.

URLs checked November 10, 2026.

## 4. Missouri, status only

I made one attempt, as asked. The fetch tool read the Secretary of State's results page, https://www.sos.mo.gov/elections/results, and reported one results link under "General Election - November 3, 2026": "View Unofficial Results", which points to the election night reporting site. The only other November 2026 link is "Certified Candidates - November 2026", a candidate list. Nothing certified or official is posted for November 3, 2026. I did not try to read any results. The plate's Missouri wording stays until the certified statement comes out, as D2-838 set.

Checked November 10, 2026.

## Proposed plate wording changes

None. All three carried claims hold as printed.

## Decisions

- D2-xxx | Virginia's sentence stays: "Democratic-led legislature" holds for both passages | The 2025 House had 51 Democrats to 48 Republicans and the Senate 21 to 19; every first-passage yes vote was a Democrat's; round 2 checked the 2026 counts
- D2-xxx | The 2025 House's party comes from the House Clerk's history pages (DOME), session by session | The current member cards show only the 2026 House; DOME records party for each session a member served
- D2-xxx | LIS's published data files (HISTORY.CSV, VOTE.CSV, Members.csv) count as the LIS vote record | LIS's bill and minutes pages load by script; its Learning Center documents these files as its public data; they agree with the House's own minutes on the House vote
- D2-xxx | The Senate's October 2025 makeup is read member by member from the vote, not assumed from today's roster | Two senators who voted have since left; their parties come from the Department of Elections' database
- D2-xxx | Tangipa v. Newsom's citation stays as printed | The order's own stamp reads "Filed 01/14/26" in the Central District of California, and the Supreme Court's docket names the same court and case number
- D2-xxx | The supremecourt.gov copy of the order counts as a primary record | It reproduces the district court's filed document with its filing stamp on every page; PACER needs a login, and courtlistener answers 403
- D2-xxx | Ohio's note stays as printed | The minutes, transcript and Article XIX, Section 1(E) support each fact
- D2-xxx | Ohio's party split keeps its two sources: the 2022 Supreme Court of Ohio opinion for the three statewide officers and the legislatures' directories for the four legislators | The commission's own member data gives titles and no party; I did not retry ohiosos.gov, which blocked the round 2 attempt
- D2-xxx | Missouri stays as printed | The Secretary of State posts only "View Unofficial Results" for November 3, 2026; certification follows the November 17 county deadline (D2-838)

## Tested

- Virginia: downloaded and read the enrolled HJ6007ER PDF; the House's October 29, 2025 minutes; LIS's 2024 Special Session I HISTORY.CSV, VOTE.CSV and Members.csv, and the 2026 HISTORY.CSV, reading the HJ6007 and HJ4 rows. Downloaded DOME's 2025 member list and all 100 member pages and counted party for 2025 by script (51 Democrats, 49 Republicans). Checked every 2025 member's "Sessions Served" line by script for departures during 2025 (only Gilbert, July 14, 2025). Read district 33 in DOME's 2026 list. Joined both first-passage votes to party by script and tallied the Y, N and X codes by script (House 51, 42, 6; Senate 21, 16, 3). Read Ebbin's candidate page and the 2025 Lieutenant Governor contest page in the Department of Elections' database. Read the Supreme Court of Virginia's May 8, 2026 opinion where it describes both votes.
- Tangipa: downloaded the 323-page appendix from supremecourt.gov and read the order's caption, filing stamps, introduction, panel, conclusion and the January 16, 2026 order; searched it for the five-seat and supermajority language. Read the Supreme Court's February 4, 2026 order list and the 25A839 docket page.
- Ohio: downloaded the commission's meetings and members data, the October 31 unapproved minutes, the October 31 transcript, the October 31 agenda, the files labeled "Minutes" under the October 30 and 31 meetings (the October 21 and October 30 minutes), and the October 21 convening notice. Four file hashes match the round 2 notes (documents 1046, 1255 and 1256, and 2022-Ohio-65). Read Article XIX, Section 1 on codes.ohio.gov, divisions (C)(3)(e), (D) and (E), and paragraph 10 of 2022-Ohio-65. Read the four legislators' party labels through the fetch tool.
- Missouri: one fetch-tool read of the Secretary of State's results page.

## Not tested

- LIS's rendered pages for HJ6007 and the Senate's October 31, 2025 minutes: both load by script, and the fetch tool returned only the page shell. The Senate vote rests on LIS's data files and the enrolled text's date, not on a rendered LIS page or the Senate's minutes.
- The party breakdown of the January 2026 votes on HJ4, member by member. I rely on round 2's 2026 counts and the Supreme Court of Virginia's "party-line vote".
- The party of the 19 sitting senators on a list dated October 2025: I used today's directory and did not check for a party change in between.
- That "Ellen H. Campbell" in LIS and "Ellen H. McLaughlin" in DOME are one person, beyond district and name: I matched on the shared first name and middle initial, the absence of any other match, and DOME's district 36 entry.
- The Tangipa order on the district court's own docket (PACER) or on cacd.uscourts.gov. The cacd.uscourts.gov calendar entry is a search snippet I did not open. I did not try courtlistener.com, given its 403.
- The four Ohio legislators' member pages in raw form: the fetch tool summarized them. The statewide officers' party on a 2025 record: the court opinion dates from 2022, and I did not try ohiosos.gov.
- Missouri's certified result: not issued, and not attempted beyond one read of the results page.

## Change log

Files created:

- `work/handoffs/phase-2/20261110_Carried-Source-Checks-Notes.md` (this file).

Files modified: none. No chapter, specimen, generator, ledger, board or source file was touched.

Scratch only, outside the project, in `/tmp/claude-0/-home-user-Dustin-s-Command-Center/67af6aec-b8e0-5b79-b000-c172e734e753/scratchpad/`:

- `research/`, one new folder per download or download batch: `va-lis-1`, `va-legacy-1`, `va-history-1` to `va-history-4`, `va-history-members`, `va-enrolled-1`, `va-ihod-1`, `va-house-minutes-1`, `va-house-minutes-2`, `va-senate-1`, `va-senate-2`, `va-pubs-1`, `va-scv-1`, `va-lis-csv-1` to `va-lis-csv-5`, `va-elections-1` to `va-elections-3`, `tangipa-scotus-1`, `tangipa-scotus-2`, `ohio-orc-1`, `ohio-orc-docs-1` to `ohio-orc-docs-3`, `ohio-orc-members-1`, `ohio-scoh-1`, `ohio-const-1`.
- `scripts/`: `va_party.py`, `va_vote_party.py`, `va_senate_vote.py`, each run with `python3 -I`.
