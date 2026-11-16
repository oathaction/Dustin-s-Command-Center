# Fix pass notes: tracker designer, Rules 11.10 and 11.11

Oath & Action Edition 06, Phase 3, the fix pass after the review of rounds 4 and 5, chat 7, November 16, 2026. Written by the tracker designer (a general-purpose agent briefed as the designer who drew chapter 11's trackers) for `work/handoffs/phase-3/20261116_Rounds-4-5-Fix-Brief.md`, calls 4 and 5. Paths are relative to `oath-and-action-v6-brand-guide/`. Files I write: `work/build/scripts/phase-2/apply_systems_ch11.py`, `apply_systems_ch11_ui.py` and their outputs.

## Status

17:00 UTC. Started. Read CLAUDE.md, the fix brief whole, CE-S11, CE-S15 to CE-S21, ST-S3 and NB-S7 in their reports, and my round 5 notes. Working order: call 4 (CE-S20) and call 5 (CE-S18) first, which need neither facts nor words; then the rest as the research lead's "Facts" and the editor's "Words for the tracker designer" land.

17:02 UTC. **Calls 4 and 5 done in Rule 11.11 (CE-S20, CE-S18).** Rerun, second run changed no file, strict build `guide1.html` exit 0, 0 warnings, 369 rules. Only `11-icons.json` moved among my outputs (Rule 11.11's text and specs); no plate changed. Waiting on: the research lead's facts for ST-S3, CE-S17 and NB-S7, and the editor's words for CE-S11, CE-S15 to CE-S17, CE-S19 and CE-S21 (17:02: neither posted).

17:12 UTC. **The editor's words (17:11) applied, every exact string: CE-S11, CE-S15, CE-S16 with NB-S7's clause, CE-S19, CE-S21 and ST-S3.** Rerun exit 0, second run changed no file, strict build `guide2.html` exit 0, 0 warnings, 369 rules. Moved: `11-icons.json` (Rules 11.10 and 11.11), `s-11-10-correct.html` (Measure 99013's line), `s-11-ballot-steps.html` (step 2's words), and the two matching alts in `manifest-systems.json`. Still waiting: CE-S17 (the editor's row waits on the research lead's fact), and the research lead's confirmation of NB-S7's reason and ST-S3's figure, after which the editor marks those rows final.

17:18 UTC. **CE-S17 applied, in the editor's final words** (on the research lead's F9: Ohio and Massachusetts send a measure the Legislature passes to the governor; Michigan makes it law with no governor). The research lead's F2 and F8 confirm ST-S3's figure and NB-S7's reason, and the editor marked both final, so no string changed for them. Every "New" string in the editor's section prints whole in my outputs (script `check_words.py`; "step 6" holds a no-break space by `nb()`, as every step number does). Rerun exit 0, second run changed no file, strict build `guide3.html` exit 0, 0 warnings, 369 rules. `git diff --stat` on my paths: `11-icons.json` and `apply_systems_ch11.py` only (the main session's snapshots took my earlier moves). Every code routed to me in the brief's table is now applied; my files wait for the editor's second read.

## Fixed

| Code | What changed | File | Proof |
|---|---|---|---|
| CE-S20 (call 4) | Rule 11.11 gains a third paragraph: a ruling no one appeals keeps the steps after it under slashes once the time to appeal has passed, as Rule 11.8 does for a request; a case decided at trial and never appealed keeps steps 3 to 6 under slashes; a case no one takes to the Supreme Court keeps steps 5 and 6 under slashes. The square's sentence now names its cases: settlement, dismissal or a denied petition. Specs: "Never appealed" was "A square on step 2" and is now "Steps 3 to 6 under slashes once the time to appeal has passed, with the trial court's ruling and “No appeal was filed in the 30 days the law allows.”, or 60 days where the United States is a party", with the slash token; a new row "No petition" (steps 5 and 6 under slashes, with the appeals court's ruling); "Ended before step 6" is relabeled "Settled, dismissed or denied", since an unappealed case also ends before step 6. Draft words, for the editor's second read. No plate changes: the three cases on the correct plate stay one current, one decided, one stopped (DR-275), and no card was unappealed | `apply_systems_ch11.py` (Rule 11.11), output `11-icons.json` | Rerun 17:02, exit 0; second run changed no file (hashes); strict `guide1.html` exit 0, 0 warnings |
| CE-S11 (chapter 11) | Rule 11.11 glosses "injunction" at its first use in chapter 11: "an injunction, a court order to do or to stop doing something"; Rule 11.12 and the specs use it bare | `apply_systems_ch11.py`, output `11-icons.json` | Rerun 17:11, second run no change; strict `guide2.html` exit 0, 0 warnings |
| CE-S15 | Step 2's words in the ballot step table: "The attorney general writes the title and summary that petitions and ballots carry, and where the law asks, first certifies that the measure is in proper form and on a subject the initiative may cover." Rule 11.10 glosses "certifies" once: "Until the state certifies the count, which makes the result official, ..." | `apply_systems_ch11.py` (`BALLOT_STEPS`, Rule 11.10), outputs `11-icons.json`, `s-11-ballot-steps.html`, its alt in `manifest-systems.json` | As above |
| CE-S16 | Rule 11.10's first paragraph names a citizen initiative, a legislative referral, and indirect and direct initiatives, and says which steps each keeps under slashes | `apply_systems_ch11.py` (Rule 11.10), output `11-icons.json` | As above |
| NB-S7 | Rule 11.10 names why each state was read: "Massachusetts, Ohio and Michigan, where the Legislature votes first on a proposed law, and California’s constitution and election office, where an initiative goes straight to the ballot"; the ballot table's alt head says the same. The table's visible caption (the `extras` entry after Rule 11.10, which the editor's row did not name: its line 1385 is the alt head) also said "the four states we read", so it takes the same clause: "What happens at each step of a ballot measure, and where the law sets it in four states: Massachusetts, Ohio and Michigan, where the Legislature votes first on a proposed law, and California, where an initiative goes straight to the ballot. Each state sets its own deadlines and signature counts." For the editor's second read (Requests). Confirmed by the research lead's F8 and marked final by the editor (17:20 in their notes) | `apply_systems_ch11.py`, outputs `11-icons.json`, the alt in `manifest-systems.json` | As above |
| CE-S19 | Rule 11.11: "Every ending that leaves a ruling in place says so in one sentence: “The lower court’s ruling stands.” after Affirmed or a tie, and “The appeals court’s ruling stands.” after a denied petition." Spec "A higher court’s ruling" now opens "Affirmed, then “The lower court’s ruling stands.”" | `apply_systems_ch11.py`, output `11-icons.json` | As above |
| CE-S21 | Rule 11.10's spec "The end, in words": "Fell short of the vote the law requires, where most said yes but a second test failed, with a sentence that names the test". No plate prints it | `apply_systems_ch11.py`, output `11-icons.json` | As above |
| ST-S3 | Measure 99013's line: "On July 14, a random sample of the signatures projected fewer than 95 percent of the valid signatures the law requires, so election officials did not go on to check every signature." Confirmed by the research lead's F2 and marked final by the editor | `apply_systems_ch11.py` (`BALLOTS`), outputs `s-11-10-correct.html`, its alt in `manifest-systems.json` | As above |
| CE-S17 | Rule 11.10's last sentence: "A measure the Legislature passes keeps steps 5 and 6 under slashes, and its words give the date and what comes next. In Massachusetts and Ohio it goes to the governor, as a bill does, and in Michigan it becomes law without one: “Passed by the Legislature on May 2. It goes to the governor.”" Spec "Passed by the Legislature": "Steps 5 and 6 under slashes, then “Passed by the Legislature on” with its date and what comes next: “It goes to the governor.”, or “It becomes law without the governor.” where the governor takes no part, as in Michigan". No plate prints it | `apply_systems_ch11.py` (Rule 11.10), output `11-icons.json` | Rerun 17:18, second run no change; strict `guide3.html` exit 0, 0 warnings |
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

### To the editor
1. **Your second read of my words for calls 4 and 5** (Rule 11.11's new third paragraph, the "Never appealed" and "No petition" specs, and the label "Settled, dismissed or denied"), and of the visible caption under the ballot table (NB-S7 row above), which I set in your clause because your row named the alt head. Write corrections as rows here or in your notes; I am not done with the file while CE-S17 waits.

## Tested

## Not tested
