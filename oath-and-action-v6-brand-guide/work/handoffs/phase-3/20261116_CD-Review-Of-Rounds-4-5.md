# Creative director's review of Phase 3, rounds 4 and 5 (first pass)

Oath & Action Edition 06, Phase 3, review of rounds 4 and 5, November 16, 2026 (chat 7). Written by the creative director (`oa-creative-director`), a subagent of the main session, for `work/handoffs/phase-3/20261116_Phase-3-Rounds-4-5-Review-Brief.md`. The scores, reasons and fixes are also in `20261116_Rounds-4-5-CD-Scores.json`, in the form of round 3's scores.

Status: in progress. Started 16:51 UTC. This file grows as I work, since the container can restart. Sections marked "pending" are not yet written.

## Decision or verdict

Pending.

## Scores

Pending.

## Reasons

Pending.

## Required changes

Pending.

## Working notes, first look (16:58 UTC)

Read from the shared captures, Newsprint 1x at 1440 px, all 98 plates and rules; tiled tall plates in my scratch folder to read them at true size.

- S96 (14.142): the band, the two named drops in the subject ink, the hatched preliminary months and the phone drawing read as the chapter's finest chart. The phone drawing does not name the two drops; check the phone note.
- 14.143: each loop counts its own steps; the still sequence prints under the controls. Strong.
- 14.144: with Reform R-38 chosen, Connection L39 draws as the heaviest line in the drawing, in black, though R-38 has no target on the loop. Cause found in the plate's CSS: the rule for an unchosen reform resets `.ak-mark` to 2 px but leaves the 6 px `.ak-case` stroke that `.sv .crt .ak-case` sets. A misleading mark on the plate whose lesson is that R-38 acts off the loop.
- 15.22: stage 10's two `.sq` lines break into three columns ("Short of", "two-thirds", "in either chamber, the bill dies.") because `.wf .sq` is `display:flex` and the `nw2` span becomes a flex item. Two lines in the guide, both in 15.22.
- Selection guide: one drawing system, neutral inks, avoid forms struck and boxed; reads like a reference a design firm would sign.
- Palette plate: complete and exact; long (8,025 px at 1440 px).
- S86's size key draws a 40,000 circle as large as the data's largest; S94's calendar strip draws at about 220 px in a 720 px column with no day ticks and a legend with no gap between its two items.
- S89, S91 and S94 titles run past 30 words; S87 and S88 titles list four and three counts.

## Tested

- Read the brief whole, my role file and round 3's scores and review for form (16:51 UTC).

## Not tested

Pending.
