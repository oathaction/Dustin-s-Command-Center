# Stage C round 1: editor's notes

Oath & Action Edition 06, Phase 2, stage C, round 1, November 11, 2026. Written by the editor (`.claude/agents/oa-editor.md`), run as a subagent of the main session, under item 6 of `20261111_Stage-C-Round-1-Brief.md`. I committed nothing and published nothing. Paths are relative to `oath-and-action-v6-brand-guide/`.

Status: second pass done. Sections 1 and 2 (chapters 01 to 12 and 17) are applied by their owners (D2-1334 to D2-1342). Sections 4 to 6 hold 67 rows for chapters 18, 19 and 26, as each stood between 03:06 and 03:57, grouped by owner with facts first; none is applied yet, since every one sits in another owner's generator or code.

## How I work this round

- I read each changed rule in a scratch build of the guide (`guide_build.py --strict --out <scratch>/guide.html`), by script, a rule at a time.
- Each word change gives the file and key (or the generator and its string), the text now, my text and the rule of chapter 02 it serves.
- Where I own the data, I apply the change and rebuild. Where another owner's generator holds the words, the change sits under that owner's heading for the main session to pass on. I change no output file by hand.

## 1. Words the promotion and round 0 added to chapters 01 to 12

**What I read.** Every string that differs from commit 820340a7 in chapters 03, 05, 08, 10 and 11 and in `manifest-systems.json` and `manifest-identity.json`, pulled by script (each JSON flattened to its keys), and the visible text of every changed specimen, set beside its old text. Then each changed rule whole, in a scratch build of the guide: Rules 03.2, 03.4 and 03.6 with `s-03-minimums`; Rules 05.3 and 05.4 with their plates; Rules 08.1 and 08.2; Rule 09.1 with `s-09-opener`; Rules 10.1, 10.4, 10.5, 10.6 and 10.9, the library's sheet 03, the list of 41 and `s-10-opener`; Rule 11.12 and chapter 11's changed plates (11.11 to 11.16, the marks and the menu; only 11.12 and 11.13 changed words, and 11.13 only where a line breaks).

**What I checked against files.** Rule 08.2's feed figures against `20261111_Promotion-C-Identity-Figures.json` (keys `feed`, `feed_dark`, `feed_thumbnail`): all match. The print L3's figures in `s-03-minimums` by arithmetic from its view box (1256.49 by 218.18 units, capitals 100 units): at 1.55 in the lockmark is 0.269 in and the capitals 3.13 mm, as printed. Rule 10.9's new likeness figures against the icon designer's runs: Evidence with Oversight and enforcement as fits 0.897, R-06's fit against R-41 and R-44 0.917 and 0.915, as printed (0.90 and 0.92).

Most of the new words read well and need nothing. The changes below are each small.

### 1a. CL-075 Housing, applied in my table

The systems designer's addendum (`20261111_Promotion-C-Ch10-Labels-Addendum.json`) held Housing's words until my table took the row (D2-1279). I added CL-075 to `work/handoffs/phase-2/20261110_Stage-B-Ch10-Labels.json` after CL-074, kept the label "Housing" and every other field as the addendum wrote them, raised the counts (125 rows, 75 CL, 20 topics) and added an `updated` line saying so.

| File and key | Now (the addendum) | Mine | Rule |
|---|---|---|---|
| `20261110_Stage-B-Ch10-Labels.json`, row CL-075, `meaning` | An apartment block stands beside a smaller pitched-roof house on one ground line, for housing as a subject: the homes of every kind where people live. | An apartment block stands beside a smaller pitched-roof house on one ground line, for housing, the homes of every kind that people rent or own. | W06: the colon holds the meaning back; none of the table's other 124 sentences uses one (its meaning rules). "Rent or own" follows the master's own description ("renters' and owners' alike") and sets Housing apart from Owner home equity |

I looked at the drawing first (`png-256/red-black/...CL-075-Housing-Red-Black.png`): the house is smaller than the three-floor block, so "smaller" holds.

**Rebuild, for the main session.** Chapter 10's words come from its generator, which writes the systems designer's files, so I did not run it in the project. I ran it in a scratch copy of the tree (`stage_b_ch10_build.py --no-draw`) and compared every output with the committed one: the only file that changes is `work/build/guide/specimens/s-10-lib-03.html`, and only CL-075's sentence in it. `10-symbols.json`, `manifest-systems.json`, the figures file, the other 26 specimens and the five sheet images come out byte for byte. So the one command in the project is `python3 -I work/build/scripts/phase-2/stage_b_ch10_build.py --no-draw`, by the main session or the systems designer. Chapter 11's library reads only the label, which did not change. The addendum can stay as the record; both generators read my table first.

### 1b. For the systems designer (`stage_a_systems_ch05.py`, `stage_b_ch10_build.py`, `apply_systems_ch11_ui.py`)

| Generator and string | Now | Mine | Rule |
|---|---|---|---|
| `stage_a_systems_ch05.py`, Rule 05.4 `builders[0]`, last sentence | Draw a state’s bar as a border, such as `<code>border-left: 4px solid</code>`, since forced colors removes an inset shadow. | Draw a state’s bar as a border, such as `<code>border-left: 4px solid</code>`. Forced colors, a setting such as the contrast themes in Windows that repaints a page in a few system colors, keeps a border and removes an inset shadow. | H02: this is the term's first use in the guide; the definition is chapter 17’s own (Rule 17.8), so the term holds from 05 on |
| `stage_a_systems_ch05.py`, Rule 05.4 `correct.caption`, third sentence | The error mark draws in the text’s ink, and its red is the 4 px bar. | The error mark draws in the text’s ink, and the error’s red is its 4 px bar. | W01: "its" points back to the mark, which holds no red; read aloud, the listener has to work out whose red it is |
| `stage_b_ch10_build.py`, Rule 10.4 `builders[1]`, a sentence after the last | (none) | The guide’s stylesheet switches the two with two lines; copy them into yours: `<code>.oa-at-2x { display: none } @media (min-resolution: 2dppx) { .oa-at-1x { display: none } .oa-at-2x { display: inline } }</code>`. | Contradiction 1 below: a builder who follows the rule as written shows both drawings at once. The CSS is the shell's own (`guide-shell.css`, lines 105 and 106) |
| `stage_b_ch10_build.py`, Rule 10.6 `correct.caption` | One drawing under two words, Congress and Congressional capacity, Housing beside its word from 48 px, and the names that keep close subjects apart. | One drawing under two words, Congress and Congressional capacity; Housing beside its word from 48 px; and the names that keep close subjects apart. | W01: read aloud, the comma list makes Housing sound like a third word under the one drawing |
| `stage_b_ch10_build.py`, Rule 10.9 `why.text[1]`, the new sentence (line 1458) | Their pixel fits, which a screen under 2x draws, part further, from 0.70 to 0.90, but Evidence and Oversight and enforcement still score 0.90, so the rule holds on every screen. | Their pixel fits, which a screen under 2x draws, sit further apart, from 0.70 to 0.90, and the closest pair, Evidence with Oversight and enforcement, still scores 0.90, so the rule holds on every screen. | W01: "Evidence and Oversight and enforcement" runs two names into three; nobody says "part further" aloud. The code already prints the fits' maximum there, so "the closest pair" is exact |
| `stage_b_ch10_build.py`, Rule 10.9 `why.text[2]` (line 1461) | …, R-06, is the one of the three reform drawings on the list of 41. | …, R-06, is the only one of the three reform drawings on the list of 41. | W01 |
| `stage_b_ch10_build.py`, `s-10-9-correct` alt, line 988: `" and ".join(...)` for each group | Housing and Housing scarcity and Owner home equity and Cost of essentials: All four hold a home. | Housing, Housing scarcity, Owner home equity and Cost of essentials: All four hold a home. | W01: three "and"s blur four names into pairs. Join a group of three or more as a list (commas, then "and" before the last); the two-name groups read as they do now |
| `apply_systems_ch11_ui.py`, Rule 11.12 `builders[1]`, second sentence (line 952) | On a product page, wrap the field, its filters and its status line in a search landmark, `<code>&lt;div role="search"&gt;</code>`. | On a product page, wrap the field, its filters and its status line in a search landmark, the `<code>&lt;search&gt;</code>` element, so a screen reader can jump straight to it, as Rule 18.15’s code does. | Contradiction 2 below; H02, in chapter 18's own words for the landmark. Waits on the markup call in contradiction 2 |

### 1c. For the identity designer (`stage_b_identity_ch09.py`; chapters 03 and 08 through `stage_a_identity_chapters.py`)

Chapters 03 and 08 were still being finished when I read them, so I read them last and send their changes through these notes.

| Generator and string | Now | Mine | Rule |
|---|---|---|---|
| `stage_b_identity_ch09.py`, Rule 09.1 spec "48 px row" (line 442) | Words in the intro style, bold, 19 px on a phone and 22 px from 48em; 12 px from each icon's ink to its word | Words in the intro style, bold, 19 px on a phone and 22 px from 48em; 12 px from each icon's ink to its word. Where the column is narrower than the row’s 592 px, from 48em to screens about 1,080 px wide, the row breaks after the arrow that follows Track, two pillars to a line | The gap the identity designer named (D2-1179): the rule's own rows and the opener break there, and the specs said only what happens under 48em |
| `stage_b_identity_ch09.py`, `s-09-opener` alt (line 191), a sentence before the last | (none) | Where the column is narrower than the row, it breaks after the arrow that follows Track, two pillars to a line. | The alt then says what a reader sees at every width, as the plate draws it |
| `stage_b_identity_ch09.py`, Rule 09.3 `builders`, the sentence "The guide’s stylesheet shows the master from 2 device pixels per CSS pixel." | The guide’s stylesheet shows the master from 2 device pixels per CSS pixel. | The guide’s stylesheet shows the master from 2 device pixels per CSS pixel with two lines; copy them into yours: `<code>.oa-at-2x { display: none } @media (min-resolution: 2dppx) { .oa-at-1x { display: none } .oa-at-2x { display: inline } }</code>`. | Contradiction 1 below, the same fix as Rule 10.4's |
| Chapter 03, Rule 03.2 `builders`, its last four sentences, with the one added after the commit (working tree, read at 03:02) | L3’s masthead master serves the 282 px masthead on screen. For print and any other width, place L3’s print master, which sets the lockmark at 2.18 cap heights, the masthead’s proportion. On screen, where the wordmark stands under 40 px tall, build L3 from the pixel masters, as the masthead and the 196 px minimum do. The earlier L3 master, with its lockmark at 2.4 cap heights, stays in the folder as the record. | L3’s masthead master serves the 282 px masthead on screen. Elsewhere on screen, where the wordmark stands under 40 px tall, build L3 from the masters drawn on the pixel grid, the wordmark’s 16 or 24 px master beside the lockmark’s master for its size, as the 196 px minimum does. In print, and on screen where the wordmark stands 40 px tall or more, place L3’s print master, which sets the lockmark at 2.18 cap heights, the masthead’s proportion. The earlier L3 master, with its lockmark at 2.4 cap heights, stays in the folder as the record. | W01: the reader is told "any other width" takes the print master, and the next sentence takes some of those widths back. H02: "pixel masters" is a new name; Rule 08.1 calls them the masters that "sit on the pixel grid". The 40 px line is Rule 03.4’s, where the wordmark’s display master starts |
| Chapter 03, Rule 03.4 `builders`, fourth sentence | The lockmark’s 16 and 24 px masters take B’s ranges, its 48 px master serves 48 px and, in a social card’s sign-off, exactly twice that, 96 px, and its display master serves every other size from 49 px (Rule 08.1). | The lockmark’s 16 and 24 px masters take B’s ranges. Its 48 px master serves 48 px, and exactly twice that, 96 px, in a social card’s sign-off; its display master serves every other size from 49 px (Rule 08.1). | W01 and W03: read aloud, the clause wedged between "and" and "exactly" loses the listener, and the two "and"s blur which master serves what |
| Chapter 08, Rule 08.1 `rule`, third sentence | Place the 16 px master from 16 to 23 px, the 24 px master from 24 to 47 px, the 48 px master at 48 px in the masthead and on covers and posters, and at exactly twice that, 96 px, in a social card’s sign-off, and the display master, drawn for our brand guide’s fifth edition, at every other size from 49 px. | Place the 16 px master from 16 to 23 px and the 24 px master from 24 to 47 px. The 48 px master serves 48 px in the masthead and on covers and posters, and exactly twice that, 96 px, in a social card’s sign-off. The display master, drawn for our brand guide’s fifth edition, serves every other size from 49 px. | W01 and W03: one 64-word sentence with four "and"s; a listener cannot tell where the 48 px master's places end and the display master begins |
| Chapter 08, Rule 08.1 spec 8 (display master) | The field and node sizes above, at every size from 49 px but a social card’s 96 px sign-off; … | The field and node sizes above, at every size from 49 px except a social card’s 96 px sign-off; … | W01: "but" for "except" reads as a contrast |
| Chapter 08, Rule 08.2 spec "Sign-off" | …so every node, link and the lever land on whole pixels. | …so every node, every link and the lever land on whole pixels. | W01 |
| Chapter 08, Rule 08.2 spec "Feed test, dark card", third and fourth sentences | On a dark ground the links take the nodes’ own color, and in a 96 px sign-off they run 2 px wide, so one bright pixel can come from a link; a link shrunk under 1 px cannot fill a block. Each floor sits halfway between the brightest block the links alone leave in a node’s square and the dimmest node’s brightest block, measured on our card at both widths | On a dark ground the links take the nodes’ own color. In a 96 px sign-off they run 2 px wide, so a single bright pixel can come from a link, and the test counts blocks because a link the feed shrinks under 1 px wide cannot fill one. Each floor sits halfway between the brightest block the links alone leave in a node’s square and the dimmest node’s brightest block, measured on our card at both widths, then rounded down to a multiple of 5 | W04: "because" joins the reason to the claim the semicolon set beside it. W20: the halfway points are 155.5 and 192 (figures file, `feed_dark.floor_study`), and the floors print 155 and 190, D2-1169's rounding |
| Chapter 08, Rule 08.2 spec "Feed test, our card" | The link-preview card in the identity proofs passes with its 96 px sign-off. At 500 px wide, its lockmark keeps 8 of 8 nodes and 52 red pixels; at 360 px, 8 of 8 nodes and 22 red pixels. Drawn on White or on Charcoal, the same card keeps 8 of 8 nodes and 48 red pixels at 500 px, and 8 and 20 at 360 px. On Prussian, with the White lever counted as a ninth node, it keeps 9 of 9 at 500 px and 9 of 9 at 360 px | The link-preview card in the identity proofs, on Newsprint, passes with its 96 px sign-off. At 500 px wide, its lockmark keeps 8 of 8 nodes and 52 red pixels; at 360 px, 8 of 8 nodes and 22 red pixels. Drawn on White or on Charcoal, the same card keeps 8 of 8 nodes and 48 red pixels at 500 px, and 8 of 8 nodes and 20 red pixels at 360 px. On Prussian, with the White lever counted as a ninth node, it keeps 9 of 9 nodes at both widths | W01: "8 and 20" leaves the listener to supply the units, and the first figures never say their ground, though the next sentence names two others |

### 1d. Contradictions found

1. **Rules 09.3 and 10.4 against the code they print.** Both tell a builder to write a 24 px drawing as one svg with two uses, classed `oa-at-1x` and `oa-at-2x`, "that the guide’s stylesheet switches". The two lines that switch them live only in `work/build/guide/shell/guide-shell.css`; `tokens.css` holds neither class. A builder who copies the svg into a product page shows the fit and the master on top of each other. Fix in words: the builders sentences in 1b and 1c. The other fix is for the engineer to ship the two lines in `tokens.css`, which chapter 26's Rule 26.5 tells a builder to start from; then each builders line would say so. Either way the two rules change together.
2. **Rule 11.12 against Rule 18.15.** Rule 11.12's new builders line wraps a search in `<div role="search">`; Rule 18.15's words and its code to copy (`c-18-search.html`) use the `search` element. Both make a search landmark, and chapter 18 already says what an older browser does with the element. A builder reading both chapters gets two answers. My recommendation: Rule 11.12 follows Rule 18.15, chapter 18 being the component's home (the stage C brief's "One component, two homes"). The markup call is the accessibility lead's and the systems designer's; my words in 1b follow the element and change if they pick the other.
3. **One name for two things, for chapter 26.** The words in Rules 05.3, 05.4 and 11.15 call the circle holding an exclamation mark "the error mark", drawn in the text's ink. The token `--oa-color-state-error-mark-on-<surface>` is Pillar Red and paints the 4 px bar; its own description in `tokens.json` says so and calls the glyph "the error glyph". Rule 05.4 lists that token beside a plate whose words say the error mark is in ink. No reader text is wrong today, but chapter 26's token table will print the name. When I write chapter 26's words I will describe this token as the error bar's color; renaming it is the engineer's call, and the token architecture's version rule would govern it.

### 1e. Looked at and left as they are

- Rule 05.4's alt ends on four clauses of one frame ("the selected check is a check mark; the warning mark is…"). It is a list of four definitions in one sentence, the form W12 allows when the facts hold four parts.
- Rule 10.6's "since it is not on Rule 10.4’s list of 41" states a fact with its reason; it is no corrective turn.
- Rule 08.2's why prints 17 red pixels at 360 px where the specs print 22. The why counts the JPEG a feed saves and the specs the plain reduction, and each says which, so they agree.
- `s-03-minimums` prints the print L3's lockmark as 0.269 in, three places where its neighbors print two. The figure comes from the round 0 figures file, and 0.27 would hide that it clears the 0.25 in minimum by less than two hundredths.
- Chapter 07's "keeps its landmark list short" is the guide's first "landmark", with no definition. It did not change today, and the new words in chapters 11 and 18 explain the term where a builder acts on it, so I note it for the next pass on chapter 07 (systems designer): "keeps short the list of landmarks, the regions of a page a screen reader can jump between".

## 2. Chapter 17, Motion and states: edits for its makers

**What I read.** The chapter file as its generator wrote it at 02:52 and again at 02:57 (the second added Rule 17.6's live hinge and lever and the lever extra), `manifest-motion.json`, the identity designer's three `s-17-hinge-*` and `s-17-lever-*` alts in `manifest-identity.json`, and every plate's visible words in a scratch build, players included (status lines, reason lines, still views, numbered keys). I checked the facts the words lean on: every contrast figure against `20261111_Stage-C-Round-1-Ch17-Figures.json` (all match); the timings (land 200 ms, a 40 ms stagger and a 320 ms slide make Rule 17.1's 560 ms; draw, stagger and land make Rule 17.4's 440 ms); that `tokens.css` sets all six durations to 0 ms under `prefers-reduced-motion: reduce`; the land's 112 percent (1.4 over 1.25); Loop R1's first link, L01, which Atlas V7 grades well supported, so "wealth concentration raises money in politics" may take a direct verb (H08); and the chapter titles the guide prints for 16 and 18.

The chapter reads plainly, and its rules match its plates in all but the places in A. The maker is still writing, so I quote each string and give its place in the generator as I read it at 02:57; line numbers will drift.

### A. Facts and contradictions, to apply first

| Generator and string | Now | Mine | Rule |
|---|---|---|---|
| `stage_c_ch17_build.py`, five strings: the empty sample in the ten states (near line 1093) and its alt (1125), Rule 17.12's plate (1305) and alt (1309), Rule 17.12 `rule[0]` (1850) | 0 of 124 symbols | 0 of 125 symbols, with the count read from the inventory in use, as `apply_systems_ch11_ui.py` reads `n_lib` | The set holds 125 since CL-075 joined; Rule 11.12 and its live plate print 125. A count read from the file holds at the next drawing (D2-1278's reason) |
| `stage_c_ch17_build.py`, Rule 17.10's list plate (near line 1243) | 16 Photography … 18 Components | 16 Photography, illustration and video … 18 Components and interaction | The plate shows the guide's own chapters as the current page in a list, and the guide names them so (Rule 17.8's related chapters print "18 Components and interaction") |
| `stage_c_ch17_build.py`, `WHY_START` (near line 528), every player's reason line, and its quote in `s-17-3-correct`'s alt (831) | At the first frame, so Reset waits until you press Play. | Reset works once you press Play. | Rule 17.11's own builders line: "Write the reason as the step the reader takes next." W01: the line reads as a status and names no step |
| `stage_c_ch17_build.py`, Rule 17.11 `rule[0]` and spec "Reason line" | …a reason line beside it that names the step… / Beside the control in secondary words, and in its accessible description | …a reason line under it that names the step… / Under the control in secondary words, and in its accessible description | Rule 17.11's plate, its caption ("its reason sits under it") and Rule 05.4's plate all set the reason under the control |
| `stage_c_ch17_build.py`, Rule 17.8 `failure.caption` (near line 1685) | `<strong>Fails 1.4.1.</strong>` | `<strong>Fails WCAG 2.2 SC 1.4.1.</strong>` | H11, and chapter 11's form (Rules 11.2 and 11.15) |
| `stage_c_ch17_build.py`, Rule 17.6 `failure.caption` | A hinge that comes to rest half a pixel low, … | `<strong>Fails Rule 17.6.</strong>` A hinge that comes to rest half a pixel low, … | Done by the maker at 02:59, before this list reached it: the other eleven failure captions in chapter 17 open this way, as chapters 05, 10 and 11 do. Nothing to apply |
| `stage_c_ch17_build.py`, Rule 17.4 `why.basis` (near line 1519) | Media Queries Level 5, W3C Working Draft, 19 February 2026 | Media Queries Level 5, W3C Working Draft, February 19, 2026 | H05, and the chapter's own source line writes it so |
| `stage_c_ch17_build.py`: `MECH_KICK` (791), the player's start line (782), the alts of `s-17-3-correct` (827), `s-17-4-correct` (866) and `s-17-4-failure` (897), Rule 17.4's caption (1521) and `sources[3]` (1929) | loop R1 | Loop R1 | H11's own example, "Loop R10, the safe-seat loop", and chapters 01 to 12, which capitalize every loop |
| `stage_c_ch17_build.py`, `sources[3]` (1929) | Source: our systems atlas, Who Do They Answer To?, loop R1, “Wealth and political influence reinforce each other”, its first link and its sentence. The player in Rule 17.4. | Source: Oath & Action’s systems atlas, Who Do They Answer To?, Loop R1, “Wealth and political influence reinforce each other”, snapshot of October 15, 2026. Its first link and its sentence, behind the player in Rule 17.4. | H04's order with the snapshot date every atlas line in chapter 01 gives (round 3, BE-S8); the last sentence takes the form of the chapter's other three lines |
| `stage_c_ch17_build.py`, Rule 17.7 `rule[0]` | …such as “Loading the tracker for S.99002.”, and a still drawing… | …such as “Loading the tracker for S.99002.” *Illustrative*, and a still drawing… (the label as the guide sets it) | H03: S.99002 is an invented bill (Rule 11.1's builders line numbers them so and asks for the label), and in the rule's text it stands away from its labeled plate |
| `stage_c_ch17_build.py`, the ten states' muted sample and its alt | Loop R1, in this view / Loop R2, outside this view | Either name each loop after its ID (V7: Loop R1, “Wealth and political influence reinforce each other”; Loop R2, “Congress becomes dependent on outside expertise”), or take a sample with no ID, as Rule 05.4's plate does with "Closed hearing" | H11: the plate prints two bare codes |
| `stage_c_ch17_build.py`, Rule 17.8 `builders[0]` (near line 1711) | …with the short role names, such as `<code>var(--oa-color-state-error-mark)</code>` and `<code>var(--oa-color-surface)</code>`, never a name that ends in a surface. | …with the short names, such as `<code>var(--oa-color-state-error-mark)</code>` for an error’s 4 px bar and `<code>var(--oa-color-surface)</code>`, never a name that ends in a surface. | Contradiction 3 in section 1d: the words call the glyph the error mark, and this token paints the bar. "Short names" is chapter 05's term (H02) |
| `stage_c_ch17_build.py`, the 17.3 failure plate's note and its alt (852 to 858) | One button with a play icon and no word. No Pause, no Reset and no still view. | One button with a play icon and no word. Pause, Reset and the still view are all missing. | W11: a run of three negatives |

**One contradiction for the systems designer's chapter 05, found through chapter 17.** Rule 17.10 sets two looks: a control that is pressed, checked or current takes the check, bold words and a 2 px edge, and a list's current place takes the selected band and its 4 px bar. Rule 05.4's plate draws Selected as "The paired surface, a 4 px bar and the selected check", the band and the check together, which matches neither. The round 1 brief makes Rule 17.8's plate the canonical one that `s-05-4-correct` points to, so Rule 05.4's Selected sample, its words and its spec should follow Rule 17.10 when chapter 05 is next built.

### B. Terms at first use (H02)

| Generator and string | Now | Mine |
|---|---|---|
| `stage_c_ch17_build.py`, Rule 17.9 `rule[0]`, first sentence (the guide's first "quiet") | Hover underlines a label, grows a link’s underline from 1 to 2 px, or thickens a quiet control’s edge from 1 to 2 px, and a filled button also steps its fill one shade. | Hover underlines a label, grows a link’s underline from 1 to 2 px, or thickens the edge of a quiet control, its word in ink inside a 1 px edge, to 2 px. A filled button also steps its fill one shade. (The definition is Rule 18.1's own.) |
| `stage_c_ch17_build.py`: Rule 17.2 `rule[0]` (1421), spec "Stagger" (1447), the token plate's line (726) and its alt (756) | a 40 ms stagger between siblings / 40 ms between siblings / The wait between siblings that move one after another. | a 40 ms stagger between marks that move one after another / 40 ms between marks that move one after another / The wait between marks that move one after another. (W18: "siblings" is the code's word for elements that share a parent) |
| `stage_c_ch17_build.py`, Rule 17.3 spec "Status line" (1492) | Polite; says Playing, Paused, and the words of the frame the motion stops on | Polite, so a screen reader waits until it finishes speaking; it says Playing, Paused and the words of the frame the motion stops on. (Rule 17.12's "one polite line" then reads as defined; the serial comma goes, as in the guide's other lists) |
| `stage_c_ch17_build.py`, Rule 17.11 `rule[0]` (1812) | …and its accessible description carries the reason. | …and its accessible description, the line a screen reader reads after its name, carries the reason. |
| `stage_c_ch17_build.py`, Rule 17.1 `why.text[0]`, last sentence (1391) | A vestibular disorder affects the inner ear’s sense of balance. | The vestibular sense is the inner ear’s sense of balance and motion. (The quote says "vestibular motion sensitivity", so the definition names the sense the quote names) |
| `stage_c_ch17_build.py`, Rule 17.8: `why.text[0]` (1678), `correct.caption` (1683), the ten states' alt (1116) | the role names a theme points at Newsprint or Charcoal / a role token that follows the theme / the same role tokens | the short names, which a theme points at Newsprint’s values or Charcoal’s / a short name that follows the theme / the same short names. (One term, chapter 05's, for one thing) |

### C. Voice

| Generator and string | Now | Mine | Rule |
|---|---|---|---|
| intro `[0]` (1896) | This chapter sets how each one moves and how it looks, and chapter 18 says where each component uses them. | This chapter sets how a motion runs and how each state looks, and chapter 18 says where each component uses them. | W01: "each one" covers a motion and a state, and only one of them moves |
| Rule 17.1 `rule[1]` | A reader’s own actions answer at once or within the fast 120 ms: hover, a toggle, a theme change. | A reader’s own actions, such as a hover, a toggle or a change of theme, answer at once or within the fast duration, 120 ms. | W06: the colon holds the actions back; W12: three items with no "and" read as a chant |
| Rule 17.1 `why.text[0]`, second sentence (1388) | Motion also costs some readers more than attention: the W3C’s Media Queries Level 5 describes the motion a reduced motion setting removes as motion that can “trigger discomfort for those with vestibular motion sensitivity, or distraction for those with attention deficits.” | For some readers motion costs more than attention. The W3C’s Media Queries Level 5 says the motion a reduced motion setting removes can “trigger discomfort for those with vestibular motion sensitivity, or distraction for those with attention deficits.” | W06: a setup line and a colon before the point |
| Rule 17.2 `rule[1]` | Fast, 120 ms, serves hover and toggles. Standard, 200 ms, serves reveals, panels, a mark that lands and a line that draws on its own. Slow, 320 ms, serves a move across a page or a component. A mark that arrives takes the enter easing, a mark that leaves takes the exit easing at the fast duration, and a mark that moves from one place to another takes the standard easing. | Hover and toggles take the fast duration, 120 ms. Reveals, panels, a mark that lands and a line that draws on its own take the standard 200 ms, and a move across a page or a component takes the slow 320 ms. The easing follows where a mark goes: the enter easing for a mark that arrives, the exit easing at the fast duration for one that leaves, and the standard easing for one that moves from place to place. | W13: three sentences on one frame, then three clauses on another |
| Rule 17.2 `correct.caption` (1438) | The six durations share one scale, the hinge’s 680 ms across the full width, and each easing is drawn as its curve. | The six durations share one scale, with the hinge’s 680 ms across its full width, and each easing is drawn as its curve. | W01 |
| `s-17-2-failure` alt (775) | …rises past the dashed line that marks the mark’s place by 10 percent… | …rises 10 percent past the dashed line where the mark should rest… | W01, and the plate's own words |
| Rule 17.3 `rule[0]` (1466) | It runs once and stops on its last frame, and nothing loops. | It runs once and stops on its last frame. | W07: "runs once" already says it, and the spec "Runs" says "never loops" |
| Rule 17.3 `rule[1]` (1471) | …so a reader who never presses Play, prints the page or listens with a screen reader gets every fact the motion shows. | …so every fact the motion shows reaches a reader who prints the page or listens with a screen reader, and one who never presses Play. | W01: "never" reaches across all three verbs, so read aloud it says the reader never prints the page |
| Rule 17.3 `why.text[0]` (1477) | Our motions last under a second and never start on their own, so none needs it, and every player gets the controls anyway, so a reader always decides when a mark moves. | Our motions last under a second and never start on their own, so none needs it. Every player has the controls all the same, and a reader decides when each mark moves. | W04: two "so"s chained; W17: "anyway" and "always" add force and no fact |
| Rule 17.3 `failure.caption` (1484), the failure plate's note (852) and its alt (858) | every 3 seconds | every three seconds | H06, and the same chapter's "five seconds" |
| Rule 17.4 `failure.caption` (1527) | The setting reaches tokens.css, the script never reads it, and a reader who asked for reduced motion still watches the link draw. | The setting reaches tokens.css, which the script never reads, so a reader who asked for reduced motion still watches the link draw. | W04: three clauses set side by side where one causes the next |
| Rule 17.5's three still views (909, 913, 917) | a straight move, slow, with the standard easing / the line extends from its start, standard, with the enter easing / from 112 percent to true size, standard, with the enter easing | a straight move over the slow 320 ms, with the standard easing / the line extends from its start over the standard 200 ms, with the enter easing / from 112 percent to true size over the standard 200 ms, with the enter easing | W01: "slow," and "standard," stand alone; Rule 17.1's still view already writes "over the standard 200 ms" |
| Rule 17.6 `rule[1]` | The ampersand and the lever keep signature red in every frame, which never counts as a view’s working red (Rule 05.3). | The ampersand and the lever keep signature red in every frame, and signature red never counts as a view’s working red (Rule 05.3). | W01: "which" can point back to the frame |
| `stage_c_identity_ch17.py`, Rule 17.6 `correct.caption` (433) and the lever extra's caption | Live. Press Play and OATH and ACTION settle… / Live. Press Play and the lockmark’s links draw… | Live. Press Play, and OATH and ACTION settle… / Live. Press Play, and the lockmark’s links draw… | W01: read aloud, "Play and OATH and ACTION" runs into one list |
| Rule 17.7 `why.text[0]`, first sentence (1636) | A pulse repeats for as long as the wait lasts, which puts it under WCAG 2.2 success criterion 2.2.2 Pause, Stop, Hide once the wait passes five seconds, and our fifth edition’s pulsing lever fell to 1.27 to 1 against Newsprint at its faintest, under the 3 to 1 a needed graphic takes. | A pulse repeats for as long as the wait lasts, which puts it under WCAG 2.2 success criterion 2.2.2 Pause, Stop, Hide once the wait passes five seconds. Our fifth edition’s pulsing lever also fell to 1.27 to 1 against Newsprint at its faintest, under the 3 to 1 that success criterion 1.4.11 asks of a graphic a reader needs. | W03: two reasons in one 53-word sentence; W01: "a needed graphic takes" |
| Rule 17.7 `failure.caption` and the plate's note (1185) | It fades between 20 and 50 percent… / The disc fades between 20 and 50 percent every 1.2 seconds… | It fades between 20 and 50 percent strength… / The disc fades between 20 and 50 percent strength every 1.2 seconds… | W01: percent of what; the alt already says "strength" |
| Rule 17.9 `rule[1]`, last two sentences (1729) | …so the 2 px gap of Charcoal between them is what shows the ring. Keep the gap there, always. | …so the 2 px gap of Charcoal between them shows the ring. | W06: "is what" holds the verb back; W07 and W17: the last line restates the spec's "never 0" with "always" for force |
| Rule 17.9 `builders[0]`, last sentence (1761) | An outline stays under forced colors; a box shadow does not. | Forced colors keeps an outline and removes a box shadow. | W10: a matched pair |
| Rule 17.10 `rule[0]` | …the selected check before the word, the word in bold, and a 2 px edge… | …the selected check before the word, the word in bold and a 2 px edge… | The guide's lists take no comma before "and" |
| Rule 17.11 `rule[1]` (1814) | A send that cannot run yet keeps focus and says why beside it. | A Send button that cannot run yet keeps focus and says why under it. | W01; the place follows row 4 of A |
| Rule 17.11 `why.text[0]` (1821) | WCAG 2.2 success criterion 1.4.3 sets no contrast for an inactive control’s text, and we hold it to the same 4.5 to 1 as any other words. | WCAG 2.2 success criterion 1.4.3 exempts an inactive control’s text from its minimum, and we hold that text to the same 4.5 to 1 as any other words. | W09: say what the criterion does; 1.4.3 lists the text of an inactive component under "Incidental" |
| Rule 17.12 `why.text[0]` (1859) | …a count of 0 alone leaves a reader with no way on. | …a count of 0 alone leaves a reader with nothing to try next. | W01 |
| Rule 17.1's player: the status lines (607, 608), `s-17-1-correct`'s alt (632, 635) and `s-17-3-failure`'s alt (855, 856) | Steps 1 to 2 done … steps 5 to 6 not yet | Steps 1 and 2 done … steps 5 and 6 not yet | W01: a screen reader says "1 to 2" for two steps |

### D. Read and left as they are

- Rule 17.5's three definitions open "A slide…", "A draw…" and "A land…". Each defines its term at first use (H02), and the three sentences take different shapes after their subject, so W13 does not apply.
- Rule 17.8 `rule[0]` repeats the intro's point about gray print, a dark theme and a reader who sees no color. A rule is read on its own, so it keeps the reason.
- The two quotes from Media Queries Level 5 in Rules 17.1 and 17.4 match the W3C's words as the research notes give them, and Rule 17.4 quotes the full sentence once.
- Rule 17.6's hinge and lever alts in `manifest-identity.json` read plainly and say every step with its time; they need nothing.

## 3. What remains, by type

Counted by the main rule each row of sections 1 and 2 serves, until the owners apply them: 59 rows in all.

| Type | Rows |
|---|---|
| A rule and its demonstration or its facts disagree (1d's items 1 and 2, the Rule 09.1 gap and opener alt, chapter 17's count of 124, chapter titles, reason line, and "beside" against "under") | 9 |
| W01, a sentence a listener has to read twice | 22 |
| H02, a term with no definition or two names for one thing | 8 |
| W04, thoughts set side by side with no joining word | 3 |
| W06, a setup or a colon before the point | 3 |
| H11, a bare ID or a criterion with no name | 3 |
| W03, W07, W09, W10, W11, W13, H03, H04, H05, H06 and the guide's list comma, one each | 11 |
| Em dashes, en dashes and the listed fillers, hedges and corporate verbs, by script | 0 |

Applied this round: one W06, CL-075's sentence in my table.

### 3b. Sections 4 to 6, by type

Counted the same way, by the main rule each row serves: 67 rows.

| Type | Rows |
|---|---|
| A rule, its plate, its code or the ledger disagree (a count, a name, a weight, a place, a rule number) | 31 |
| W01, a sentence a listener has to read twice | 7 |
| W09, a "never" or "not" turn | 5 |
| W10, a matched pair | 4 |
| W20, a claim larger than its evidence | 4 |
| H04, a source line with no retrieval date or two forms of one source | 4 |
| H11, a loop or criterion code in the wrong form | 2 |
| W18, a studio or code word in reader text | 2 |
| W06, W08, W13, H02, H03, H06, chapter 02's scope line and studio words in a download, one each | 8 |
| Em dashes, en dashes and the listed fillers, hedges and corporate verbs, by script | 0 |

## 4. Chapter 18, Components and interaction: edits for its makers

**What I read.** `18-components.json` as `stage_c_ch18_build.py` wrote it at 03:42 (unchanged at 03:57), every rule whole in a strict scratch build (0 warnings, 185 rules); the 24 failure alts in `manifest-components.json`; the 24 anatomy plates' keys and alts (`stage_c_ch18_anatomy_build.py`, `manifest-anatomy.json`); and the visible words of the 24 code sets (`c-18-*.html`, with their scripts' status words). I checked the words against the code itself: where a rule, its anatomy key and its code disagree, the row says which one the code bears out. Every rule number the chapter cites exists in the page, and every chapter title it prints matches. Its figures hold: the contrast ratios against `tokens.json`, Prussian against Charcoal at 1.41 to 1, tokens.css at 93,235 bytes (93 KB), and the 125 symbols.

### 4a. For the accessibility lead (`stage_c_ch18_build.py`): facts and contradictions first

| Key | Now | Mine | Rule |
|---|---|---|---|
| Rule 18.1 `rule[1]` | …draws a dashed edge and points to a line beside it that says why… | …draws a dashed edge and points to a line under it that says why… | The code sets the reason under the button (`c-18-button.html`), as Rule 17.11 and Rule 05.4's plate do |
| Rule 18.6 `rule[0]`, second sentence | The link to the part the reader is in carries `aria-current="page"` and a 2 px underline. | The link to the part the reader is in carries `aria-current="page"`, bold words and a 2 px underline. | The code sets the current part bold and underlined (`c-18-masthead.css`, `[aria-current]`), and the anatomy key says "Bold, with a 2 px underline" |
| Rule 18.6 spec "States" | Current part: a 2 px underline and aria-current. Hover: a 2 px underline. | Current part: bold words, a 2 px underline and aria-current. Hover: a 1 px underline. | The code's hover underline is `--oa-border-width-underline`, 1 px, so it stays apart from the current part's 2 px |
| Rule 18.6 `rule[0]` and spec "Accessible name" | such as “Parts” | such as “Parts of the site” | The code's label (`aria-label="Parts of the site"`) and the anatomy key |
| Rule 18.7 `rule[0]`, last clause | …a short list in a line, such as a breadcrumb, sets the current place in bold words while the places before it stay links. | …a short list in a line, such as a breadcrumb, ends on the current page as a link in bold words, with aria-current and no underline, after the links to the places before it. | The code's current crumb is a link with `aria-current="page"`, and anatomy key 1 says "its link says it is the page" |
| Rule 18.9 spec "States" | Not selected: regular words and no bar. | Not selected: words at 600, the weight every control's word takes, and no bar. | The code sets every tab in `--oa-type-ui`, 600, and Rule 17.10's spec says "600 when off" |
| Rule 18.9 spec "A screen reader hears" | …and its place, such as 2 of 3. | …and its place, such as 2 of 4. | The live set holds four tabs |
| Rule 18.11 `rule[1]`, `correct.caption` and `builders[0]` | Its focus ring sits inside the frame… / the focus ring drawn inside the frame / Draw the ring inside the frame with `outline-offset: -2px` plus the ring’s width | Keep the words, and the component engineer moves the ring inside (4d); or, if the ring stays outside, "Its focus ring sits 2 px outside the frame’s edge" and a builders line that drops the negative offset | The code draws the ring 2 px outside (`c-18-scroll-region.css`: `outline-offset: var(--oa-border-focus-offset)`, 2 px), and the anatomy plate draws the code. The rule gives a reason for inside, so I recommend the code follow the words. "−2 px plus the ring’s width" also needs to be one figure: −4 px, the ring's 2 px and its 2 px gap |
| Rule 18.18 `title` | Give every message its mark, its first word and its bar, and announce only what changes. | Give every message its mark and its first word, and announce only what changes. | A success takes no bar in the code, and anatomy key 6 says "with no bar"; `rule[0]` already says which messages take one |
| Rule 18.18 `correct.caption` | …its words, its 4 px bar, and the Error Band behind an error on Newsprint. | …its words, the 4 px bar on an error or a warning, and the Error Band behind an error on Newsprint. | As the title |
| Rule 18.20 `rule[0]` and spec "States" | …one state word: Done, Now, Not yet, Never happened or Stopped (Rule 11.2). / …Stopped (Rule 11.2) | …one state word: Done, Now, You can take part now, Not yet, Never happened or Stopped (Rules 11.2 and 11.4). / …Stopped (Rules 11.2 and 11.4) | The spec lists six words and the rule five; "You can take part now" is Rule 11.4's |
| Rule 18.24 `rule[1]` | A chip that opens its record is a link, with an underline on hover and a target at least 24 px tall… | A chip that opens its record is a link, underlined as Rule 18.5 sets, 1 px at rest and 2 px on hover, with a target at least 24 px tall… | The code underlines a linked chip at rest (`c-18-id-chip.css`, `.oa-chip--link`) |
| Rule 18.24 spec "States" | Plain. As a link: hover, an underline; focus, the ring. | Plain. As a link: a 1 px underline, 2 px on hover; focus, the ring. | As above |
| Rule 18.24 spec "Light and dark" | The edge in --oa-color-border-hairline and the words in the text’s ink. | The edge, a hairline in --oa-color-border-strong, and the words in the text’s ink. | The code draws the edge in `--oa-color-border-strong`, as anatomy key 3 says |
| `s-18-22-failure` alt | A panel at 360 px for loop R1 from our systems atlas… | A panel at 360 px for Loop R1 from our systems atlas… | H11's form, which chapter 17 now prints |
| `s-18-24-failure` alt | A sentence at 360 px from our systems atlas, “R10 shifts accountability to small primary electorates, and R-01 sits on that loop.” | A sentence at 360 px written from our systems atlas’s records, “R10 shifts accountability…” | W20: the atlas holds no such sentence; Loop R10's title is "Safe seats shift accountability to small primary electorates", and Reform R-01's record names R10 among its loops |
| `sources[3]` | …built November 2, 2026, read November 11, 2026. | …built November 2, 2026, retrieved November 11, 2026. | H04's word, as the chapter's other four lines use it |

**One contradiction for the systems designer's chapter 17, found through chapter 18.** Rule 17.10 says "A link to the page a reader is on takes a 2 px underline, and a rail or a list takes the selected band with its 4 px bar", and its spec "Current place" says the same. Chapter 18's code, which its Rules 18.6 and 18.7 describe, draws three looks: a masthead's current part in bold with a 2 px underline, a breadcrumb's current page in bold with no underline, and a list's current place on the band with its 4 px bar and bold words. Chapter 17's own plate sets that list item at 600 (`.sx-cur`), where chapter 18 and Rule 17.10's own spec make "on" 700.

| Generator and string | Now | Mine | Rule |
|---|---|---|---|
| `stage_c_ch17_build.py`, Rule 17.10 `rule[1]`, second sentence | A link to the page a reader is on takes a 2 px underline, and a rail or a list takes the selected band with its 4 px bar. | A link to the page a reader is on takes bold words, with a 2 px underline in a masthead and none at the end of a breadcrumb, and a rail or a list takes the selected band, its 4 px bar and bold words. | Rules 18.6 and 18.7 and their code |
| `stage_c_ch17_build.py`, Rule 17.10 spec "Current place" | A link: 2 px underline; a rail or list: the selected band and its 4 px bar | A link: bold words, with a 2 px underline in a masthead; a rail or list: the selected band, its 4 px bar and bold words | As above |
| `stage_c_ch17_build.py`, Rule 17.10's plate, the list's `.sx-cur` | `font-weight:600` | `font-weight:700`, from `--oa-font-weight-bold` | Rule 17.10's own spec: "Bold, 700; 600 when off" |

### 4b. For the accessibility lead: voice

| Key | Now | Mine | Rule |
|---|---|---|---|
| intro `[1]`, second sentence | What a screen reader hears is what the code hands it, the name, the role, the state and any status line, and each screen reader words these its own way. | A screen reader hears the name, role, state and status line the code hands it, and each screen reader words these its own way. | W06: "is what" holds the point back |
| `sources[1]`, last sentence | The Practices show one tested way to build each control; WCAG sets what must hold. | The Practices show one tested way to build each control, and WCAG sets what each must meet. | W10: a matched pair |
| Rule 18.1 `why.text[0]`, second sentence | The disabled attribute would take the button out of the Tab order and hide its reason with it, where aria-disabled keeps both in reach. | The disabled attribute would take the button out of the Tab order and hide its reason with it, so an unavailable button carries aria-disabled, which keeps both in reach. | W10: "where" sets the two against each other |
| Rule 18.3 `builders[0]` | Hide the native radio with a visually hidden style that keeps it focusable, never with `display: none`, and draw… | Hide the native radio with a visually hidden style that keeps it focusable, since `display: none` would take it out of the Tab order, and draw… | W09: say why, without the "never" turn |
| Rule 18.5 spec "Target" | …which WCAG 2.2 SC 2.5.8 excepts… | …which WCAG 2.2 SC 2.5.8 exempts… | W18 |
| Rule 18.15 `why.text[0]`, first sentence | A visible label stays when the reader types, where a placeholder vanishes. | A placeholder vanishes at the first letter typed, so the label sits above the field, where it stays in view. | W10 |
| Rule 18.17 `rule[0]`, last sentence | …a send that cannot run yet keeps focus and says why, as Rule 18.1 sets. | …a Send button that cannot run yet keeps focus and says why, as Rule 18.1 sets. | W01, and Rule 17.11's wording |
| Rule 18.19 `why.text[0]`, first sentence | Words tell every reader what is happening, where a spinner shows only that something is, and a pulse moves without end. | Words tell every reader what is happening. A spinner shows only that something is happening, and a pulse moves without end. | W10 and W03 |
| Rule 18.22 `rule[1]` | …and never under 6 seconds… | …and never under six seconds… | H06 |

### 4c. For the systems designer, the anatomy keys (`stage_c_ch18_anatomy_build.py`)

| Plate and key | Now | Mine | Rule |
|---|---|---|---|
| `s-18-02-anatomy`, key 4 | Off: word. The same word in regular weight, with no check | Off: word. The same word at 600, the weight every control's word takes, with no check | Fact: the chip's word is `--oa-type-ui`, 600 (Rule 17.10: "600 when off"); regular is 400. The alt follows |
| `s-18-24-anatomy`, key 5 | As a link. It opens the record; its words underline under a pointer, as here | As a link. It opens the record; its words keep a 1 px underline, 2 px under a pointer, as here | Fact: the code underlines a linked chip at rest |
| `s-18-11-anatomy` and its alt | The ring as the code draws it, 2 px outside the frame | Follows the call in 4a's Rule 18.11 row; a rerun picks it up | Rule and plate agree once the code does |
| `s-18-05-anatomy`, key 2 | Words. Say where the link goes, and work read on their own | Words. Say where the link goes, and make sense read on their own | W01 |

### 4d. For the component engineer (`work/build/guide/code/c-18-*`)

| File and words | Now | Mine | Rule |
|---|---|---|---|
| `c-18-download.html`, the file that is not ready | Download the swatch file, ASE / The swatch file comes with the final tokens. | Download the hearing report, PDF / The report comes after the hearing on March 3. (with the Illustrative label the ready file carries) | Fact: DR-214 ships tokens.css and tokens.json only, so the example promises a file nobody plans |
| `c-18-tracker.html` and `.js`, the update that stops | Stopped at step 3 of 6: Committee vote, on March 10. The committee voted against the bill. (for S.99002) | The same stop for another of chapter 11's invented bills, such as H.99004, Records request fees, which chapter 18's own table already shows as "Stopped in committee" | Contradiction: chapter 17's Rule 17.1 moves S.99002 past its committee vote to step 4, and chapter 18's notes hold that one invented bill means one thing across the guide |
| `c-18-tabs.html`, the title | Bill S.99002, school bus contracts | Bill S.99002, School bus contracts | The bill's title as chapters 11 and 17, the tracker and the table print it |
| `c-18-loop-stepper.html` and `.js`, the reason line | At the start, so Previous step and Reset the loop wait until you move on. | Previous step and Reset the loop work once you press Next step or Play. | Rule 17.11's builders line, and chapter 17's players now say "Reset works once you press Play." |
| `c-18-loop-stepper.html` and `c-18-diagram-controls.html`, the kicker | From our systems atlas, loop R1 | From our systems atlas, Loop R1 | H11's form, as chapter 17 now prints it |
| `c-18-report-reader.html`, the hint | Wider than this column. Scroll the page sideways to see all of it. | Wider than this column. Scroll the report page sideways to see all of it. | W01: Rule 18.11 says the page never scrolls sideways; here "page" means the report's page |
| `c-18-scroll-region.css`, the ring | `outline-offset: var(--oa-border-focus-offset)` | A negative offset of the ring and its gap, −4 px, if the accessibility lead keeps the ring inside (4a) | Rule 18.11 |

### 4e. Read and left as they are

- Each of the loop stepper's three steps opens with a short line of its own, then quotes Atlas V7's own sentence for L01, L02 or L03 word for word, and the verbs hold the grades: L02 is plausible and takes "can raise" (H08); L01 and L03 are well supported.
- The table's "No bills match. Clear the search or the filters to see all 12 bills." counts bills the four-row example does not show; the example carries the Illustrative label, so it stands.
- The "Updated!" in Rule 18.20's failure and the "click here" in Rule 18.5's are the faults the plates teach.

## 5. Chapter 19, Accessibility: edits for its maker (the accessibility lead, `stage_c_ch19_build.py`)

**What I read.** `19-accessibility.json` as written at 03:46 (unchanged at 03:57), its 18 plates and alts, the guide's own line for each of the 55 criteria (the `c19-m` lines), the matrix, the results and the device script. W3C's quoted criterion text I left exactly as W3C wrote it. The counts hold: WCAG 2.2 has 31 criteria at A and 24 at AA once 4.1.1 is removed, six of them new, and the map's 37, 5, 8 and 5 make 55. Master Brief section 22 has 14 checks, as Rule 19.7 says, and the results plate keeps Tested and Not tested apart.

### 5a. Facts and contradictions

| Key | Now | Mine | Rule |
|---|---|---|---|
| Rule 19.1 `rule[0]`, second sentence | Every page and product we publish meets all of them. | Build every page and product we publish to meet all of them. | W20: `rule[1]` counts eight gaps, and Rule 19.8's results list open faults, so the present tense claims a result the chapter's own results contradict |
| The criteria list, 3.3.4 and 3.3.7 (`stage_c_ch19_build.py`, lines 139 and 140) | …chapter 22 if one sends testimony, gifts or petitions. / …chapter 22 when one does. | …chapter 18 if one sends testimony, gifts or petitions. / …chapter 18 when one does. | Fact: chapter 22 is Newsletter and email; the round 0 map gave both to chapter 18, where forms live. The maker to confirm, or name chapter 20 |
| The criteria list, every line with one rule (1.3.3, 1.3.4, 1.3.5, 1.4.2, 1.4.5, 1.4.12, 2.1.4, 2.5.2, 2.5.4, 2.5.7) | Rules 19.3. | Rule 19.3. | W01 |
| The criteria list, every line with several rules | Rules 18.10, 18.3, 18.17, 18.6, 18.7, 11.5. | Rules 11.5, 18.3, 18.6, 18.7, 18.10 and 18.17. | W01: in the page's order, with "and" before the last, as the guide sets its lists |
| Rule 19.4 `rule[0]`, last sentence | The wordmark is the one picture of text a page holds. | The wordmark and its lockups are the only pictures of text a page holds. | The rule's own spec, "Allowed as an image: The wordmark and the lockups (chapter 03)" |
| `sources[2]` | Sources for Rule 19.9: Apple, “Turn on and practice VoiceOver on iPhone” and …; Microsoft, “Change color contrast in Windows”. The steps name the menus as each maker does; makers rename them between versions. | Further reading for Rule 19.9, each maker’s own guide: Apple, …; Microsoft, “Change color contrast in Windows”. We wrote the steps from these makers’ menus as we know them and did not check them on a device; makers rename menus between versions. | H04 asks for a retrieval date, and the maker's notes say the steps came from what it knows, with no page read, so "Sources" claims more than happened. If the pages were read, keep "Sources" and add the date instead |
| `s-19-6-correct` and `s-19-6-failure` alts | An Illustrative pair of buttons… / (the manifest marks both not illustrative) | Drop "Illustrative" from the alt, or set the flag | H03 labels invented content a reader could take for real; two page buttons need no label, but alt and flag must agree |
| Rule 19.9 `rule[0]`, first sentence, and the results plate's last Not tested line | Four short scripts check what no container can… / This container has none of them… | Four short scripts check what no automated test can… / The machine these checks ran on has none of them… | W18: "container" is the studio's word for its build machine |
| intro `[0]`, second sentence | …from W3C, the body that writes the web’s standards. | …from the World Wide Web Consortium, W3C, which writes many of the web’s standards. | W20: HTML itself comes from WHATWG, which chapter 18 cites; H02: spell out W3C at its first use |

### 5b. Voice

| Key | Now | Mine | Rule |
|---|---|---|---|
| Rule 19.3 `title` | Name a control or a step by its words, never only by its color, shape or place. | Name a control or a step by its words, and add its color, shape or place only after them. | W09 |
| Rule 19.3 `rule[0]`, second sentence | Color, shape and place can add to the words, as in “Send your comment, under the form”, and never stand in for them, since a phone moves things and a screen reader or a contrast theme drops color. | Color, shape and place can follow the words, as in “Send your comment, under the form”, since a phone moves things, and a screen reader or a contrast theme loses color. | W09 |
| Rule 19.5 `rule[0]`, second sentence | A gesture with two fingers, a drag, a tilt or a shake may add a way, never the only one. | A gesture with two fingers, a drag, a tilt or a shake may add a second way beside that control. | W09 |
| Rule 19.6 `why.text[0]`, second sentence | Words that may not wrap are the most common way a page loses them. | A label that may not wrap is how this guide’s own pages lost words when we first tested them at 200 percent. | W20: "most common" counts nothing; the round 0 inventory found clipped labels (its F-2) |
| The device script, iPhone step 1 | …pressing the side button three times turns VoiceOver on and off. | …pressing the side button three times, or the Home button on an iPhone that has one, turns VoiceOver on and off. | Fact: an iPhone with a Home button takes the shortcut there |
| The device script, iPhone and Android step 4 | To type, double-tap a field, type, then swipe on. | To type, double-tap a field, type, then swipe right to move on. | W01 |
| The device script, last line | A fail with its words is as useful as a pass. | Write a fail down with the words you heard, so the builder can find what broke. | W08: a closing line that carries no step |

## 6. Chapter 26, Tokens and how to choose them: edits for its maker (the engineer, `stage_c_ch26_build.py` and the `c-26-*` code sets)

**What I read.** `26-tokens.json` as written at 03:06. The generator changed at 03:49, after its last output, so a row may already be done; each quotes its string. Its figures hold: tokens.json and tokens.css hold the same 500 tokens (tokens.css adds 212 short names and type parts), 13 categories, body type 17 px at 1.6, tokens.json 278 KB, version `6.0.0-gate2.7`, and the change note at the top of tokens.css. Rule 26.5 now gives the two switch lines that section 1d asked for.

### 6a. Facts and contradictions

| Key | Now | Mine | Rule |
|---|---|---|---|
| `c-26-warning.html` and `s-26-4-4-correct`'s alt | Step 4 of 6: in committee | Step 2 of 6: Hearing | Fact: Rule 11.1's step 4 is First chamber, and the warning is about the hearing ("The hearing moved to March 12") |
| intro `[0]`, first sentence | …a named value kept in one file that the guide, the asset package and every product read. | …a named value kept in the token files, which the guide, the asset package and every product read. | The next paragraph and Rule 26.8 name two files |
| Rule 26.3 `rule[0]`, second sentence | Then its role: text, graphic, border, focus, data, action or state. | Then its role: text, graphic, border, focus, data, action, state or field. | The rule's own spec lists eight roles; the field ground is D2-1193's |
| `sources[0]` to `sources[3]` | No retrieval date; `sources[2]` and `[3]` give no date at all | Each ends with its retrieval date, and Media Queries Level 5 takes "W3C Working Draft, February 19, 2026", as chapter 17 prints it | H04 |
| `sources[1]` | W3C, “Web Content Accessibility Guidelines (WCAG) 2.2”, Recommendation, October 5, 2023, updated December 12, 2024 | W3C, “Web Content Accessibility Guidelines (WCAG) 2.2”, W3C Recommendation, December 12, 2024 | One form for one source, as chapters 17, 18 and 19 print it |
| Rule 26.5 `rule[2]` | …the two lines that show the pixel fit on a standard screen and the master on a sharper one… | …the two lines that show the pixel fit on a screen under 2x and the master from 2x… | H02: the term Rules 09.3 and 10.4 define |
| The header of `tokens.css` (the token build's source, `oa-tokens.src.mjs`) | …Version 6.0.0 ships when Dustin approves the token files at Gate 2… (DR-204)… | The version and what it means, with no person's name, gate or decision code | Builders download this file; chapter 26 already strips studio codes from the table for the same reason. For Phase 3's package, low priority |

### 6b. Voice

| Key | Now | Mine | Rule |
|---|---|---|---|
| Rule 26.2 `rule[0]` | A new token joins tokens.json only when all five hold. First, a measured need… Second, a value… Third, one job… Fourth, contrast… Fifth, a description, a tier and a status. | A new token joins tokens.json only when all five hold: a measured need that no token meets, registered with an ID and its evidence; a value made from one palette color, mixed in OKLab toward Newsprint or Charcoal, with the amount recorded; one job, said in one sentence; contrast that passes on every surface it serves, at the threshold its kind needs, with the ratio stored; and a description, a tier and a status. | W13: five sentences on one frame |
| Rule 26.3 `why.text[0]`, first sentence | Each step narrows the choice by a fact about the page, never by taste, so two builders reach the same token. | Each step narrows the choice by a fact about the page, so two builders reach the same token. | W09 |
| Rule 26.4 `rule[0]`, first sentence | Four parts every product needs, each chosen by the five steps of Rule 26.3, at actual size beside its failure, with code to copy. | The four examples below take parts every product needs through the five steps of Rule 26.3, and set each at actual size beside its failure, with code to copy. | Chapter 02's scope line: outside headings, labels, captions and chart keys, every line is a full sentence |
| Rule 26.7 `why.text[0]` | …and a value typed by hand never hears about the next release. | …and a value typed by hand stays as it was when the next release changes the token. | W01 |

### 6c. Read and left as they are

- Chapter 26's failure alts for Rules 26.1 to 26.3 and 26.5 to 26.8 open on the fault, where Rule 26.4's open "Failure case: do not publish." That follows the guide's practice: an alt opens with the band's words only where the plate draws the band, and those seven draw none, as most failure plates in chapters 01 to 12 draw none.
- Rule 26.3 walks its five steps in order ("Then its role… Then its emphasis… Then its state…"). It is a procedure, and the order is the point, so the repeated "Then" stays.

## For the main session

- **Chapter 10.** Run `python3 -I work/build/scripts/phase-2/stage_b_ch10_build.py --no-draw` once, so `s-10-lib-03.html` takes CL-075's sentence from my table (1a). My scratch run shows it changes that one file only.
- **Rules 09.3 and 10.4 (1d, item 1).** Ask the engineer whether `tokens.css` should carry the two switch lines. If it does, the builders lines in 1b and 1c say "tokens.css switches them" in place of the CSS; if not, they print the CSS as written there.
- **Rule 11.12 and Rule 18.15 (1d, item 2).** Ask the accessibility lead and the systems designer to settle one markup for the search landmark; my words in 1b follow the `search` element.
- **Chapter 17.** Pass section 2 to the systems designer (`stage_c_ch17_build.py`) and its two `stage_c_identity_ch17.py` rows to the identity designer. Every row quotes its string, so a row the maker has already rewritten can be skipped.
- **Chapter 26 (1d, item 3).** When I write its words I will describe `--oa-color-state-error-mark-on-<surface>` as the error bar's color.
- **Sections 4 to 6.** Pass 4a, 4b and 5 to the accessibility lead; 4c and the three Rule 17.10 rows in 4a to the systems designer; 4d to the component engineer; 6 to the engineer. Two rows need a call before words: Rule 18.11's focus ring, inside the frame as the words say or outside as the code draws it (I recommend inside), and the owner of criteria 3.3.4 and 3.3.7 (I recommend chapter 18, as round 0 set it).
- **Chapter 26 came to me as a finished draft.** The round 1 brief had me write its words beside the engineer; section 6 is my edit of the engineer's words instead.

## Routine calls

- D2-xxx | CL-075's row joins my label table with the addendum's label and other fields as written and its meaning recast with no colon; the counts rise to 125 and an `updated` line says why | DR-185 and D2-1279 make the table the words' home; none of its other 124 sentences uses a colon (W06)
- D2-xxx | I tested the CL-075 change by running chapter 10's generator in a scratch copy of the tree and left the run in the project to the main session or the systems designer | The generator writes the systems designer's files; the scratch run shows one specimen and one sentence change
- D2-xxx | Chapter 05 carries the guide's first definition of forced colors, in Rule 17.8's own words | H02 asks for the definition at first use, and one wording keeps the term the same in both chapters
- D2-xxx | Rules 09.3 and 10.4 print the two CSS lines that switch a fit and its master, unless the engineer puts them in tokens.css | A builder who copies the svg alone shows both drawings
- D2-xxx | Rule 11.12's search landmark follows Rule 18.15's `search` element, pending the accessibility lead's call | Chapter 18 is the component's home (the stage C brief's "One component, two homes")
- D2-xxx | "Short names" stays the guide's term for the color names a theme or surface class points at a value, as chapter 05 sets it | Chapter 17 used three names for one thing (H02)
- D2-xxx | Chapter 17's empty-state count reads the inventory in use | The set grew to 125 and the typed 124 went stale (D2-1278's reason)
- D2-xxx | Chapter 17's edits go to its makers as a list to apply in their generators, each row quoting its string; I edited no chapter 17 file | The maker is still writing (round 1 brief, item 6)
- D2-xxx | Rule 05.4's Selected sample follows Rule 17.10 at chapter 05's next build | The round 1 brief makes Rule 17.8's plate the canonical one, and Rule 17.10 sets the look
- D2-xxx | Where a chapter 18 rule, its anatomy key and its code disagree, the words follow the code, except Rule 18.11's ring, where the rule gives a reason and the code should follow it | The code is what a builder copies; Rule 18.11 says why the ring belongs inside
- D2-xxx | Rule 17.10 names three current-place looks, a masthead's, a breadcrumb's and a list's, all with bold words, and its plate's list item takes 700 | Chapter 18's code draws all three, and Rule 17.10's spec makes "on" 700
- D2-xxx | One invented bill keeps one story across the guide, so chapter 18's tracker stops H.99004 in committee and leaves S.99002 to chapter 17's story | Chapter 17 moves S.99002 past its committee vote, and chapter 18's notes set the principle
- D2-xxx | The criteria list writes "Rule" for one rule and lists several in page order with "and" before the last | The guide's list form, read aloud
- D2-xxx | A failure alt opens "Failure case: do not publish." only where its plate draws the band | The guide's practice in chapters 01 to 26, checked across all eight manifests
- D2-xxx | W3C's quoted criterion text in chapter 19 is left exactly as printed; only the guide's own words around it are edited | The main session's instruction and H01's principle for quotations

## Questions for Dustin

None this round, in either pass. Every item above is a routine call inside the approved phase, and none touches a locked line or the identity's geometry. The locked lines are exact: in the 02:57 build the tagline appears 13 times, the mission four, the reader promise four and the editorial commitment ten, each word for word, with no near miss.

## Tested

- Two scratch builds of the guide with `guide_build.py --strict --out` (02:43 and 02:57). Each wrote the page (14 chapter files, 168 rules, 379 specimens); `--strict` exits 1 on chapter 18's missing anatomy plates and code sets only, which other makers are still writing.
- Every string that differs from 820340a7 in chapters 03, 05, 08, 10 and 11 and in two manifests, listed by script, and the visible text of each changed specimen beside its old text. Then each changed rule read whole in the built page.
- Rule 08.2's printed feed figures against `20261111_Promotion-C-Identity-Figures.json`, keys `feed`, `feed_dark` and `feed_thumbnail`: all match. The dark floors' midpoints are 155.5 and 192, printed as 155 and 190.
- The print L3's 0.269 in and 3.13 mm in `s-03-minimums`, from its view box by arithmetic: match.
- Rule 10.9's new likeness figures against the icon designer's two runs: match (0.897; 0.917 and 0.915).
- CL-075: my table parses with 125 rows and 20 topics, and a diff shows only the new row, the counts and the `updated` line. Chapter 10's generator run with `--no-draw` in a scratch copy of the tree changed one output, `s-10-lib-03.html`, and only CL-075's sentence; the other 34 outputs (26 specimens, five sheet images and three JSON files) came out byte for byte.
- That the switch classes `oa-at-1x` and `oa-at-2x` are set in `guide-shell.css` and absent from `tokens.css`.
- Chapter 17's contrast figures against its figures file (all match); its timings by sum; `tokens.css`'s reduced motion block; Atlas V7's grade for Loop R1's first link (L01, well supported); the guide's titles for chapters 16 and 18; the Media Queries Level 5 quote against the research notes; WCAG 1.4.3's "Incidental" exception in the research notes; where chapters 17 and 18 define forced colors and a quiet button; which chapters open failure captions with "Fails".
- A script scan for em and en dashes and the listed fillers, hedges, corporate verbs and throat-clearing phrases across chapter 17, `manifest-motion.json`, the changed chapters, both label files and these notes: no real hit. The one run of negatives (W11) I found by reading.
- The four locked lines across the whole 02:57 build, by script: every use word for word, and no sentence that opens like one and then departs from it.
- **Second pass (03:47 to 04:01):** a strict scratch build of all 16 chapters (9,538,958 bytes, 185 rules, 420 specimens, 0 warnings); every rule number chapters 18, 19 and 26, their manifests and the 24 code sets cite, checked against the page's rule ids (all exist); every chapter title they print, against the page and the build's chapter table; chapter 18's figures against tokens.json and the files (1.41 for Prussian against Charcoal, 93 KB for tokens.css, 125 symbols, Deep Stone and Dim Newsprint for the secondary text); each disagreement between a rule, its anatomy key and its code read in the code itself (the button's reason line, the masthead's current part and hover, the breadcrumb's current link, the chip and tab weights, the scroll frame's ring, the ID chip's edge and underline, the success message's bar); WCAG 2.2's counts by level and the six new criteria; Master Brief section 22's 14 checks; the round 0 map's owner for 3.3.4 and 3.3.7; tokens.json's 500 tokens against tokens.css's 712 names; the body type's 17 px and 1.6; the top of tokens.css; the loop stepper's sentences against Atlas V7's L01 to L03; the failure alt openings in all eight manifests against whether each plate draws the band; and a script scan of the three chapters, four manifests and the code sets' visible words for dashes and the listed words (no real hit).
- My own text in these notes, read against chapter 02's rules.

## Not tested

- Chapter 10 rebuilt in the project. I ran its generator only in a scratch copy.
- Chapter 17 after 02:59 and chapters 03 and 08 after 03:02. The makers are still writing, and anything later is unread.
- The live players in a browser: their motion, Pause, Reset, slow motion and reduced motion. I read their words only.
- How any of the new words sound read aloud to a real reader, or through a screen reader.
- `guide_check.js`, which I did not run.
- Rhetorical triplets and parallel runs, which I checked by reading; no script can rule them out.
- Chapter 18's words, which are not in this round's task for me. (Superseded: section 4 reads them in the second pass.)
- Chapters 18, 19 and 26 after 03:57, and chapter 26's generator as it stood at 03:49, whose output I did not see.
- The live code sets in a browser: their states, keyboard paths and status lines as they run. I read their markup, CSS and script strings.
- The device script's steps on any device; I checked its menus against what I know of each platform only.
- Each of chapter 19's 55 criterion lines against the rules it cites, beyond spot checks; I checked that each cited rule exists, not that each meets its criterion.

## Change log

- Created: `work/handoffs/phase-2/20261111_Stage-C-Round-1-Editor-Notes.md` (this file).
- Modified: `work/handoffs/phase-2/20261110_Stage-B-Ch10-Labels.json`, CL-075's row after CL-074, the counts (125 rows, 75 CL, 20 topics) and a new `updated` line.
- Modified in the second pass: this file only, with sections 3b, 4, 5 and 6, the status line, and new lines under the main session, routine calls, Tested, Not tested and this log.
- Kept in my scratch folder, outside the project: two guide builds, a copy of the tree for the chapter 10 test run and my reading scripts, all under `/tmp/claude-0/-home-user-Dustin-s-Command-Center/42858b21-febe-5543-930e-ed82e286a69e/scratchpad/stage-c-r1/editor/`.
