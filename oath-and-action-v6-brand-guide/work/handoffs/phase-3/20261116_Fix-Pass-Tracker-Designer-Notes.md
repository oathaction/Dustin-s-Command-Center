# Fix pass notes: tracker designer, Rules 11.10 and 11.11

Oath & Action Edition 06, Phase 3, the fix pass after the review of rounds 4 and 5, chat 7, November 16, 2026. Written by the tracker designer (a general-purpose agent briefed as the designer who drew chapter 11's trackers) for `work/handoffs/phase-3/20261116_Rounds-4-5-Fix-Brief.md`, calls 4 and 5. Paths are relative to `oath-and-action-v6-brand-guide/`. Files I write: `work/build/scripts/phase-2/apply_systems_ch11.py`, `apply_systems_ch11_ui.py` and their outputs.

## Status

17:00 UTC. Started. Read CLAUDE.md, the fix brief whole, CE-S11, CE-S15 to CE-S21, ST-S3 and NB-S7 in their reports, and my round 5 notes. Working order: call 4 (CE-S20) and call 5 (CE-S18) first, which need neither facts nor words; then the rest as the research lead's "Facts" and the editor's "Words for the tracker designer" land.

17:02 UTC. **Calls 4 and 5 done in Rule 11.11 (CE-S20, CE-S18).** Rerun, second run changed no file, strict build `guide1.html` exit 0, 0 warnings, 369 rules. Only `11-icons.json` moved among my outputs (Rule 11.11's text and specs); no plate changed. Waiting on: the research lead's facts for ST-S3, CE-S17 and NB-S7, and the editor's words for CE-S11, CE-S15 to CE-S17, CE-S19 and CE-S21 (17:02: neither posted).

## Fixed

| Code | What changed | File | Proof |
|---|---|---|---|
| CE-S20 (call 4) | Rule 11.11 gains a third paragraph: a ruling no one appeals keeps the steps after it under slashes once the time to appeal has passed, as Rule 11.8 does for a request; a case decided at trial and never appealed keeps steps 3 to 6 under slashes; a case no one takes to the Supreme Court keeps steps 5 and 6 under slashes. The square's sentence now names its cases: settlement, dismissal or a denied petition. Specs: "Never appealed" was "A square on step 2" and is now "Steps 3 to 6 under slashes once the time to appeal has passed, with the trial court's ruling and “No appeal was filed in the 30 days the law allows.”, or 60 days where the United States is a party", with the slash token; a new row "No petition" (steps 5 and 6 under slashes, with the appeals court's ruling); "Ended before step 6" is relabeled "Settled, dismissed or denied", since an unappealed case also ends before step 6. Draft words, for the editor's second read. No plate changes: the three cases on the correct plate stay one current, one decided, one stopped (DR-275), and no card was unappealed | `apply_systems_ch11.py` (Rule 11.11), output `11-icons.json` | Rerun 17:02, exit 0; second run changed no file (hashes); strict `guide1.html` exit 0, 0 warnings |
| CE-S18 (call 5) | Rule 11.11's text: "joined to “and sent back”, which the court enters as remanded, when it returns the case." The card keeps "Reversed and sent back by the Supreme Court on June 2." | `apply_systems_ch11.py`, output `11-icons.json` | As above |

## Not fixed

| Code | Reason |
|---|---|

## Calls

| call | reason |
|---|---|
| A ruling no one appeals keeps the steps after it under slashes, at the trial court (steps 3 to 6) and at the appeals court (steps 5 and 6); the square stays for settlement, dismissal and a denied petition | Call 4 names the trial court; the same reason holds one court up, and leaving the unpetitioned appeals ruling to the old square would keep CE-S20's two marks for one kind of end. Data lead: please confirm in your sign-off |
| "No petition" names no day count | The 90 days of Supreme Court Rule 13.1 and 28 U.S.C. 2101(c) can be extended by a justice for up to 60 days (workflow sources file, step 5 row), so a fixed count would be wrong for some cases; the trial court row keeps its 30 and 60 days as approved |

## Requests

## Tested

## Not tested
