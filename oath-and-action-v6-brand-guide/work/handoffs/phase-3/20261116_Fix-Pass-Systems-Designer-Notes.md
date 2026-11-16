# Fix pass notes: systems designer, chapter 15

Oath & Action Edition 06, Phase 3, the fix pass after the review of rounds 4 and 5, chat 7, November 16, 2026. Written by the systems designer (a general-purpose agent briefed as the designer who drew chapter 15) under `work/handoffs/phase-3/20261116_Rounds-4-5-Fix-Brief.md`. Paths are relative to `oath-and-action-v6-brand-guide/`. My files: `work/build/scripts/phase-3/phase3_ch15_build.py` and what it writes (`15-systems-graphics.json`, `s-15-*`, `manifest-systems-graphics.json`). Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/f55a08bf-cdcf-539d-a683-426e26f4f342/scratchpad/c07/fix/systems-designer/`. Written as I go; the container can restart.

My codes: CE-M2, CE-M3, CE-M4, CE-S1 to CE-S10, CE-S11 (chapter 15's part), CE-S12, CE-S23; ST-M2, ST-S5, ST-S6, ST-S7, ST-S9; DF-1, DF-2, DF-5, DF-8, DF-9, DF-10, DF-11, DF-14; NB-M1 (Rule 15.20's sentence), NB-S5, NB-S6.

## Status

- 17:00 UTC. Started. Read `CLAUDE.md`, the fix brief, the CE, ST, DF and NB reports whole, and my round 4 and round 5 notes. Baseline run of `phase3_ch15_build.py` at `8ace3dc6`: every check passes, 25 rules, 51 plates, and no file of mine changes. The data lead's and research lead's notes are not posted yet; the editor's "Words for the systems designer" is being written. Starting with the items that need no ruling or fact: CE-M2, CE-M4's structure, CE-S6 and DF-11, CE-S7, DF-8, DF-9.

## Fixed

Each in `work/build/scripts/phase-3/phase3_ch15_build.py`; proof is the rerun (every check passes) and a word diff of the plate against `HEAD` (`tdiff.py` in my scratch folder). Words marked "draft" are the reviewer's, applied so the structure could land; the editor's "Words for the systems designer" replace them where they differ.

- **CE-S6, DF-11 (15.22, stage 10's stop line in three columns).** A stop line's words now sit in one span after the mark, so the flex line holds two items, the mark and the words, and the no-wrap span around "two-thirds" no longer becomes a column. The lines that say where a path goes next ("Then stage 13.", "With two-thirds in each, then stage 13.") are plain blocks, no longer flex lines. Words unchanged.
- **CE-M4 (15.22, "Signed" on the line every enacted bill passes).** Stage 9 leaves the spine: it is now the first of the outcomes at the President, a path set to one side with "If the President signs it" and "Then stage 13.", beside stages 10, 11 and 12. The spine runs 1, 2, 6, 7, 8, 13, held by the generator's check, so the key's "A stage every enacted bill passes" and the rule's "the stages every change on the route passes through" read true. On Rule 15.23 stage 9's square under step 6 follows (it draws as a path's square). The key's words wait for the stage mark ruling (call 1, DF-2).
- **CE-M2 (15.23, cloture only under step 4).** Step 5, "Second chamber", now holds stages 3, 4, 5, 6 and 7: suspension, cloture and reconciliation serve either chamber, as Rule 15.22's stages 3 to 5 say ("Then stage 6, or stage 7 ..."; "stage 2 or stage 6"). The generator holds that each of stages 3 to 5 still names stage 6; the alt says step 5 holds stages 3 to 7 and why.
- **CE-M3, DF-1 (15.23, "steps" for the law's stages).** "A federal request’s stages in the law, behind the tracker’s six steps" and "The law’s stages for a federal rule, behind the tracker’s six steps", the reviewers' identical words. A new check fails any block whose subhead calls the law's parts steps before "behind the tracker".
- **CE-S7 (15.23, route IDs bare).** Route FS's and Route BI's block heads print the atlas's name after the chip, as every chip in the chapter does: Route FS “Federal statute”, Route BI “State ballot” (the chip check forbids a comma after a chip, so the reviewer's "Route BI, the state ballot," takes the chapter's form). The source line reads "A state bill follows Route SS, the state statute, the same way". Names read from the atlas.
- **DF-8 (15.24, figures under ten opening sentences).** "Seven reform entries name this route", and six, five, four and three alike; the alt says "one entry, none checked" and "two checked" in words (H06).
- **DF-9 (15.24, Route FS's card names its stages differently from 15.22).** The card's stage run is now read from `fs_stages()` by a new `fs_card_stages()`, in Rule 15.22's names, folded where the card joins stages: "Introduced and sent to committee → Passed by the first chamber, under the usual rules or by suspension of the rules, cloture or reconciliation → Passed by the second chamber, by the same paths → One text for both chambers → Enrolled and presented → Signed, veto and override, law without a signature or pocket veto → Public law → Funded by appropriation, put to work by agency rules, reported to Congress and taken to court → Ended by a sunset, struck down by a court, or repealed or changed". A stage renamed on 15.22 (CE-S3's "Sent to the President", if taken) reaches the card on the next build.
- **CE-S12 (15.21, four effect codes).** Draft: "the three delay classes and the seven effect codes, ranks of direction and rough size with no measured amount". The count is computed and held to the atlas glossary's own list (+L, +M, +S, 0, −S, −M, ?). "Ordinal" is gone from chapter 15's reader text: 15.21's why says "ranked steps", its spec "effect codes", and 15.20's why "the atlas’s own codes, one to each outcome family" (it said "four ordinal codes", which reads as a count of codes).
- **CE-S23 (three small words).** 15.21's spec: "A drawing of the control, with its alt saying it is a picture". The read-aloud line takes "fewer" before a title whose head noun counts (a set of six: Variables C1, C5, D3, E1, X2, X5): Rules 15.1 and 15.6 now read "back to fewer policy advantages for wealthy and organized interests", and Rule 15.15 "fewer incumbents defeated or pushed into retirement". 15.16 glosses "outcome family" at its first use in chapter 15, in chapter 13's words, draft: "then print its effects one outcome family to a row, an outcome family being one of the four groups of results the atlas judges reforms by. Give each row the atlas’s code, its words and the pips of Rule 13.5, and print no row that adds them."
- **ST-S9 (15.25, the drawing tool's habits as fact).** Rows 11 and 17 now say "as our first audit read it in the atlas’s drawing tool" and "our first audit read the atlas’s drawing tool that way"; rows 47, 48 and 52 open "By our reading of October 21, 2026, the atlas’s drawing tool ..." (the date our list of fixes for the atlas read the tool, `work/handoffs/phase-1/20261021_Atlas-V7-1-Issue-List.md`, items 24 to 26). The generator holds the five rows to the sidecar's qualification and fails a row that drops the attribution.
- **ST-S7 (two read dates).** Stage 16 now cites each row its words rest on: "5 U.S.C. 801(a), read November 11, 2026; 5 U.S.C. 801(b), read November 12, 2026" (the disapproval row was already held, and now prints). Rule 15.24's cards may key a row of another route's table; the FA card now reads its 553, 801(a) and 802 rows ("read November 11 and 12, 2026") and the FS card its 706 row ("read November 11, 12 and 14, 2026").
- **DF-10, in part (15.22's source line order).** "Source: Oath & Action’s systems atlas, ..., route FS, its instrument and who acts, snapshot of October 15, 2026, United States. Each stage’s source as named beside it, with the date we read it." The snapshot date no longer reads as the stages' date, as on 15.24.

## Not fixed

## Calls

| call | reason |
|---|---|

## Requests

## Tested

## Not tested
