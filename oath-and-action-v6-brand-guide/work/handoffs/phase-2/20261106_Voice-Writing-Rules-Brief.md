# Chapter 02: the writing rules, before and after (editor's brief)

Oath & Action Brand Guide, Edition 06. Phase 2, November 6, 2026. Written by the main session for the editor. Paths are relative to `oath-and-action-v6-brand-guide/`.

## What Dustin asked for

Chapter 02 adopts Dustin's own writing rules as Oath & Action's public writing rules (DR-70). Each rule carries a labeled before and after taken from real Oath & Action copy, and Dustin sees the rules with their examples before the rest of the chapter is built. He asked for "the right narrative and copy", and his bar for everything is a finished product that looks like the work of the best branding and design firm in the world. The page that shows these rules is Board 5; the main session builds it from your content.

## Who you are

The studio's editor. Read and adopt `.claude/agents/oa-editor.md`, then read Master Brief sections 3, 8, 15 and 23 (`brief/20261021_Oath-And-Action-V6-Master-Brief_V2.md`) and `CLAUDE.md`.

## The rules to set out

Dustin's full list, from his standing instructions to the studio. Each becomes one rule, in plain words a reader with no training understands, with any term of art explained at first use (for example parataxis, nominalization, corrective negation):

- Write for the spoken voice. Plain prose in active voice. Vary sentence length unpredictably.
- No em dashes.
- No antithesis, corrective negation, contrasting pairs, negative parallelisms or negative anaphoras.
- No rule of three (rhetorical triplets) and no parallel sentence structures within a paragraph.
- No parataxis used as a rhythm device, no paragraph pinning, no landing sentences, no summary beats, no slogan-like closing sentences, no setup and payoff constructions.
- No throat-clearing openers and no rhetorical crutches.
- No stacked noun phrases and no nominalization.
- No hedging qualifiers, no filler intensifiers (genuinely, really, truly, actually), no corporate-register verbs (leverage, underscore, reflect), no performed enthusiasm, no inflated adjectives.

Group them so a reader learns them in a sensible order (for example: sound like a person talking; say it straight; let the sentence carry its own weight; cut the padding). Then add the house rules the studio already follows on every page: quote the locked lines exactly; explain terms at first use; label illustrative people, quotes, places and figures beside the item; every public policy statistic carries its source, observation period and qualification; dates in words; numbers under ten in words except in data; the true minus sign; a title claims only what its evidence holds, with the grade's verb; no period split at an inauguration date (DR-64); party names in words, never party colors.

## The examples

Every rule gets one before and one after.

- **Before** comes from real Oath & Action copy wherever it exists, quoted exactly, with its source beside it (for example "V5 guide, chapter 02, How we sound", "Atlas V7, an everyday answer", "Studio draft, chart S14, first build, November 6"). Search the committed files for real copy: the Phase 0 editor audit (`work/handoffs/phase-0/20261020_Editor-Audit.md`, sections 2, 5 and 7), the text census (`work/handoffs/phase-0/20261020_V5-Text-Census-Summary.md`), the Phase 1 voice and headline work (`work/handoffs/phase-1/20261021_Voice-Line-And-Headlines.md`, `20261021_Editor-Review-Of-Phase-1.md`, `20261021_Brand-Strategy.md`), the atlas round and chart round reviews in `work/handoffs/phase-2/` (red team reports quote draft titles and notes before they were fixed, such as the stretch test's first titles in `20261106_Data-Viz-Stretch-Red-Team.md` and `20261106_CD-Review-Of-Stretch-Test.md`), and the V7 text in `work/boards/phase-2/data-viz/shared/20261106_Chart-Data.json`. The large source HTML files are not in this checkout; do not look for them.
- Where no real example of a rule exists, write one in Oath & Action's subject matter and label it "Illustrative" beside it.
- **After** is the rewrite. It must obey every rule on the page, not only the one it demonstrates, and keep every fact of the before. If the before holds a fact you cannot check, keep it unchanged and say so in your notes.
- One line under each pair says what changed and why it reads better aloud.
- No before may make a public figure, party or person look foolish; the examples teach a craft. Keep the set balanced across topics.

## The narrative

Open the section with a short passage (under 150 words) on why Oath & Action writes this way, tied to the reader promise, "We explain how a decision is made and give you a practical way to take part.", and the editorial commitment, "Clarity is our duty. Action is our promise.", both quoted exactly. Close the section with a short checklist a writer runs before publishing (no more than ten lines), written as questions. Every sentence you write obeys the rules it teaches; the reviewers will read your own prose against them first.

## Outputs

1. `work/handoffs/phase-2/20261106_Voice-Writing-Rules.md`: the section as it would read in chapter 02, in Markdown.
2. `work/boards/phase-2/voice/20261106_Voice-Rules-Content.json`, the same content for the board, in this shape (plain strings, no HTML):

```json
{
 "title": "How Oath & Action writes",
 "deck": "one or two sentences",
 "narrative": ["the opening passage, as paragraphs"],
 "groups": [
  {"name": "group name", "intro": "one sentence",
   "rules": [
    {"id": "W01", "name": "short name", "rule": "the rule in one or two sentences", "terms": "a plain definition of any term of art, or empty",
     "before": "the before, exactly", "before_source": "where it comes from", "illustrative": false,
     "after": "the rewrite", "why": "one line on what changed"}
   ]}
 ],
 "house_rules": [{"id": "H01", "name": "short name", "rule": "one or two sentences", "example": "a short correct example, or empty"}],
 "checklist": ["questions, ten at most"],
 "notes_for_dustin": ["anything he should decide, such as a rule that conflicts with a locked line or with V5 copy he may want to keep"]
}
```

3. A notes section at the end of the Markdown file: the sources you searched, every before you could not trace to a real source and labeled Illustrative, any fact you could not check, and what you tested and could not test.

Write only these files. Do not commit. Reply with a summary under 150 words.
