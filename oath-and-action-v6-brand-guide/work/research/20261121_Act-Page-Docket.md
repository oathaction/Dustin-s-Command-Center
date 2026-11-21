# The Act page's docket: commenting on a proposed federal rule

Written November 21, 2026 by the main session, chat 11, for chapter 20's example Act page (DR-309: a process piece under Rule 01.22, on a real procedure any reader in any state can use, with a real docket checked and dated). Every fact below was read on November 21, 2026 between 18:52 and 18:56 UTC.

## How the docket was chosen

The Federal Register's public API (`https://www.federalregister.gov/api/v1/documents.json`, no key) listed 110 proposed rules published from November 1, 2026. The main session chose one that meets four tests:
1. Comments are open well past the guide's next boards (open until January 19, 2027).
2. Comments go through Regulations.gov, the portal most agencies use, so the steps teach the common route.
3. The subject touches readers on every side and is not a fight between parties: whether a common supplement may be sold as a dietary supplement.
4. It is a rule an ordinary reader can follow from its summary.

Others weighed and set aside: the FCC's Internet of Things labeling notice (comments go through the FCC's own system, so its steps would not teach the common route); airspace and airworthiness notices (too narrow for a general reader); several rules on contested subjects where the example would read as taking a side.

## The rule

| Field | Value | Source |
|---|---|---|
| Title | Rulemaking To Provide That N-acetyl-L-cysteine Is Not Excluded From the Dietary Supplement Definition | Federal Register API, document 2026-23351 |
| Agency | Food and Drug Administration (FDA), Department of Health and Human Services | Same |
| Action | Proposed rule | Same |
| Docket | FDA-2025-N-2699 | Same |
| RIN | 0910-AI91 | Same |
| Citation | 91 FR 73717 (21 CFR Part 190) | Same |
| Published | November 17, 2026 | Same |
| Comments close | January 19, 2027; the Regulations.gov system takes comments until 11:59 p.m. Eastern Time that day; mailed or delivered paper comments count if received on or before that date | Same; the rule's ADDRESSES section, read from govinfo's PDF |
| Where to comment | https://www.regulations.gov/commenton/FDA-2025-N-2699-0001 | Federal Register API, `comment_url` |
| The rule's page | https://www.federalregister.gov/documents/2026/11/17/2026-23351/rulemaking-to-provide-that-n-acetyl-l-cysteine-is-not-excluded-from-the-dietary-supplement | Federal Register API, `html_url` |
| Official PDF | https://www.govinfo.gov/content/pkg/FR-2026-11-17/pdf/2026-23351.pdf (10 pages, read in full for the ADDRESSES section) | govinfo.gov, HTTP 200 |
| Significant | Yes (the Federal Register marks it significant) | Federal Register API |

**The agency's summary, quoted.** "The Food and Drug Administration (FDA or we) is proposing to issue a regulation finding that N-acetyl-L-cysteine (NAC) is not excluded from the dietary supplement definition in the Federal Food, Drug, and Cosmetic Act (FD&C Act). This action, if finalized, would allow products containing NAC to be lawfully marketed as dietary supplements, provided that such products are not otherwise in violation of the FD&C Act."

## How to comment, from the rule's ADDRESSES section

- **Online:** the Federal eRulemaking Portal, https://www.regulations.gov. "Follow the instructions for submitting comments."
- **What becomes public:** "Comments submitted electronically, including attachments, to https://www.regulations.gov will be posted to the docket unchanged." The rule warns against including "medical information, your or anyone else’s Social Security number, or confidential business information", and says a name or contact information in the body of a comment "will be posted".
- **By mail, hand delivery or courier:** Dockets Management Staff (HFA-305), Food and Drug Administration, 5630 Fishers Lane, Rm. 1061, Rockville, MD 20852.
- **Every submission** "must include the Docket No. FDA-2025-N-2699".
- **Confidential information:** paper only, two copies, one marked "THIS DOCUMENT CONTAINS CONFIDENTIAL INFORMATION" and one with that information blacked out.
- **Reading other comments:** received comments are "publicly viewable at https://www.regulations.gov or at the Dockets Management Staff between 9 a.m. and 4 p.m., Monday through Friday, 240-402-7500."

## What could not be checked

- Regulations.gov answers automated readers with 403 (its own bot check, as V10 found), so the comment form's fields were not read; the page says only what the rule's own text says about it.
- The Federal Register's full-text web page asks automated readers for a captcha; its API and govinfo's PDF of the same document were read instead.

## For the page

A process piece leaves the side to the reader (Rule 01.22): the page explains what the rule would do, who decides, by when, and how a comment is made and read, and asks the reader for nothing but taking part if they choose. The one way to take part is the link to the comment page (Rule 11.4, the one working red). Print the docket number, the close date with its time zone, the rule's citation and "checked November 21, 2026" on the page.

## Added 20:17 to 20:19 UTC: answers to the design director’s R3 and R5

Read by the main session from two primary sources: H.R. 7008's bill status file on govinfo (`https://www.govinfo.gov/bulkdata/BILLSTATUS/119/hr/BILLSTATUS-119hr7008.xml`, HTTP 200, updated October 1, 2026) and the rule's own text in govinfo's PDF, page by page (PDF pages 1 to 10 are Federal Register pages 73717 to 73726).

### R3 (a) and (b): H.R. 7008's committee steps

| Date | Step | Source |
|---|---|---|
| January 12, 2026 | Introduced; referred to the House Committee on House Administration | Bill status, actions |
| January 14, 2026 | Committee consideration and markup session held; ordered to be reported (amended) by the yeas and nays, 7 to 4 | Same |
| February 3, 2026 | Reported (amended) by the Committee on House Administration, H. Rept. 119-479; placed on the Union Calendar, Calendar No. 409 | Same |
| July 22, 2026 | Passed the House 232 to 198 (roll no. 280), after a motion to recommit failed 211 to 218 (roll no. 279) | Same; research ledger P7-019 |
| September 30, 2026 | Cloture on the Senate's motion to proceed not invoked, 53 to 47 (record vote 253) | Same; P7-019 |

**(a) Hearing.** The bill status file lists no committee hearing for H.R. 7008: the committee's activities are "Referred To", "Markup By" and "Reported By" only. Print the step as a markup, never as a hearing.
**(b) Committee vote.** Yes: 7 to 4 on January 14, 2026, to report the bill as amended.

### R3 (c): an advance notice before the proposed rule?

The rule's background (II.B, pages 73719 to 73720) and its section IV.B (pages 73722 to 73723) name no advance notice of proposed rulemaking. The steps the rule itself records are:

| Date | Step | Page |
|---|---|---|
| 2001, 2010 and July 2020 | FDA states that NAC-containing products are excluded from the dietary supplement definition (a 2001 response to a health claim petition; a 2010 response to an NDI notification; July 2020 warning letters to companies selling hangover products labeled as supplements) | 73719 to 73720 |
| 2021 | Two citizen petitions ask FDA to conclude that NAC is not excluded (dockets FDA-2021-P-0523 and FDA-2021-P-0938); one also asks for notice-and-comment rulemaking if FDA keeps its position | 73720 |
| March 31, 2022 | FDA's joint final response denies one petition in full and the other in part, and says it is considering rulemaking | 73720 |
| April 22, 2022 | Draft enforcement discretion guidance (87 FR 24170), with a 30-day comment period; it says FDA was likely to propose such a rule if no safety concern arose | 73723 |
| August 2, 2022 | Final enforcement discretion guidance (87 FR 47220): FDA will not act against certain NAC products labeled as supplements until it completes rulemaking or denies the remaining request | 73720 |
| November 17, 2026 | The proposed rule (91 FR 73717); comments open until January 19, 2027 | 73717 |

So the Act page's step 1 is the 2021 petitions (or the 2022 response), never an advance notice. "Names no advance notice" is what the rule's text shows; a search of the docket on Regulations.gov could not be run (403).

### R5: what the rule reports from each side (Rule 01.22)

- **Those who asked for the change.** "In 2021, we received two citizen petitions requesting that we conclude that NAC is not excluded from the definition of dietary supplement under section 201(ff)(3)(B) of the FD&C Act" (page 73720). The rule does not name the petitioners in the text read.
- **The case against, as the rule states it.** The rule records no objector. It says: "To date, we have not received any comments expressing concern or providing data to demonstrate that allowing the sale of NAC in or as a dietary supplement would impact drug development or identifying any other concerns" (page 73723). The concern the law itself guards is new drug development: the exclusion clause exists in part "to protect the incentives for new drug development" (page 73721), and FDA "invite[s] comment on whether the sale of NAC-containing products labeled as dietary supplements in the United States has negatively impacted NAC drug development or is anticipated to in the future" (page 73723). FDA's own earlier position, from 2001 to 2022, was that NAC is excluded (pages 73719 to 73720).
- **For the page (DR-93).** The record does not hold two sides of equal length. Print what each side has on the record: the petitioners' request, FDA's earlier position with its reason in the law, and the rule's own statement that no comment so far has raised a concern, with the question FDA asks commenters. Do not write an opponents' paragraph the record does not support.
