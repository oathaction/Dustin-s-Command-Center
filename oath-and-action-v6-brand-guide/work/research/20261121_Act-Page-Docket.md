# The Act page's docket: commenting on a proposed federal rule

Written November 21, 2026 by the main session, chat 11, for chapter 20's example Act page (DR-309: a process piece under Rule 01.22, on a real procedure any reader in any state can use, with a real docket checked and dated). Every fact below was read on November 21, 2026 between 19:00 and 19:20 UTC.

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
