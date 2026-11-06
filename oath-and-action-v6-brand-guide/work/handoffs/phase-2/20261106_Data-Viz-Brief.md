# Data visualization round: the makers' brief

Oath & Action Brand Guide, Edition 06. Phase 2, November 6, 2026. Written by the main session for three specialist makers, the red team and the creative director. Paths are relative to `oath-and-action-v6-brand-guide/`.

## 1. What Dustin asked for

October 30: "a cool oath & action brand system for data visualizations, charts, graphs, maps, tables, and displaying data different ways", with "pay particular attention to nytimes. i like their visual style." Then: "Yes do editorial - clean, clear, great design like the New York Times." Then the scope: one New York Times-style editorial treatment for data, charts and the atlas together (DR-27). On November 6 he picked the atlas system, System 1 (DR-36): "I love the times explainer design." His bar for everything: the work of "a globally renowned branding and design firm."

His answers for this round (DR-44 to DR-51, `work/ledger/20261020_Decision-Log.md`):

- Three chart-system concepts, each with the same ten charts on the same data. After his pick, the full chapter 14 set is built in the picked system.
- Every concept shows its charts on White and on Newsprint. He settles one page color for charts and the atlas together.
- Data from Atlas V7 and primary public sources, each with a full source line. Anything else carries "Illustrative data" beside the chart.
- Locked type only: Inter Tight titles, Inter labels and numbers, Lora Italic for quoted words only. No serif chart titles.
- Party data in neutral inks with the party's name printed on the mark. Pillar Red and Prussian never mark a party.
- Still image first (Substack, email, social cards), with interactive versions for the atlas site and reports. The studio ships a chart kit, so build every chart from a generator function, never by hand.
- Two charts per concept on Charcoal.

## 2. What you deliver

One concept page per maker, built by a script, plus a notes file.

| Concept | Folder | Page | Build script | Notes |
|---|---|---|---|---|
| 01 Explainer | `work/boards/phase-2/data-viz/01-explainer/` | `20261106_Data-Viz-01-Explainer.html` | `build_concept.py` | `work/handoffs/phase-2/20261106_Data-Viz-01-Notes.md` |
| 02 Register | `work/boards/phase-2/data-viz/02-register/` | `20261106_Data-Viz-02-Register.html` | `build_concept.py` | `work/handoffs/phase-2/20261106_Data-Viz-02-Notes.md` |
| 03 Instrument | `work/boards/phase-2/data-viz/03-instrument/` | `20261106_Data-Viz-03-Instrument.html` | `build_concept.py` | `work/handoffs/phase-2/20261106_Data-Viz-03-Notes.md` |

Write only inside your own folder and your own notes file. Never touch `source/`, the ledgers, the shared folder, the shared scripts, another maker's folder, the atlas pages or the identity masters. If the shared data or a shared check is wrong, say so in your notes and to the main session; do not patch it.

### The page

One self-contained HTML file with hash views, listed in `<meta name="chart-views" content="white newsprint dark social system">`. Each view's root carries `data-view-root="<view>"`; the masthead links every view, and the first view links to the others.

| View | What it holds |
|---|---|
| `white` | A short header (the concept's name, one paragraph on its idea, the views), then the ten specimens S01 to S10 on White |
| `newsprint` | The same ten specimens on Newsprint, from the same generator with the ground changed |
| `dark` | Two specimens of your choice on Charcoal, with the dark palette you propose |
| `social` | One social card at 1080 by 1350, the size Instagram and LinkedIn use for a portrait post, built from one specimen. Show it at true size inside a `role="region" tabindex="0"` scroll box with an `aria-label`, or as a PNG you export with full alt text and the source beside it |
| `system` | The concept's rules on one sheet: the anatomy of one chart with every part named, the type ramp with sizes, the mark specifications (line weights, dot sizes, bar gaps), the palettes with measured contrast on each ground, the annotation and source-line rules, and a short "How to read our charts" for readers |

Beside each specimen, outside its `<figure>`, a small studio strip names the specimen's ID, its form and the reader question, and says in one line why this form answers it. Keep the strip visibly apart from the chart so nobody mistakes it for chart copy.

## 3. The shared language you all keep

These hold in all three concepts. They come from the atlas pick, the research brief and the locked brand.

**From the atlas pick** (`work/boards/phase-2/atlas-editorial/01-times-explainer/`; read `build_system.py`'s `CSS` block and look at the captures in `captures/`):
- Body Inter 400 17/27. Display Inter Tight 800, 56/60 at -0.035em; headline 40/44 at -0.03em. Eyebrows Inter 700 13/18, 0.06em tracking, capitals. Source and small text Inter 400 13/18 in Deep Stone (#4E535B). Page wrap 1440 px wide with 64 px side padding on desktop, 16 px side padding at 390 and 360 px.
- Hairline rules in Charcoal or Stone; line family 1, 1.5, 2, 3 and 6 px (D2-60).
- Context in Stone; the route or series the headline names in Charcoal, heavier.
- The pointing tag is the sign mark (DR-38) wherever a sign appears.
- Notes sit inside the drawing, joined to the data by 1 px leader lines.
- The wordmark master in the masthead, never live type: use `work/build/assets/identity/wordmark/20261028_Wordmark-24px-Master.svg` (and the 16 px master on phones), as the pick's `wordmark()` helper does, inside a link marked `data-red="signature"`.
- No newspaper's name, typefaces, wordmark, colors or layouts (D2-65). The quality is borrowed, not the marks.

**From the research brief** (`work/research/20261030_Data-Viz-System-References.md`, rules R01 to R28; read them all). The ones every specimen shows:
- R02, R03: a sentence title that states the finding, in Inter Tight 800, with the evidence kind (Finding, Association, Estimate, Illustration) as a label above it, and a verb that matches the grade: documented takes record language; well supported a direct finding; plausible "can" or "may"; hypothesis "untested"; contested shows both readings; scenario estimates take "would" or "may".
- R04: a measure line under the title naming the measure, unit, place and period.
- R05, R06: direct labels; a legend only when labels cannot fit; the unit once, on the top tick or first label.
- R07: annotation inside the plot: name the record, explain an unusual encoding, give a reader's scale.
- R15, R16, R17: bars from zero; never bridge missing data; one scale across small multiples unless the measure line says otherwise.
- R18, R19: labels Inter 600 at 13 px or more, tabular figures, the true minus sign (−, U+2212); horizontal hairline gridlines, no vertical grid, no ticks, a Charcoal baseline at zero.
- R20: a source line under every chart in section 15 order (publisher, title or table, observation period, geography, date retrieved, qualification), with the shared dataset's `source_line` as your starting text. Shorten only by dropping words, never facts.
- R21: a text or table equivalent for every chart that carries everything a sighted reader gets, notes and source included.
- R22: nothing important waits behind hover.
- R25: design at 390 and 360 px too. Keep text at its set size and redraw the chart for the narrow width (a second artboard, or a layout that reflows); never shrink a whole drawing so its text drops under 13 px.
- R26: color never carries meaning alone; pair it with a label, shape, pattern or position, and check the grayscale capture.
- R28: every mark, tick and number traces to the shared data.

**Rule 05.3, the red rule** (D2-01; quote it exactly where you teach it): "The wordmark's ampersand and the lockmark's lever are signature red and do not count, and neither do the ampersands inside the hinge diagram and the hinge-circle badge, which are identity marks. The hinge diagram never shares a view with the wordmark and never stands in for the hinge divider. An icon's red accent counts as signature red when the icon stands alone, as an app tile, an avatar or a single feature icon. In a row or a menu, icons go one color and only the current one keeps its red. Each view (one screen, card, slide or printed page) then carries one working red, in this order of precedence: an error the reader must fix; the step a reader can take now; the one point the headline names, which in a systems figure is where a reform acts. One job may take several marks, such as each target of one reform. A hinge headline's ampersand uses the view's working red. The hinge divider's ampersand takes its surface's ink: Charcoal on Newsprint and White, Newsprint on Charcoal, White on Prussian. In the guide itself, specimens, labeled failure cases and palette swatches do not count. Red never sits on Prussian."

How it works on a chart page:
- Red never encodes a series, a category or a scale (R10). It may mark the one point a headline names (R09).
- Treat each specimen as one view for the red count, and mark every red element: `data-red="working" data-red-job="<one short job name>"`, or `data-red="signature"` for the wordmark. The rendered check counts working-red jobs per page view, so on a page of ten charts, give red to at most one specimen per view and say which in your notes, or use none. A good use is one demonstrated specimen, as section 13 asks: show red marking the headline's point, and show how that red steps down to Charcoal when an ask or an error takes the view's red.
- Pillar Red on Newsprint measures 2.96:1, under the 3:1 graphics need, so a red mark on Newsprint takes a 1 px Charcoal keyline (R09). On White it measures 4.17:1; on Charcoal 4.49:1.

**Party data (DR-48).** Wrap every mark that stands for a party in an element with `data-party="Republicans"` (or "Democrats", and so on). Those marks take neutral inks, never Pillar Red or Prussian, and print the party's name. Order parties by value or alphabet. S01 tests this.

**Evidence and honesty** (Master Brief section 15; CLAUDE.md). Label illustrative items beside the item. State qualifications in the chart, not only in the table. Titles are studio drafts; mark nothing as Dustin's words. A title may say what a measure did over time; it may not say a policy caused it unless the source grades that cause.

**Writing rules** (CLAUDE.md) bind every word on the page and in your notes: plain spoken prose, active voice, no em dashes, none of the listed patterns (antithesis, corrective negation, contrasting pairs, rhetorical triplets, parallel runs, setup and payoff, slogan endings, throat-clearing, summary beats, stacked noun phrases, nominalizations, hedges, performed enthusiasm, filler intensifiers, corporate verbs). American spelling.

## 4. Data and the ten specimens

Every value comes from `work/boards/phase-2/data-viz/shared/20261106_Chart-Data.json`, built by `work/build/scripts/phase-2/dataviz_shared_data.py` from Atlas V7 (`work/extract/atlas-v7-data.json`) and the research lead's public series (`work/boards/phase-2/data-viz/shared/public/`, brief `work/research/20261106_Data-Viz-Public-Series.md`). Read each dataset's `rows`, `source_line`, `notes` and qualification before you draw it. Map geometry and the tile grid are in `work/boards/phase-2/data-viz/shared/geo/`.

| ID | Form | Dataset | Reader question |
|---|---|---|---|
| S01 | Big number in context | `stock-trading-ban` | Do Republicans and Democrats agree on anything about Congress? |
| S02 | Line with event notes | `child-poverty-spm` | What happened to child poverty when the expanded child tax credit was paid, and after it lapsed? |
| S03 | Ranked bar | `rule-changes-by-instrument` | Who changed the rules: voters, courts or legislatures? |
| S04 | Dot plot or dumbbell | `turnout-by-age` | Which age groups vote, and did that change between two elections? |
| S05 | Small multiples | `homeownership-by-race` | How far apart are homeownership rates by race, and has the gap closed? |
| S06 | Comparison table | `scenarios-2030` | If a reform path were followed, which way would each outcome move? |
| S07 | Map | `rcv-bans` | Where can a city adopt ranked-choice voting, and where has the state ruled it out? |
| S08 | Unit chart | `rule-changes` | Have the rules been moving toward voters or away from them? |
| S09 | Timeline | `history-events` | Which rule changes since 1870 decided who counts, who governs, who owns and who checks? |
| S10 | Evidence mix | `claims-by-grade` | How much of each everyday answer rests on documented fact? |

Each specimen's `requirements` field in the shared data adds what that form must show. Notes on the data:
- **S03** and **S08** come from V7's repair log. Its direction codes are the atlas's own, set out in `coding_note`; the chart must say so in a line. The data holds a finding worth a title: ballot measures moved the rules away from voters in none of 17 cases, and state statutes did in 9 of 11. Check that against the rows before you write it.
- **S06** prints V7's direction words exactly. A glyph or tint per cell follows `class_method` and is labeled as the studio's reading. This specimen tests a diverging scale without red and blue. The four families print as "Quality of democracy" (DR-39), "Government efficacy", "Economic performance" and "Income and wealth equality".
- **S09**: event keys E01 to E24 are the studio's. Every event is documented.
- **S10**: grades never take Pillar Red. The atlas draws grades as line textures (documented and well supported solid, plausible dashed, contested dash-dot, hypothesis dotted). A fill needs its own grade code that survives grayscale; the palette lab's grade ramp is a start.
- **S02, S04, S05, S07** use the research lead's public series. Their dataset records name the CSV, its columns and its `key_fields`; the mark key is those fields joined by `|` (for example `2021` or `18 to 24|2020`). Use the vintage and the qualification the research brief names.

### The data contract the verifier reads

```html
<figure data-spec="S03" data-dataset="rule-changes-by-instrument" data-evidence="Finding">
  <p data-role="evidence-label">Finding</p>
  <h3 data-role="title">…a sentence that states the finding…</h3>
  <p data-role="measure">Rule changes in the atlas's repair log, by how they were made, 1965 to 2026</p>
  <svg data-view="s03-wide" …>
    <rect data-key="Ballot initiative" data-value="17" data-mark="bar" data-axis="x" …/>
    <text data-key="Ballot initiative" data-value="17" data-mark="label" …>17</text>
  </svg>
  <p data-role="source">Source: …</p>
  <details data-role="equivalent"><summary>Show the table</summary><table>…</table></details>
</figure>
```

- `data-key` is the dataset row's key; `data-value` its number; `data-field` names the column when it is not `value` (for example `data-field="toward voters"`, or `data-field="rate"`); `data-category` carries a category string instead of a number (with `data-field`, or `direction` by default on `rule-changes`).
- `data-mark` is `bar`, `point`, `unit`, `cell`, `vertex` or `label`. Bars and points also carry `data-axis` (`x` or `y`, the value axis) and, where two scales share one drawing, `data-scale="<name>"`. The rendered check measures every bar against a zero baseline and every point against one straight scale, so draw them exactly.
- The required rows of each V7 dataset must all be drawn (every one of the 64 rule changes, 24 events, 16 questions, 8 scenarios, 7 instruments).
- A specimen may appear on several views; it needs the same attributes each time.

### Checks you must pass before you hand back

```bash
python3 -I work/build/scripts/phase-2/dataviz_verify.py --selftest work/boards/phase-2/data-viz/0N-name/20261106_Data-Viz-0N-Name.html
```

```bash
node work/build/scripts/phase-2/dataviz_check.js work/boards/phase-2/data-viz/0N-name/20261106_Data-Viz-0N-Name.html
```

The first checks every specimen and mark against the shared data and plants seven errors to prove it works. The second renders every view at 1440, 390 and 360 px and checks sideways scroll, the 13 px floor, text contrast, labels inside drawings and apart, Rule 05.3, party colors, the scale of bars and points, axe-core (WCAG 2.2 AA), focus rings and the click from the first view into another view and back; it writes captures, including grayscale, to your folder's `captures/`. Both write results JSON beside your page. Fonts come from Google Fonts (Inter, Inter Tight, Lora); no other outside request is allowed, so no chart library from a CDN. Draw with Python-generated SVG and a little plain JavaScript for the views.

## 5. Color

Start from the palette lab (`work/boards/phase-2/data-viz/shared/20261106_Palette-Lab.json`, sheet `20261106_Palette-Lab.html`). What it measured:
- Charcoal 18.73:1 on White, 13.29:1 on Newsprint. Stone 6.05 and 4.29. Verdigris 4.74 and 3.37. Prussian 13.28 and 9.42.
- **Verdigris and Stone sit only 0.05 apart in OKLab lightness and 0.051 apart under deuteranopia.** Never separate two categories by those two inks alone; add a label, position or texture.
- On Charcoal, lifted Prussian and lifted Verdigris land 0.022 apart in lightness and 0.034 apart under tritanopia. Dark charts need direct labels and few categories.
- The sequential five-step ramps (Verdigris, Prussian) hold about 0.1 OKLab between neighbors on both light grounds and keep their grayscale order.
- Two diverging candidates go to Gate 2 (section 13): A, one-sided, Stone through a neutral to Verdigris; B, two-sided, Prussian through the ground to Verdigris. Never red and blue.
- Fills inside a scale may fall under 3:1 against the ground only when every value is printed or the table carries it; say so as a design judgment.

You may propose different tints. Derive each by mixing locked colors in OKLab (D1-04), give it one job, measure it on each ground, and list it in your notes. Identity colors never change.

## 6. The three concepts

All three stay inside the atlas pick's editorial language. They differ in what leads.

### 01 Explainer. Maker: a senior newspaper graphics editor

You have spent fifteen years on metro and national graphics desks, drawing charts for readers who scroll on a phone between other things. You believe a chart earns its place by making one point a reader can repeat at dinner. Your concept leads with the finding. Each specimen opens with its evidence label and a sentence title, then a short measure line, then a chart with generous white space, Stone context and one Charcoal subject, and the notes in the drawing do the teaching: name the record, give a reader's scale, explain the odd encoding once. Charts sit in one reading column the way an explainer's do, with a few breaking wider. Tables appear where a reader would look something up. This is the concept closest to what Dustin admired and to the atlas pick itself, so the bar is high: every label placed by hand-quality rules, every title true to its grade, nothing decorative.

### 02 Register. Maker: a reference information designer

You have built statistical yearbooks and the data pages of a weekly magazine, where readers compare and look things up. Your concept leads with the numbers. Tables are first-class: ranked registers with tabular figures, thin rules, a sparkline or bar inside the row, change columns and a sort order that answers the question. Charts sit on a strict grid with the same frame every time, so a reader learns the parts once: label, title, measure line, figure, notes, source. Prussian and Verdigris carry most data work, with their tints, and Stone carries context. This concept ties to Concept 11 Register, which Dustin favored, and should make the guide's tables the best thing in it. Keep the editorial voice: sentence titles and notes still lead each figure.

### 03 Instrument. Maker: a civic product data designer

You design data products people come back to: trackers, dashboards and the data views inside an atlas. Your concept leads with the system. Every chart is a module with fixed slots (label, title, measure, figure, notes, source, a Chart and Table switch, downloads), set on the Signal Grid's spacing, so a builder can make the next one from the kit without asking. Atlas IDs (RL01, PW15, E09) print as small index labels where they help a reader find the record. Texture and line style carry the second code after color, as the atlas's evidence lines do. The page shows how a chart behaves as a still image for Substack and as an interactive panel, and states which parts change. Keep it editorial and calm: a reader should feel a well-made report, never a control room.

## 7. Your notes file

Use the atlas round's notes as the model (`work/handoffs/phase-2/20261105_Editorial-01-Notes.md`): the idea; each view; your decisions with one-line reasons; the palette you used with measurements; where red appears and why; titles you would flag for Dustin; a self-score 1 to 5 on Craft, Clarity, Brand fidelity, Usefulness, Evidence honesty, Accessibility and Beauty and distinctiveness, with a line each; what you tested and what you could not test, as separate lists; a change log of files you created and modified. Finish your reply to the main session with a summary under 200 words.

## 8. What the red team and the creative director will look for

One reviewer per lens reads all three concepts: statistics and honest scales; civic education (does it teach); interface and accessibility (does it work at 360 px, by keyboard and in a screen reader's reading order); brand and nonpartisanship (does anything read as taking a side, is red disciplined, does it look like Oath & Action with the wordmark covered); type and drawing craft at 2x. A simulated panel of first-time readers sees only screenshots. The creative director then scores each concept on the seven-line rubric with a ship threshold of 4 on every line.
