# Chat 11c editor notes

Editor, chat 11c, November 22, 2026. Brief: `work/handoffs/phase-4/20261122_Chat-11c-Brief.md`, section 6.1. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/e76584b2-1bba-5266-a75e-730f247433d8/scratchpad/c11c/editor/`. Started 21:48:24 UTC (`date -u`); notes opened 21:49:11 UTC.

Read first: my role file; `CLAUDE.md`; chapter 02's writing rules; the decision log from line 7342 to its end (D4-100 to D4-241, DR-305 to DR-325); chapter 21's plan, sections 1 to 13; Master Brief sections 3, 8, 15 and 23; chat 11b's editor notes for the identity chain's side effects (D4-222).

## Routine calls

- D4-xxx | DR-323 ran `phase3_ch13_build.py` alone, with no run of `phase3_ch14_build.py` | Chapter 14's build reads its own plan, entries and specs and never `13-evidence.json`, so chapter 13's assembly does not need it; `phase3_ch14_build.py --check` reads 99 of 99 files current after the change
- D4-xxx | The identity chain for DR-324 and DR-325 rewrote the same five files beyond chapter 03 that D4-222 names, and all five went back to their prior bytes from my scratch copies taken before the run: `s-04-1-correct`, `s-09-3-correct`, `s-09-3-failure`, `s-17-hinge-failure` and `work/boards/phase-2/stage-a/proofs/20261110_Letterhead-Proof.html` | They grew 72 to 10,108 bytes in the run (8,670 to 8,742; 9,728 to 9,912; 6,799 to 6,959; 14,823 to 16,063; 105,999 to 116,107), as in chat 11b, and DR-324 and DR-325 name Rule 03.6 alone. Each restored file now equals HEAD (`git diff --quiet`), and the rewritten copies sit in scratch, `identity-run-side-effects/`
- D4-xxx | Rule 03.6's correct plate keeps its label "Phone, 390 px: L1 from the 24 px master" | A 390 px window is 24.375em at the default text size, so it falls in the row "Site, from 24.375em to 48em", and D4-115 keeps the 24 px master at 390 px; the plate and the new words agree

## Rulings

None of my own; I follow the data visualization lead's and the design director's as they land.

## Words for

Chapter 21's words, drafted here until the design director hands the generator's word fields over by name (brief 6.1 step 6). Not started.

## Done

Each time below is a `date -u` value read in the same command.

### A done (DR-323, DR-324, DR-325), 21:51 UTC

1. **DR-323**, Rule 13.12's rule text, second paragraph: `work/build/scripts/phase-3/phase3_ch13_build.py` (the block at line 1716), comment `# DR-323 (ED11B-1)`. Run under the lock 21:50:03 UTC; its own checks passed and it wrote `13-evidence.json`, its 27 specimens and manifest, of which only `13-evidence.json` changed.
   - Original: "An Act piece quotes each side at the same length (Rule 01.22), and an invented quote carries the Illustrative label beside it (Rule 13.8)."
   - Revision: "An Act piece sets out what the record shows from each side, at the length the record holds (Rule 01.22), and an invented quote carries the Illustrative label beside it (Rule 13.8)."
   - `phase3_ch14_build.py --check` under the lock, 21:50:07 UTC: "99 of 99 files current", exit 0.
2. **DR-324**, Rule 03.6: `work/build/scripts/phase-2/stage_a_identity_chapters.py`, comment `# DR-324 (ED11B-2)` above the rule text and above the row.
   - Rule text, original: "Under 48em, it sets L1 from the 24 px master beside the menu button."
   - Rule text, revision: "Under 48em, it sets L1 from the 24 px master beside the menu button, and under 24.375em, 390 px, from the 16 px master."
   - Row label, original: "Site, under 48em"; revision: "Site, from 24.375em to 48em". Its value and token stay.
3. **DR-325**, Rule 03.6's `files=`: `A + "wordmark/20261028_Wordmark-16px-Master.svg"` after the 24 px master, comment `# DR-325 (ED11B-3)`. The file exists at `work/build/assets/identity/wordmark/20261028_Wordmark-16px-Master.svg`.
4. **The identity chain's side effects (C11B-1, D4-222).** Copied the five files to scratch `before-identity-run/` with their SHA-256 (21:49:26 UTC), ran `stage_a_identity_build.py` under the lock (21:50:26 to 21:50:37 UTC, exit 0: 73 specimens, chapters 03, 04, 08 and 09), and the run rewrote all five. I put back all five from my copies (21:50:44 UTC): `s-04-1-correct`, `s-09-3-correct`, `s-09-3-failure`, `s-17-hinge-failure` and `20261110_Letterhead-Proof.html`. Each now equals HEAD. Chapters 04, 08 and 09, every other specimen and `manifest-identity.json` kept their bytes.
5. **Proof.**
   - Strict build after, under the lock (21:50:52 to 21:51:03 UTC): exit 0, 0 warnings, 0 stale plates, 13,084,029 bytes, 393 rules, 731 specimens. The before build (21:49:31 to 21:49:42 UTC, same tree less my four files) gave exit 0, 0 warnings, 13,083,858 bytes, the opening figure.
   - Word search of the built HTML (tags and `<wbr>` stripped, no-break spaces read as spaces), before → after: Rule 13.12's new phrase 0 → 1, in Rule 13.12 only; "An Act piece quotes each side at the same length" 1 → 0 on the page. Rule 03.6's new sentence 0 → 1, in Rule 03.6 only; the old sentence 1 → 0. "Site, from 24.375em to 48em" 0 → 1, in Rule 03.6; "Site, under 48em" 1 → 0 on the page. `20261028_Wordmark-16px-Master.svg` 4 → 5, the new one in Rule 03.6's file list (the others sit in Rules 03.1, 03.8, 05.3 and 05.7, as before).
   - A line diff of the two pages shows these four places and the build-time line, nothing else.
   - `git diff --stat` after the restore: `03-identity.json` (5), `13-evidence.json` (2), `stage_a_identity_chapters.py` (10), `phase3_ch13_build.py` (5); four files, 14 insertions, 8 deletions. Nothing else in the tree moved.

| Chapter | JSON file before | after | Section of the built page before | after |
|---|---|---|---|---|
| 03 Identity | 27,118 | 27,259 (+141) | 463,108 | 463,237 (+129) |
| 13 Evidence | 45,531 | 45,573 (+42) | 243,027 | 243,069 (+42) |

The page grew 171 bytes, 13,083,858 to 13,084,029, all of it in chapters 03 and 13 (the build report's per-chapter figures; no other chapter moved).

## Requests

None yet.

## Not fixed

| Code | Source | Where | What is wrong | Suggested fix | Why not made | Status |
|---|---|---|---|---|---|---|

## Tested

- Strict build before and after, under the lock, with the figures under "A done".
- `phase3_ch14_build.py --check`, 99 of 99.
- Word search of both built pages for the old and new phrases, by rule block (scratch `wordsearch.py`).
- A line diff of the two built pages (split at each `>`).
- `git diff --stat` and `git status --short` after the restore; each of the five restored files against HEAD with `git diff --quiet`, and my scratch copies against their SHA-256.
- A search of the after page for "same length", "under 48em" and the 24 px master near "phone", "390" or "menu": no other rule says an Act piece quotes each side at the same length, and Rule 20.1's "under 48em the bar sets L1" names no master, so nothing else contradicts the new words.
- Script check of the three new texts and this file for em dashes and the listed words (genuinely, really, truly, actually, leverage, underscore, reflect, very, just, simply): 0.

## Not tested

- The guide check, which the main session runs at the close.
- Whether the five rewritten side-effect files differ in pixels from their originals; I put the originals back, so nothing new ships.
