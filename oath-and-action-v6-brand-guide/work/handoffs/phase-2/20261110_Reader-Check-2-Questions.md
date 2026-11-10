# The combined reader check: questions

Oath & Action Edition 06, Phase 2, stage B, November 10, 2026. Written by the editor for the engineer, who builds the page from this file as a new dated page from the first check's tooling (D2-493), and for the main session and Dustin. The first check's page and folder, `work/boards/phase-2/reader-check/`, stay as they are.

This is the one combined check DR-143 asks for. Five to eight people who have never seen the brand take it once, on their phones (DR-148). It keeps the first check's questions that still apply and adds questions on reading Pillar Red for party (DR-114, with R-46 Expand the House as DR-152 asks), the six tracker steps, the pillar icons, the end mark at 14 and 12 px and the 24 px lockmark. Every word a reader sees is quoted below, so the engineer copies it as written.

Round 3 fix pass, November 10, 2026: two changes for the engineer. Step 4's name on the page is now "A card and a drawing" (D2-950), and step 7's footer question reads "Look at the small square mark beside the line of text. What did you see in it?" (PP-S13). Nothing else in this file changed.

## What carries over, what leaves, what is new

| First check | In this check | Why |
|---|---|---|
| Step 1, welcome and consent | Kept, with the new time and one new recorded field | DR-87 still holds |
| Step 2, the overview, R10 and B4 | Kept as written | System 1 is settled (DR-36), and nobody has answered these yet: the first link was never sent (DR-143) |
| Step 3, eight symbols named | Four symbols: R-02 kept, and Congress, Testify and Contact an Official, approved November 10, in place of the other three; the four pillar icons leave this step | Dustin's answer (DR-189) puts the new drawings in front of first-time readers; since November 7 a pillar icon always sits with its word (DR-111), so step 5 tests them as they are used |
| Step 4, nine small marks | Rebuilt with today's small marks | The condensed wordmark left the proofs (DR-115), the hinge-circle badge keeps sizes from 48 px (DR-118), and the pillar icons now have pixel fits (DR-179); the rebuilt 24 px lockmark joins (DR-181) |
| Step 5, three charts | Kept as written | The chart system is settled (DR-52 to DR-61) |
| Step 6, three sentence pairs | Kept as written | Chapter 02 is settled (DR-73 to DR-83) |
| Step 7, two mastheads | Leaves | DR-115 settled the width (D2-323) |
| New | Red and party: the link card and R-46 | DR-114, DR-152 |
| New | The pillar row at 24 and 48 px | DR-111, DR-133, DR-179 |
| New | The six tracker steps | DR-108, DR-143 |
| New | The 24 px lockmark in use | DR-145, DR-181 |
| New | The end mark at 14 and 12 px | DR-142, DR-180 |

## The flow, 11 steps, about 15 minutes

| Step | Name on the page | What the reader does | Timed looks | Minutes, estimated |
|---|---|---|---|---|
| 1 | Welcome | Reads one paragraph, types a first name or initials, taps Start | none | 0.5 |
| 2 | Drawings | The overview, then R10 and B4 in random order, with the first check's questions | 3 at 10 s | 2.8 |
| 3 | Symbols | Names four symbols | 4 at 10 s | 1.9 |
| 4 | A card and a drawing | A link card and one drawing, with questions on what the red says | 2 at 10 s | 1.2 |
| 5 | The four | Two rows of four drawings with words; which one the page belongs to | 2 at 10 s | 0.9 |
| 6 | Steps | Three rows of step marks and one list of bills | none | 1.5 |
| 7 | Small marks | A sheet of 12 marks, then one mark in a page footer | 2 at 10 s | 1.3 |
| 8 | The end of an article | The same two sentences at two text sizes | none | 1.1 |
| 9 | Charts | S02, S11 and S14 in random order, as in the first check | 3 at 15 s | 2.5 |
| 10 | Sentences | W02, W10 and W11, A and B in random order | none | 0.7 |
| 11 | End | Thanks; in copy mode, the answers with a Copy button | none | 0.3 |

Fixed looking time is 175 seconds. With 54 answers (ten typed, two of them optional, and 44 tapped) the check runs about 15 minutes for a careful reader and about 11 for a quick one. These are estimates; the first check's figure of 9 to 10 minutes was never measured on real readers either.

Step 4 comes before steps 5 to 9 so that the first question about party meets the brand's red before the charts' party questions and before the red on the pillar row and the tracker.

## What the page keeps from the first check

Build from the first check's tooling (`build_reader_check.js`, `reader_check_template.html`, `test_reader_check.js`) and keep its behaviors:
- the reader starts every look, the clock runs only while the page is visible and every image has loaded, and "Show it again" follows every timed look, with its uses counted
- one question per screen, every question skippable, an empty Next caught
- answers saved after each one in saved mode, and copy mode with the Copy button when `db` or `user` is missing or a write fails
- a first name or initials and nothing else, resume after a reload, no brand name in the page's own words, stimuli under neutral file names with titles, descriptions and IDs stripped
- one light look on Newsprint, 44 px targets, text 13 px or larger except a mark shown at true size

New screen kind: steps 6 and 8 show their picture above the question with no timer, since a reader reads a tracker or an article ending at their own pace.

## Group reading

The studio reports, for each question, how many readers chose each answer and what they typed. A question needs a look when fewer than half the readers who answered it pass. Any reader who reads a party into a drawing or a page goes to Dustin with their own words, whatever the count.

## Step 1, Welcome

Title: "A short test of a draft design"

Paragraph: "We’re trying out a draft design for a civic publication, and we’d like your first impressions. You’ll look at some drawings, symbols, charts, sentences and small parts of pages and answer quick questions about each. It takes about 15 minutes. We record your answers, how long you take, how often you look again, your screen’s width and sharpness and the first name or initials you type below, and nothing else. You can skip any question and stop at any time."

The mode sentence, the field and Start stay as in the first check.

## Step 2, Drawings (kept)

The first check's screens, words and choices, unchanged: the overview's first two phone screens for 10 seconds, then "What do you think this page is for?" (typed) and "Which part would you open first?" (the eight parts as the drawing prints them, "None of them", "Not sure"); then R10 and B4 in random order, each for 10 seconds, each followed by "Do the arrows come back to where they started?", "Does it feed itself or push back?", "Which step is the least certain?" and "Where does a reform act?" with the first check's choices.

What counts as a pass, and why each is asked, stand as the first answer key gives them (`work/boards/phase-2/reader-check/20261106_Reader-Check-Answer-Key.json`, `overview` and `loops`). If System 1's finishing pass (DR-121) has redrawn the overview, R10 or B4 by the time the page is built, capture today's drawings and check that the step and box words in the choices still match what the drawing prints.

## Step 3, Symbols (four symbols, three of them new, DR-189)

Ready screen: title "Four symbols"; body "Each symbol shows on its own for 10 seconds. Then tell us what you think it stands for. A guess is fine."; button "Show the first symbol".

What the reader sees: one symbol at a time at 48 px, the Black edition on Newsprint, in random order, for 10 seconds. Draw each from `work/build/assets/civic-line-v6/black/`, the set in use, so Congress is the chamber Dustin approved on the drawings board (DR-156) and Testify and Contact an Official are CL-073 and CL-074 (DR-159, DR-160).

Question, for each: "What do you think this symbol stands for?" Hint: "A word or a few. A guess is fine." A one-line answer.

| Code | Symbol | What counts as a pass | Partly |
|---|---|---|---|
| i1 | CL-025, Congress | Names Congress, the House or the Senate | Names a legislature, a parliament, lawmakers or a chamber in session, such as "a legislature voting" |
| i2 | CL-073, Testify | Names testifying or giving testimony, speaking at a hearing, or a witness before a committee or a panel | Names a hearing, a committee or a panel, or someone speaking at a microphone, without the person who testifies |
| i3 | CL-074, Contact an Official | Names contacting, calling, writing to or visiting an official, a representative or their office | Names sending a message, giving feedback or making a complaint, with no official named |
| i4 | R-02, Ranked-choice voting | Names ranking candidates or ranked or numbered choices on a ballot | Names voting or a ballot alone |

Answers to report to Dustin in the readers' own words, whatever the count, because the drawings were drawn to rule them out (research notes of November 9, section 1):
- Congress: a court, a stadium or a theater audience, or any answer that names one party.
- Testify: a court or a trial, a judge, or a debate between candidates.
- Contact an Official: a job interview, a customer service or front desk, or a bank teller.

What to expect: the creative director found that no Congress drawing names Congress without its label, and that the label makes it land (D2-620). Congress will likely draw more partial answers than full ones, and a partial answer still shows the drawing points the reader at the right word.

Why it is asked: Dustin asked that every symbol clearly depict its institution, act or reform (DR-146), and on November 10 he approved Congress, Testify and Contact an Official by name after three options each. Only studio readers have named them so far. R-02 stays from the first check as a drawing already settled, for comparison. Chapter 10 always sets a symbol beside its word, so a reader who names the subject from the drawing alone shows the drawing and the word agree. The meanings follow the editor's table for chapter 10 (`20261110_Stage-B-Ch10-Labels.json`).

## Step 4, A card and a drawing (new)

The step's name on the page, in the progress line and anywhere else the page names its steps, is "A card and a drawing", the same words as its ready screen. The page shows the name before the first question about party, so it names what the reader will see and leaves color out (D2-950).

Ready screen: title "A card and a drawing"; body "Next you’ll see a card like the ones that appear when someone shares a link, and then a drawing. Each shows for 10 seconds. A few questions follow."; button "Show the card".

### red_card: the link card

What the reader sees: the link-preview card from the guide's proofs (`s-proofs-social`), the card face alone with no specifications table, 1200 by 630 drawn at the phone column's width (358 px wide at 390 px), as a feed would show it: the kicker "Explainer · Zoning", the hinge headline "The zoning code & the rent." with its red ampersand, the wordmark and the lockmark with its red node. 10 seconds.

Question red_card:favors: "Does this card seem to favor a party or side?"
Choices, in this order: "No" (no), "Yes, the left" (left), "Yes, the right" (right), "Not sure" (unsure).
Follow-up red_card:why, shown only after "Yes, the left", "Yes, the right" or "Not sure": "What gave you that impression?" Hint: "Optional. A few words is plenty." A one-line answer.

What counts as a pass: "No". A Yes or Not sure whose follow-up names the red, the color or the ampersand is the finding DR-114 asks for.

Why it is asked: Pillar Red stays the lead color (DR-114), and red is the color many readers link to one party. The card is the brand at its most common size in a reader's day, with red in two places and nothing about party in its words.

### house: R-46 Expand the House

What the reader sees: the drawing R-46 Expand the House, Red Black edition, at 96 px on Newsprint, with no label, for 10 seconds. It shows a chamber from above with a few seats added along the outer row in red, at the right end.

Question house:red: "What do you think the red seats show?"
Choices, the first four in random order, then "Not sure": "Seats being added" (added), "Seats one party holds" (party), "Seats for the leaders" (leaders), "Empty seats" (empty), "Not sure" (unsure).
What counts as a pass: "Seats being added". "Seats one party holds" is the reading DR-152 asks the check to catch.

Question house:favors: "Does this drawing seem to favor a party or side?"
Choices as red_card:favors. No follow-up.
What counts as a pass: "No".

Why it is asked: DR-152 keeps R-46 as drawn and asks this check whether readers take its red seats, at one side of a chamber, as a party's. Chapter 10 always sets R-46 beside its label, "Expand the House of Representatives", so showing it bare is the hard case: a pass here holds for the page.

## Step 5, The four (new)

Ready screen: title "Two rows"; body "Next are two rows of four small drawings, each with a word beside it. Each row shows for 10 seconds, with a question or two after it."; button "Show the first row".

### row_24: the compact row at 24 px

What the reader sees: the pillar row as a page header sets it under 48 px (chapter 09), at the phone column's width: the four icons at 24 px in one color, each with its word, in the order Explain, Track, Connect, Act, joined by arrows. The page serves Connect, so "Connect" is bold and underlined. No red. The icons draw as chapter 09 sets them for the reader's screen: the 24 px pixel fit B on a 1x screen and the masters at 24 px on a 2x screen (DR-179). 10 seconds.

Question row_24:current: "This row sits at the top of a page. Which of the four does the page belong to?"
Choices, in the row's order: "Explain", "Track", "Connect", "Act", "Not sure".
What counts as a pass: "Connect".

Why it is asked: chapter 09 marks the current pillar by underlining its word at every size, with no red under 48 px (DR-111, R10). This asks whether the underline alone tells a reader where they are.

### row_48: the section opener at 48 px

What the reader sees: the pillar row as a section opener at 48 px, stacked in one column as phones show it, the page serving Track: "Track" underlined, and Track's icon with its red parts, the pin and the magnifier's handle (chapter 09; the 48 px row in `s-01-pillars`). 10 seconds.

Question row_48:current: "Which of the four does this section belong to?"
Choices: "Explain", "Track", "Connect", "Act", "Not sure".
What counts as a pass: "Track".

Question row_48:red: "What do you think the red on one drawing tells you?"
Choices, the first four in random order, then "Not sure": "It marks the one this section belongs to" (current), "It warns of a problem" (warning), "It shows a party or side" (party), "It’s there for decoration" (decoration), "Not sure" (unsure).
What counts as a pass: "It marks the one this section belongs to". "It shows a party or side" goes to Dustin under DR-114.

Why it is asked: from 48 px, red on the current icon is a second sign beside the underline (DR-111, DR-133). This asks whether readers take that red to mean “you are here”.

## Step 6, Steps (new)

Ready screen: title "Bills and their steps"; body "Next are a few questions about how a list follows bills through a state legislature. The pictures stay on screen, so take your time."; button "Start".

The pictures come from chapter 11's list of five bills (Rule 11.5, `s-11-5-correct`) on Newsprint at 360 px, after DR-151's renumbering lands, with its Illustrative label. For questions 1 to 3, show one bill's row of six numbered step marks alone, with the bill's name, status line and the key hidden.

### steps_slash

What the reader sees: the row for "Records request fees": step 1 done, step 2 drawn with a slash, step 3 done, step 4 now, steps 5 and 6 not yet. Above it: "Step marks for one bill".

Question: "Look at step 2. What do you think its mark means?"
Choices, the first four in random order, then "Not sure": "That step was skipped and never happened" (skipped), "That step failed" (failed), "That step is done" (done), "That step is happening now" (now), "Not sure" (unsure).
What counts as a pass: "That step was skipped and never happened".

Why it is asked: a step that never happened keeps its number with a slash (DR-108), and chapter 11 draws each state as a shape so the set reads without color (Rule 11.2). The list prints the reason in words beside the row; this asks what the shape says before the words do.

### steps_square

What the reader sees: the row for "Parking meter fees": steps 1 to 5 done, step 6 drawn as a filled square.

Question: "What do you think the square at step 6 means?"
Choices, the first four in random order, then "Not sure": "The bill stopped there" (stopped), "The bill became law" (law), "The bill is waiting at that step" (waiting), "That step was skipped" (skipped), "Not sure" (unsure).
What counts as a pass: "The bill stopped there".

Why it is asked: a bill that stops ends its line on a square, and a signed bill reads as law in words (DR-108, Rule 11.3). A reader who takes the square for law reads the opposite of the record.

### steps_dot

What the reader sees: the row for "Public meeting notice": step 1 done, step 2 now with the small red disc on its ring, steps 3 to 6 not yet.

Question: "What do you think the small dot on step 2 means?"
Choices, the first four in random order, then "Not sure": "You can take part at this step now" (take_part), "Something went wrong at this step" (error), "This step is running late" (late), "It marks one party" (party), "Not sure" (unsure).
What counts as a pass: "You can take part at this step now", or "Not sure". The list always prints "You can take part now" beside the dot (Rule 11.4), so the misreadings that matter are "Something went wrong at this step" and "It marks one party".

Why it is asked: the take-part mark is one of the three things that may claim a view's working red (Rule 05.3), and chapter 11 decides which yields when an error mark sits beside it. A reader who sees an error or a party here shows where the words must carry the meaning.

### steps_list

What the reader sees: the whole list of five bills as chapter 11 prints it, with every status line and the key, Illustrative label included. The picture scrolls inside the page if it runs long.

Question: "Which bill does this list say you can take part in now?"
Choices: the five bill names in the list's order ("Public meeting notice", "School bus contracts", "Library hours", "Records request fees", "Parking meter fees"), then "None of them" (none), "Not sure" (unsure).
What counts as a pass: "Public meeting notice".

Why it is asked: the tracker's job is to show a reader where a decision stands and when they can act. This asks whether a newcomer finds the one bill open to them in a list of five.

### steps_names

What the reader sees: the same list.

Question: "The list follows each bill through six steps: Filed, Hearing, Committee vote, First chamber, Second chamber and Governor. How clear are those step names?"
Choices, in this order: "All clear" (all), "Mostly clear" (most), "Mostly unclear" (few), "Not sure" (unsure).
Follow-up steps_names:which, shown after any answer other than "All clear": "Which name was unclear?" Hint: "Optional." A one-line answer.
What counts as a pass: "All clear" or "Mostly clear".

Why it is asked: DR-108 gave the tracker six plain step names in place of nine stages. This is the first time a reader outside the studio judges them.

## Step 7, Small marks (rebuilt)

Ready screen: title "Twelve small marks"; body "Next is a sheet of 12 marks at the small sizes you might see in a browser tab or a page header. It shows for 10 seconds. Then you’ll say how clear each one looked."; button "Show the marks".

What the reader sees: one sheet at true size, one color, Charcoal on Newsprint, numbered 1 to 12, in two rows, 16 px then 24 px, for 10 seconds. The rating screen repeats each mark at its true size, as in the first check.

| Code | Mark | Size | Drawn from |
|---|---|---|---|
| m1 | The wordmark at today's width | 16 px tall | the 16 px wordmark master |
| m2 | Ampersand B | 16 px | the 16 px master |
| m3 | The lockmark | 16 px | the 16 px master, which stays in use (DR-181) |
| m4 | Explain | 16 px | the 16 px pixel fit (DR-179) |
| m5 | Track | 16 px | the 16 px pixel fit |
| m6 | Connect | 16 px | the 16 px pixel fit |
| m7 | Act | 16 px | the 16 px pixel fit |
| m8 | The lockmark | 24 px | the rebuilt 24 px master (DR-181) |
| m9 | Explain | 24 px | fit B on a 1x screen, the master on a 2x screen (DR-179) |
| m10 | Track | 24 px | as m9 |
| m11 | Connect | 24 px | as m9 |
| m12 | Act | 24 px | as m9 |

Question marks:rate: "How clear was each mark?" Hint: "Each one appears again below at the same size. Clear means you can make out its shape." For each mark, the first check's three choices: clear, blurry, can't tell.
What counts as a pass: "Clear". A mark that half the readers call blurry or can't tell goes to the identity designer with the screen sharpness each reader recorded.

Why it is asked: the first check's question, with the marks in use today. Pixel fits are drawn for 1x screens and most phones are 2x or 3x, so the record's screen sharpness says which drawing each reader saw.

### lockmark_24: the 24 px lockmark in use

What the reader sees: the foot of a page at phone width on Newsprint, as chapter 08 sets the footer place: the lockmark at 24 px from the rebuilt master, with its red lever, beside a line of footer text. 10 seconds.

Question: "Look at the small square mark beside the line of text. What did you see in it?"

The question screen hides the picture, so the question finds the mark by the line of text beside it and asks what the reader saw. In the picture the mark sits near the top of what the reader sees, so "at the bottom" sent readers to the wrong place (PP-S13).
Choices, the first three in random order, then "Not sure": "Dots on a grid" (dots), "Lines or stripes" (stripes), "A blur or a smudge" (blur), "Not sure" (unsure).
What counts as a pass: "Dots on a grid".

Why it is asked: DR-145 rebuilt the 24 px master so each node and the lever draw as one outline, because the old file could part into stripes. This asks whether readers see the grid of nodes it is meant to show.

## Step 8, The end of an article (new)

Ready screen: title "The end of an article"; body "Next are the last lines of a short article, at two text sizes. The text stays on screen."; button "Show the text".

What the reader sees, screen 1: two sentences from our systems atlas's everyday answer to "Why is my electric bill going up?", set as an article ending in 17 px Inter on Newsprint, at the phone column's width, with the end mark, ampersand B, half an em after the final period in the text's ink, at the text's cap height, drawn from fit B at 14 px (DR-180):

> For an investor-owned utility, the state public utility commission sets rates in a rate case; for public power and cooperatives, a city council, utility board or co-op board does. Rates recover the cost of power plants, fuel, transmission lines and local wires, and investor-owned utilities also earn a regulated return on what they invest.

Screen 2: the same lines in 15 px text, with fit B at 12 px.

The lines are real, quoted word for word from Atlas V7's pathway PW03, so they carry no Illustrative label. Draw the mark as chapter 04's end mark specimen does on the reader's screen (`s-04-6-correct`, Rule 04.6).

Questions on screen 1:

end_17:meaning: "What do you think the small mark at the end of the text tells you?"
Choices, the first four in random order, then "Not sure": "The article ends here" (ends), "There’s more to read" (more), "It points to a note" (note), "It’s the publication’s sign" (sign), "Not sure" (unsure).
What counts as a pass: "The article ends here". "It’s the publication’s sign" passes in part, since B is the publication's ampersand.

end_17:clear: "Can you make out the mark’s shape?"
Choices, in this order: "Yes, clearly" (clear), "Barely" (barely), "No, it looks like a blur" (blur), "I don’t see a mark" (unseen).
What counts as a pass: "Yes, clearly" or "Barely".

end_17:sits: "How does the mark sit with the words?"
Choices, the first three in random order, then "Not sure": "It fits in with the text" (fits), "It pulls my eye too much" (loud), "It looks like a stray character or a mistake" (stray), "Not sure" (unsure).
What counts as a pass: "It fits in with the text".

Questions on screen 2: end_15:clear and end_15:sits, worded and scored as above.

Why it is asked: DR-130 set the end mark at the text's cap height because B at 16 px read louder than the line it ends, and DR-142 and DR-180 drew it on whole pixels at 14 and 12 px so its edges stay crisp. These questions ask whether readers see it, whether it sits quietly, and whether they read it as the end.

## Step 9, Charts (kept)

The first check's screens, words and choices, unchanged: S02, S11 and S14 in random order, each for 15 seconds, then "What is this chart telling you, in one sentence?" (typed) and "Does it seem to favor a party or side?" ("No", "Yes, the left", "Yes, the right", "Not sure"). Passes and reasons stand as the first answer key's `charts` gives them. Capture today's drawings; if a chart's title has changed since November 6, put its new title and finding in the new answer key.

## Step 10, Sentences (kept)

The first check's three pairs, W02, W10 and W11, in that order, A and B in random order within each, "Which is easier to follow?" with its three choices. Passes and reasons stand as the first answer key's `pairs` gives them: the after is expected to read easier.

## Step 11, End (kept)

The first check's thank-you screen and copy text, unchanged.

## Record: what changes

The first check's `record_fields` stand, with these changes:
- `device_pixel_ratio`, the screen's `window.devicePixelRatio` at the start, beside `viewport_width`. Pixel fits are drawn for 1x screens, so steps 5, 7 and 8 need it to say which drawing a reader saw.
- `orders` adds the order of the shuffled choices for each question that shuffles them, by choice code.
- Items for the new steps, keyed by the codes above: `red_card`, `house`, `row_24`, `row_48`, `steps_slash`, `steps_square`, `steps_dot`, `steps_list`, `steps_names`, `marks` (12 codes, m1 to m12), `lockmark_24`, `end_17`, `end_15`.
- The masthead item leaves.

## Answer key: what the engineer writes

A new key file beside the new page, never published with it, holding:
- the first key's `overview`, `loops`, `charts` and `pairs` sections as they stand, with any chart title brought up to date
- `icons`: the four rows of step 3's table, each with its file, ID, chapter 10 label, the editor's meaning sentence from `20261110_Stage-B-Ch10-Labels.json`, and what counts as a pass and in part
- one entry per new question above: the stimulus file, its size and surface, the right answer's code, any partial codes, the codes that go to Dustin (`party` on house:red, steps_dot and row_48:red; `left` and `right` on every favors question) and the "why it is asked" line
- `marks`: step 7's table, with each source file as promoted

## Words the page must never print

The build's leak check refuses a page that names a stimulus's meaning. Add these to the first check's list: "Expand the House", "R-46", "end mark", "lockmark", "pillar" and "Pillar Red", and allow "party" only in the favors questions and in the choices of house:red, row_48:red and steps_dot. The pillar words Explain, Track, Connect and Act are allowed: step 5 prints them as the rows do. The first check's label test covers step 3's new labels, Congress, Testify and Contact an Official, once the configuration carries them. Keep "testimony", "hearing", "official" and "legislature" out of the page's own words up to the end of step 3 as well, since a reader could echo them in a step 3 answer. The step 2 drawings print none of them; check again if they are recaptured.

## The invitation

Two lines for Dustin to paste to five to eight people who have never seen the brand, with a mix of ages and political leanings (DR-87). Put the link where it says [link].

> Could you spare about 15 minutes on your phone for a short test of a draft design for a civic publication? You’ll look at some drawings, charts and pages and say what you see, and there are no wrong answers: [link]
>
> It asks only for a first name or initials, and you can stop at any time. If the last screen shows your answers with a Copy button, please paste them into a reply to me.
