# Review of rounds 4 and 5: reader panel, simulated (RP)

Oath & Action Edition 06, Phase 3, chat 7, November 16, 2026. Written by the reader panel agent for the main session, under the review brief `work/handoffs/phase-3/20261116_Phase-3-Rounds-4-5-Review-Brief.md` ("Reader panel, simulated").

**Every reader on this page is simulated.** Dustin struck real reader tests before launch (DR-202). No real person read this work. Each reader below is a profile written by one agent, and each reader's words are that agent's prediction of how such a person would read. Treat them as hypotheses to check with real readers in a later phase, never as findings from people.

Status: in progress. Started 16:35 UTC (read by `date -u`).

## How the panel ran

- Build read: the strict build of `9a6e1182` at `scratchpad/c07/main/guide.html`, never read whole. Page text came from a script (`scratchpad/c07/review/reader-panel/scripts/extract.py`) that pulls each rule and plate by its anchor.
- Pictures: the shared capture set (`scratchpad/c07/captures/`), as `index.json` listed them while the capture run went on.
- Each reader read the selection guide "Choose a chart", Rules 14.142, 14.143, 14.144, 15.22, 15.23, 15.24, 11.10 and 11.11, and one round 4 form chosen to fit that reader.
- Seven readers: the two fairness readers count as two.

## Reader profiles, written before they read

Each profile is invented for this panel. None is a real person.

| # | Simulated reader | Profile | Screen | Round 4 form |
|---|---|---|---|---|
| R1 | Newcomer on a phone | Thirty-one, works shifts at a distribution warehouse, votes in presidential years. Knows the Supreme Court and Congress exist; has never met "cloture", "remand" or "interval". Reads on a phone between tasks, thumbs down the page, quits a table wider than the screen. | 390 and 320 px, Newsprint and Charcoal | 14.138, S92 step-by-step |
| R2 | High school civics teacher | Teaches eleventh-grade U.S. Government in a public school, fourteenth year. Plans a 50-minute lesson on how a law is made, struck down and challenged, and wants one plate to project and one to print. Knows the process well and catches a wrong legal term at once. | 1440 px on a laptop and a classroom projector; grayscale print | 14.135, S89 process explainer |
| R3 | Local reporter on deadline | Covers county government for a small daily. Has 90 minutes to file a monthly jobs chart for tonight's paper. Uses a web chart tool, knows "margin of error" loosely, has never read a style guide past its color page. | 1440 and 1024 px | 14.79, S85 icon array |
| R4 | Partner staffer, one chart a month | Communications associate at a partner nonprofit. Makes one chart a month for a newsletter and social posts in a design app. Not a statistician; afraid of getting the brand wrong; wants to be told which chart and which colors. | 1024 and 768 px, then 390 px to check the post | 14.141, S95 social data card |
| R5L | Reader who leans left | Retired public school librarian, volunteers with a voter registration group, gives to Democratic candidates. Reads for whether the guide's examples and words favor one side. Knows campaign finance cases by name. | 1440 px | 14.137, S91 comparison cards |
| R5R | Reader who leans right | Owns a small machine shop, votes in Republican primaries, serves on the county planning board. Reads for whether the jobs chart or the reform examples quietly argue against the party in power or for one side's reforms. | 1440 px and 390 px | 14.136, S90 by-the-numbers panel |
| R6 | Screen reader user | Blind from birth, a benefits counselor, uses a screen reader with Chrome every working day and moves by headings, tables and links. Simulated from the page's accessibility text (see "How R6 was simulated"), never from a real screen reader. | No picture; text only | 14.81, S87 Venn diagram |

## Working notes, 16:41 UTC (kept until the readers' sections replace them)

- Browser check at 16:41 UTC: `browsers.sh` printed "browsers=2 load=3.15, WAIT". R6 is built from the plates' alt text, `role="img"` labels and live text by script for now; I will try once more after 17:30.
- Captures read so far: Newsprint 1x at 1440 (the only folder landed at 16:41).
- Faults seen so far, to be written up below: S92's table calls "Go to court" and "Appeal a denial" "Every request"; Rule 14.144's R-38 card places Variable EC9 "in the technology layer" where R-30's card places it "in the economy layer"; "band" means a margin band on 14.142 and "the kind of change" on 14.144; Rule 15.22's stage 2 gives a simple majority as "218 of 435" and "51 of 100"; stage 7 names only a conference committee; 15.24's one worked reform, R-28, has no stated reason it was chosen.
