# Round 4 editor notes

Oath & Action Edition 06, Phase 3, round 4. Editor (`oa-editor`), November 13, 2026, under `work/handoffs/phase-3/20261113_Phase-3-Round-4-Brief.md` (the editor's row and its "Editor" paragraph bind). Paths are relative to `oath-and-action-v6-brand-guide/`. Scratch: `/tmp/claude-0/-home-user-Dustin-s-Command-Center/5af59004-38b5-5773-926b-c1b00dd9bd57/scratchpad/phase-3/round-4/editor/`. Written as I go; the container can restart.

The owners read the four "Words for" sections directly. Each row gives the file, the field, the old words and the new, and why. The owner applies them; once an owner reports finished, I write straight into its word fields (D3-669) and log each change here. I never touch a key that picks a mark or an ink (V22, D3-1297).

## Status

- 20:41 UTC. Started. Read my role file, `CLAUDE.md`, chapter 02's writing rules, the round 4 brief and my round 3 and board 2 notes. No round 4 spec, entry, sketch or notes file of another owner exists yet. Working tree clean at `829d0db8`. Next: the rest of the brief's "Read first" list, then group lines 9 and 17, then Rule 13.4's plates once the systems designer's DR-265 list lands, and S37 once the data lead rules.

- 20:49 UTC. Baselines taken: `phase3_ch14_rules_build.py` and `phase3_ch13_build.py` each rerun with no change and write nothing (`git status` unchanged). S37 built as committed to scratch (PASS, 16,065 bytes, 16,815 with its frame), and a scratch preview of its curl (below) for the data lead. Read the data lead's rulings (a) to (c); no ruling on S37 yet. Rule 13.4's two plates print no chain label (below), which the systems designer's list should confirm.

## Summary

## Routine calls

- D3-xxx | The brief's "group lines 9 and 16" are read as the lines of the two round 4 families: group 9, proportion and overlap (coverage plan 3.8), and group 17, infographics (coverage plan 3.16), which the plan file and `14-chapter.json` number 17 | The plan file's `groups` give group 17 the family section 3.16 and rules 14.135 to 14.141; group 16 is tables and plain words, built in round 1, and I read its line too

## Group lines 9 and 17

## Rule 13.4's plates (DR-267)

**What the two plates print today (20:47 UTC, read by script on `s-13-4-correct.html` and `s-13-4-failure.html`).** Each loop prints its chip and its own title in quotation marks (`loops[].title`), then each connection's chip and its own name (`links[].name`), with the grade word on the correct plate. Neither plate prints a variable's name in any form: no chain label (`loops[].chain_labels`) and no variable title (`nodes[].title`), in the visible text, the alt, any `<svg>` (11 and 4 drawings, none with a `<text>`, `<title>` or `<desc>`), or an attribute. A match of every one of the 31 chain labels that differ from their variable's title, as a whole item or a short phrase, finds none in any chapter 13 plate. The only raw substring hit is "Safe seats", which opens Loop R10's own title ("Safe seats shift accountability to small primary electorates") and Connection L08's name ("Safe seats make the primary decisive"); both are the atlas's names for a loop and a connection, which DR-265 and DR-267 leave as they are. So, unless the systems designer's list shows a label I missed, Rule 13.4's plates need no change under DR-267, and I will say so to the data lead rather than add variable names the plates never printed.

## S37's curled apostrophes (D3-1556)

**Scratch preview, before the ruling (20:45 UTC).** A copy of `s37.json` with `"typography": {"curl_quotes": true}` after its `table` (S06's and S42's form), built with `--specs` from scratch; the repository's spec is untouched. PASS, 0 faults. Against the committed spec built the same way, the four SVGs differ in exactly two `<text>` elements each, at the same x and y: the drawn row labels "Rebuild Congress's own staff and experts" and "Limits on pricing software using rivals' data" print "Congress’s" and "rivals’". The CSV export is the same byte for byte. Weight, as the guide places it: 16,065 to 16,194 bytes (16,815 to 16,944 with its frame), 129 bytes more; a scratch copy with no change weighs 16,065, so the 129 bytes are the curl itself (the key in the compressed island and the curled table cells), not the scratch path.

## Words for maker A

## Words for the infographics maker

## Words for the cartographer

## Words for the systems designer

## Requests

### Requests to the data lead

- **ED4-1, S37's curl (D3-1556), ready on your ruling (20:50 UTC).** The facts are under "S37's curled apostrophes": `"typography": {"curl_quotes": true}` changes two drawn row labels and nothing else in the drawing, keeps the CSV as stored, and costs 129 bytes on the page (16,944 with its frame). Please rule in your notes whether I apply it. Once you do, I write the one key, rebuild S37, check the drawings again and list the two labels for board 3.

## Tested

## Not tested

## Files

- Created: this file.
