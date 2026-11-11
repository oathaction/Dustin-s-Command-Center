# Gate 2 red team: drift across the 16 chapters

Oath & Action Edition 06, Phase 2, November 11, 2026. Task 2 of `20261111_Gate-2-Brief.md` (DR-226). Reviewer: the design director's eye, as a reviewer, with the editor's eye for words. Page read: the frozen page at `scratchpad/gate-2/review/guide.html` (16 chapters, 185 rules, 424 specimens).

Status: in progress. Findings are added as the checks run.

## Score

(pending)

## Must fix

(pending)

## Should fix

(pending)

## Questions for Dustin

(pending)

## Tested

Interim notes, written as checks finish (the container can restart).

- Every "Rule NN.N" in the page's words, captions, aria labels and link texts, 1,929 mentions of all 185 rules, by script (`drift/xref.py`): every one names a rule that exists, in one form (two-digit chapter, no stray formats). All 1,135 rule links land on a rule whose number matches the link's words. No same-page link is dead.
- 351 distinct sentences that cite a rule in another chapter, each printed beside its target's title and read (`drift/xsent.json`), with the full text of eighteen targets read against the claim.
- Every contrast ratio the page prints (528 instances, 84 values) against WCAG 2.2's formula on the token colors (`drift/ratioscan.py`).
- Atlas V7 IDs: 78 distinct typed IDs (loops, reforms, variables) all exist in `atlas-v7-data.json`; the 50 reform names in chapter 10 match the atlas titles except DR-185's two settled short names and a typographic apostrophe.
- Chapter 19's 55 criteria against `20261111_WCAG22-Criteria-Text.json`: number, name, level and the first 150 characters of every criterion's words match; 31 at A, 24 at AA, six new; statuses 33, 8, 9, 5.
- Rule 10.4's list of 41 against `civic-line-v6/fit-24/`: 37 fit files plus the four pillar icons; each contact sheet's "Also at 24 px" count (7, 7, 11, 9, 3) adds to 37.

## Not tested

(pending)

## Routine calls

(pending)
