# Data visualization round: the creative director's brief

Oath & Action Brand Guide, Edition 06. Phase 2, November 6, 2026. Written by the main session. Paths are relative to `oath-and-action-v6-brand-guide/`.

## Your task

Score the three chart-system concepts after their fix pass, recommend one to Dustin, name the last faults that must be fixed before he sees Board 3, and write the board's content. You hold the bar Dustin set: "the work of a globally renowned branding and design firm."

Read first: `CLAUDE.md`; your role file `.claude/agents/oa-creative-director.md`; the makers' brief `work/handoffs/phase-2/20261106_Data-Viz-Brief.md`; the fix pass brief `work/handoffs/phase-2/20261106_Data-Viz-Fix-Pass-Brief.md`; the six red team reports and the reader panel (`work/handoffs/phase-2/20261106_Data-Viz-Red-Team-*.md`, `20261106_Data-Viz-Reader-Panel.md`); each maker's notes with its "Fix pass" section (`work/handoffs/phase-2/20261106_Data-Viz-0N-Notes.md`); the decision log from DR-44 on (`work/ledger/20261020_Decision-Log.md`); and, for the standard the atlas round set, your own review `work/handoffs/phase-2/20261105_CD-Review-Of-Editorial-Systems.md`.

The pages:
- `work/boards/phase-2/data-viz/01-explainer/20261106_Data-Viz-01-Explainer.html`
- `work/boards/phase-2/data-viz/02-register/20261106_Data-Viz-02-Register.html`
- `work/boards/phase-2/data-viz/03-instrument/20261106_Data-Viz-03-Instrument.html`

Open every view yourself with Playwright (preinstalled; `require('playwright')`, `chromium.launch()` with no options) at 1440 and 390 px, at deviceScaleFactor 2 for close looks, and save renders to your scratchpad. Compare each concept with the atlas pick (`work/boards/phase-2/atlas-editorial/01-times-explainer/captures/`), since the charts and the atlas must read as one family. The red team scores were given before the fix pass; yours come after it.

Edit no page and no shared file. Write only the two outputs below.

## Outputs

**1. Your review**, `work/handoffs/phase-2/20261106_CD-Review-Of-Data-Viz-Systems.md`:
- Scores 1 to 5 for each concept on Craft, Clarity, Brand fidelity, Usefulness, Evidence honesty, Accessibility, and Beauty and distinctiveness, with a line of reason each. The ship threshold is 4 on every line.
- Your recommendation and a runner-up, with the reasons, and what the runner-up does best that the pick should borrow.
- "Must fix before Board 3": the last faults per concept a reader would meet, each concrete enough for a maker to fix in minutes. Keep it short; the bar is faults, not wishes.
- "Finishing work for the pick", ranked: what turns the picked concept into chapter 14 (the full set of twenty or more charts, the selection guide, the palette specification, three complex examples, and the chart kit Dustin approved in DR-49).
- Your view on the two page colors (White and Newsprint) for charts and the atlas together (DR-45), and on the two diverging candidates the concepts tested in S06 (A, one-sided, Stone through a neutral to Verdigris; B, Prussian through the ground to Verdigris).
- Risks for Dustin to weigh.
- What you tested and what you could not test, as two lists.

**2. Board 3's content**, `work/boards/phase-2/data-viz/board-3/20261106_Board-3-Content.json`, in this shape (plain strings, the writing rules apply to every word):

```json
{
  "deck": "two or three sentences: what Board 3 shows and what Dustin is asked",
  "pick": "01",
  "runner_up": "02",
  "concepts": {
    "01": {"name": "Explainer", "idea": "one sentence", "pick_if": "one sentence", "best": ["three or four lines"], "holds_back": ["two or three lines"],
           "cd_scores": [0, 0, 0, 0, 0, 0, 0], "red_team": {"statistics": 0, "civic": 0, "interface": 0, "brand": 0, "craft": 0, "production": 0}, "readers_first": 0},
    "02": {},
    "03": {}
  },
  "rec_text": "a paragraph on why the pick",
  "runner_text": "two sentences",
  "finishing": ["ranked lines"],
  "ground": {"rec": "White or Newsprint", "text": "two sentences"},
  "diverging": {"rec": "A or B", "text": "two sentences"},
  "decisions": [{"q": "short question", "text": "one or two sentences of context", "rec": "the recommendation"}],
  "risks": ["lines"]
}
```

Fill `red_team` from the six reports' scores (before the fix pass) and `readers_first` from the reader panel's count of first places. The decisions list must include, in this order: which concept to pick; the page color; the diverging pair; the editor's disclosure wording on the four election-rule charts (D2-106; V7's QA report asks Dustin to confirm it); S01's party split (D2-104: totals only, since the Senate record could not be read); a web address for social cards once his site is settled (the website is on hold); and the order of work after the pick (the studio recommends building the full chapter 14 set and the chart kit next, then the direction review items, then the rest of Phase 2 through Gate 2, as DR-43 and DR-44 set). Add any other decision your review finds.

Finish with a summary under 200 words: scores, pick, runner-up, and the must-fix list.
