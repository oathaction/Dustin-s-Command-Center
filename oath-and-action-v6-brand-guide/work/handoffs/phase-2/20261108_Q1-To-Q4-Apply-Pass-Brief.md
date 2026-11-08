# Brief: the small apply pass for the changes board, Q1 to Q4

Oath & Action Edition 06, Phase 2, November 8, 2026. Written by the main session for the identity designer and the editor. Dustin answered the changes board on November 8: "Q1 to Q10 as recommended, and I approve Q1, Q2, Q3, Q5, Q6 and Q7 by name." His answers are DR-129 to DR-138; the studio's calls for this pass are D2-462 to D2-464. This pass closes Q1 to Q4 only. Q5 to Q10 belong to stage B, and nothing in this pass draws for them.

Every rule in `work/handoffs/phase-2/20261107_Apply-Pass-Brief.md` and `20261107_Apply-Pass-Fix-Brief.md` still binds: fixed artboards on the type scale, no studio codes on reader pages, one Illustrative label at the head of a wholly invented piece, the failure band on a failure plate that could pass for our work, true size first, and generated HTML never edited by hand.

## Read first, in this order

1. `CLAUDE.md` and chapter 02's writing section, `work/handoffs/phase-2/20261106_Voice-Writing-Rules.md`. It binds every word you write, in the guide and in your notes. No em dashes.
2. The decision log, `work/ledger/20261020_Decision-Log.md`, from DR-104 to D2-464.
3. The changes board's content, `work/boards/phase-2/apply-pass/20261107_Apply-Pass-Board-Content.json`, keys `decisions` (Q1 to Q4) and `review`.
4. `work/handoffs/phase-2/20261107_CD-Review-Of-Apply-Pass.md` (CD-N8, CD-N9 and the recheck) and `20261107_Apply-Pass-Red-Team-Craft-Access.md` (CA-S1, CA-S2).
5. Your own apply pass notes, with their fix pass section.

## What Dustin decided, binding on everyone

- **L6 (DR-129).** L6 loses its four pillar dots. Its lockmark keeps L6's own proportion. A page narrower than 884 px closes with the footer place.
- **End mark (DR-130).** B stands at the text's cap height, its band (the 16 px master's y 1 to 15) on the capitals, as plate (a) on the board draws it. This is an exception to B's 16 px minimum for the end mark alone. Rule 03.4 gains one line for the exception.
- **48 px lockmark master (DR-131).** The proposal in `work/boards/phase-2/apply-pass/lockmark/20261107_Lockmark-48px-Proposal.svg` becomes a master for the masthead and the sign-off. L3's lockmark is set at 48 px. Rule 08.2 gains the feed test at 500 and 360 px.
- **Rule 01.11's reason (DR-132).** "A case from each party, told the same way, puts a mechanism that both parties use in front of the reader. Where the record shows one side doing more, the finding stands as the record shows it."

## Round one, in parallel

### Identity designer (`.claude/agents/oa-design-director.md`): chapters 03, 04, 08 and the proofs

1. **The 48 px master (DR-131).** Copy the proposal into `work/build/assets/identity/lockmark/20261108_Lockmark-48px-Master.svg` with a clean `<title>`, no board notes, and the drawing otherwise byte for byte the same; assert that in your script, as you did for the display master. Write its Prussian White edition by treatment D to `work/build/assets/identity/prussian/20261108_Lockmark-48px-Master-Prussian-White.svg`. Add it to `work/build/assets/identity/20261028_Identity-Minimum-Sizes.json` with the size range each master now covers, chosen by test and logged as a routine call. Leave the proposal file in the board folder; it is the record of what Dustin approved.
2. **Where the 48 px master goes.** The masthead (L3, its lockmark at 48 px on whole pixels) and the sign-off draw it. The page header and the footer keep the 24 px master. Change every place that draws these: Rules 08.1, 08.2 and 08.3 with their specifications, builders notes and plates; chapter 03's L3 wherever it shows the masthead form; the proofs (masthead, social card, letterhead). If L3's master file embeds the lockmark, write a new dated L3 master beside the old one and say so in your notes; the old file stays as a record. Rewrite the held wording in Rules 08.1 and 08.3 so it names four masters and says what stays the same in every place.
3. **The feed test (DR-131, CA-S2).** Write the test into Rule 08.2's specifications in plain words: a 1,200 by 630 card reduced to 500 and 360 px wide must keep a visible lockmark, with the measures you used. Run it on the proof's social card with the new master, and print the passing figures where the rule gives them.
4. **The end mark (DR-130, CD-N8).** Rule 04.6 draws B at the text's cap height at every body size, as plate (a). Replace "a little taller than the capitals beside it" with the measured figures, taken again in Chromium after the change. Rule 03.4 gains one line: the end mark alone may stand under 16 px, at the text's cap height, because it follows a word and names nothing on its own. B's row in the minimum sizes file says the same. Check every specimen in your chapters that ends an article on B. The pixel-fit end mark at 12 and 14 px is not part of this pass.
5. **L6 (DR-129).** `l6()` draws without the dots everywhere L6 appears: `s-03-l6`, the lockup sheet, the minimum table, Rule 08.2's footer row and any proof. L6's text says a page narrower than 884 px closes with the footer place. Remove any line that says L6 waits on Dustin.
6. **CD-N9.** Inset Rule 08.2's place labels (Masthead, Page header, Footer, Sign-off) 16 px from the frame's left rule, as Rule 04.6's tags are.
7. Look at chapters 03, 04 and 08 and the proofs at 1440 and 390 px, at twice size where detail matters: the masthead, the sign-off, the end mark at 17 and 19 px, L6 and the social card.

### Editor (`.claude/agents/oa-editor.md`): chapter 01, then a copy edit

1. **Now.** Rule 01.11's reason takes DR-132's words exactly. Change `RULE_11_WHY` in `work/build/scripts/phase-2/guide_editor_ch01.py` and rebuild through `guide_editor_build.py`. Search chapters 01 and 02, their specimens and alt text for any other copy of the old reason, and change it too.
2. **Round two, when the main session sends you the identity designer's notes.** Copy edit every string the identity designer added or changed in chapters 03, 04, 08 and the proofs. Change strings in the identity designer's build scripts and rerun them, as you did in the apply pass's round two. Never change a measured figure without the identity designer's notes behind it.

## Checks before you hand back

- Your own build script, then `python3 -I work/build/scripts/phase-2/guide_build.py --strict`, then `node work/build/scripts/phase-2/guide_check.js work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html`. The check takes about two minutes. If the build fails in a file you do not own, wait a minute and retry.
- npm is installed in `work/build` for this container. Do not reinstall it.

## Notes and limits

Add a section headed "Q1 to Q4 pass" to your apply pass notes (`20261107_Apply-Pass-Identity-Notes.md` or `20261107_Apply-Pass-Editor-Notes.md`): what you did for each item, routine calls as "D2-xxx | decision | reason" lines, questions for Dustin with a recommendation (only where a change truly needs him), Tested and Not tested kept apart, and a change log. Never touch `source/`, `work/ledger/`, the Civic Line masters, any board other than reading it, the reader check, or another owner's files. Do not commit or push. Reply to the main session in 150 words or fewer: what changed, what failed, and your notes file.
