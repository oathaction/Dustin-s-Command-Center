# Oath & Action V6 studio rules

This project rebuilds the Oath & Action brand guide as Edition 06. Dustin Cathcart, Founder and Editor, is the client and the only person who approves changes. The full specification is `brief/20261021_Oath-And-Action-V6-Master-Brief_V2.md`. Read it before any phase work, and reread the sections a phase names before starting that phase.

## Folder layout

```
source/                 supplied files. Read-only. Never edit, move, rename or delete.
brief/                  master brief and phase prompts
work/extract/           parsed parts of the large source files
work/research/          research ledger, rights ledger, reference boards
work/boards/            proposal and review boards (HTML) shown at gates
work/build/             modular source for the V6 guide and the asset package
work/handoffs/          files agents pass to each other
work/ledger/            change ledger, decision log, open questions, gate reports
deliverables/           finished files only
```

## Gates

1. Every phase ends at a gate. Write the gate report to `work/ledger/` and stop. Begin the next phase only after Dustin replies in the conversation with an approval.
2. A gate report contains: what was done, the review board to open, rubric scores, decisions made, open questions, the proposal for the next phase, and a change log of files created and modified with their locations.
3. Each gate approves the proposal for the next phase. Work outside an approved proposal waits for the next gate.
4. Any change to a locked element (Master Brief section 3) or to identity geometry needs its own named approval. Show the original and the proposal side by side at actual sizes before asking.
5. Inside an approved phase, make routine decisions yourself and record them in the decision log with a one-line reason.

## Start of every session

Read, in order: `work/ledger/YYYYMMDD_Decision-Log.md`, `work/ledger/YYYYMMDD_Change-Ledger.md`, `work/ledger/YYYYMMDD_Open-Questions.md`, and the latest gate report. Confirm which phase is active and what was approved. Then continue.

## Large files

The source HTML files are 0.5 to 4.3 MB and carry base64 fonts and images. Never read one whole. Write extraction scripts that split them into CSS, scripts, the SVG sprite, fonts, images and one file per chapter under `work/extract/`, then work on the extracts. Atlas V7 keeps its model as JSON in `<script type="application/json" id="atlas-data">`. Extract it to `work/extract/atlas-v7-data.json` and query it with scripts. Run Python with `-I` when it reads supplied files.

## Agents

The studio agents live in `.claude/agents/`. Use them as Master Brief section 4 describes. Give each agent a written task, the file paths it needs, and the output path. Agents return work as files in `work/handoffs/` with a short summary. Run independent agents in parallel. Keep the pass accurate: if a step was done by the main session instead of a separate agent, say so in the gate report.

## File naming

- Files: `YYYYMMDD_Title-Case-Words.ext`, with the execution date, one `_` after the date, Title-Case words joined by hyphens, a lowercase extension, and an optional `_V2`, `_DRAFT`, `_REVIEW` or `_FINAL` suffix.
- Folders: lowercase kebab-case. `_archive/` and `_templates/` are the only folders that start with `_`.
- In paths written as `YYYYMMDD_...`, use the date the file is first created. A living ledger keeps its first date, so find it with a pattern such as `work/ledger/*_Decision-Log.md`.
- Source code and tool configuration keep their language or tool conventions (`build.mjs`, `tokens.css`, `CLAUDE.md`).
- Never use spaces, `(1)`, `copy`, or `FINAL_FINAL`.

## Writing rules for every word in the guide and in reports to Dustin

Plain, spoken prose in active voice. Explain terms at first use. Quote the locked brand lines exactly. Vary sentence length. Avoid em dashes, antithesis, corrective negation, contrasting pairs, rhetorical triplets, parallel sentence runs, setup and payoff lines, slogan-like closing sentences, throat-clearing openers, summary beats, stacked noun phrases, nominalizations, hedging qualifiers, performed enthusiasm, filler intensifiers (genuinely, really, truly, actually) and corporate verbs (leverage, underscore, reflect).

## Honesty

Report what you tested and what you could not test as separate lists. Never describe a check you did not run. Label illustrative people, quotes, places and figures beside the item. Every public policy statistic carries its source, observation period and qualification.

## End of every phase

Finish with a change log: files created, files modified, and their locations.
