# Stage B round 3 fix pass: chapter 11 hand's notes

Oath & Action Edition 06, Phase 2, stage B round 3, November 10, 2026. Written by the chapter 11 hand (`oa-design-director`, checked against `oa-ux-accessibility-lead`), a new agent in this role, run as a subagent of the main session under `20261110_Stage-B-Round-3-Fix-Brief.md` ("The chapter 11 hand"). My round 2 record is `20261110_Stage-B-Round-2-Systems-Ch11-Notes.md`. I committed nothing and pushed nothing. Paths are relative to `oath-and-action-v6-brand-guide/`.

Status: done. Every item the brief routes to me is applied in `apply_systems_ch11.py` and `apply_systems_ch11_ui.py`, and the stepper runs loop R1 by Dustin's answer (DR-195, D2-974), which the main session sent me mid-pass. No item waits.

## Items and what I did

Numbers follow the brief's list for the chapter 11 hand.

1. **ED 4e, chapter 11's five rows.** Rule 11.9's second paragraph now names the rule first ("A rule the agency issued without asking for comment first keeps steps 2 to 4 under slashes...") and gives the interim final rule its own sentence. The Justice Department source line takes "retrieved" after a comma, as the chapter's other lines do (in one run with BE-S1, item 9). Rule 11.10's builders say "the count of working days". The stepper's alt says "connection". The figure's note in Rule 11.16 names its reform in full, now reform R-32 (item 7). Every banded failure plate's alt in chapter 11 opens "Failure case: do not publish." (16 alts); the notes fields that say "Labeled failure" are not alts and stay.
2. **D2-950, six tracker pictures.** The alts of `s-11-1-correct`, `s-11-3-correct`, `s-11-3-failure`, `s-11-4-correct`, `s-11-4-failure`, `s-11-8-failure` and `s-11-9-failure` now name each step's state in words (done, now, you can take part now, not yet, never happened, stopped) where they named filled circles, rings and squares. `s-11-2-correct` keeps its shapes, since that plate is the key of the shapes; `s-11-5-failure` and `s-11-6-failure` keep theirs, since the shapes are the fault. `s-11-16-*` say each step's state too.
3. **`s-01-pieces` and chapter 11's mark classes.** No markup change was needed from me. The editor's generator (`guide_editor_ch01.py`) draws the Track card's steps with my `steps_svg()`, `key()` and `MARK_CSS`, so its rebuild carries the classes. I imported its `track_steps()` and `track_css()` against my final module: the marks carry `rn`, `ra`, `sl`, `lr`, `la`, `halo` and the 16 `data-icon` groups, and the CSS holds every `.mk` token rule (`rn`, `ra`, `sl`, `lr`, `la`, `td`, `tk`, `tc`). The working copy of `s-01-pieces.html`, rebuilt by the editor this pass, already holds them. The classes for the editor, if a mark is ever written by hand: `rn` (ring now), `ra` (ring ahead), `sl` (slash), `lr` (line reached), `la` (line ahead), `td`, `tk` and `tc` (the take-part disc, keyline and cut), and `halo`.
4. **PP-M1, the words a developer builds from.**
   - Rule 11.2's why now says which marks draw in ink (the steps reached, the slash, the line as far as the record has come) and which in Stone or Dim Newsprint (the rings ahead, the ring under a slash, the line after the current step), and that only the take-part disc is red.
   - A new readable table, "Drawing the marks" (`s-11-marks-drawn`, an extra after Rule 11.2), gives every mark at the four circle sizes: its drawing, its line or size token and its color token. It gives the slash's angle, its length (28, 30, 32 and 34 px, 2 px past the ring at each end) and its ink; the halo as a 4 px stroke that shows 2 px; the square at 22, 24, 26 and 28 px; the take-part disc's center, 0.72 of the radius right and up (8.64, 9.36, 10.08 and 10.8 px); the number weights (700, and 600 for a step not yet reached or never happened); and the line into a step that never happened. Its figures are computed from `node()`, so the table cannot drift from the drawing.
   - Request 99003 and the words now agree: the 2 px line runs into a step that never happened, the last step included, and Rule 11.5's Line spec, the table and Rule 11.2's why say so (call below).
   - Rule 11.5's spacing: "the first circle on the text edge and each next one 60 px on, center to center, so six fit a 328 px row."
   - Rule 11.2's specs give the halo its own row with its token, the slash its length and ink, the square its size; Rule 11.7's Numbers row gives the 600 weight; Rule 11.2's builders point to the table.
5. **PP-M3 and CD-S7.** Rule 11.15's specs list the error mark's ink, `--oa-color-state-error-text-on-newsprint`, and the red bar, `--oa-color-state-error-mark-on-newsprint`, labeled "The red bar" with "this token colors the bar only". Its token chips no longer put the error mark token in the row of mark colors. A builders sentence says the same. Rule 11.16's specs add the error mark's ink beside "First claim ... which holds the red bar".
6. **CD-M1 and CA-S1, the report reader.** A four-page report, each page with its own heading and a sentence or two of real text at the body size, Illustrative like the rest of the piece. The page is readable to a screen reader (no `aria-hidden`), and the status line names the page's title: "Page 2 of 4: What a mile of road costs". The failure plate's counter reads "1 / 4" to match.
7. **BE-M2 with D2-958, BE-S6, CD-S5.** H.99009 is now "Local news grants", headed "The House hears the local news grants bill on March 3". Its figure draws Local news supply (Variable B2) outlined as the target, with an arrow to Electoral pressure (Variable C3), and the note: "Reform R-32, public and philanthropic funding for local news, acts here. In our atlas, more local news raises electoral pressure, the risk officials face of losing office. It grades the reform’s own effect a hypothesis, since no evaluation has yet shown that such funds improve coverage." R-32 carries no interest flag in V7, targets B2 and connection L26 (B2 to C3, well supported), and grades its remedy evidence a hypothesis, which the note says. The three marks, their order and the yielding are as built. The Illustrative label sits at the end of the card's kicker line only; the atlas figure carries none. "all-party" is gone, so its hyphen cannot break, and the email error keeps "an @," on one line. My round 2 notes' counter table says what H.99009 now is.
8. **BE-M3 with D2-969 and DR-195.** The stepper runs Atlas V7's loop R1, "Wealth and political influence reinforce each other", read from the model as round 2 read R10: the chain's labels, each step's verb from its connection's sign, and the connection's own plain sentence. Step 2 is L02, graded plausible, so it reads "Money in politics can raise policy tilt to insiders." and its sentence ends "Our atlas grades this step plausible, the least certain in the loop." Steps 1 and 3 (L01, L03) are well supported and take "raises". The start line reads "Start at wealth concentration, and suppose it rises. Press Play, or Next step to follow one connection at a time." The loop is one parameter, `LOOP_ID` in `apply_systems_ch11_ui.py`; the kicker, title, alts, caption, notes and the pace spec read from it. Rule 12.5's marker and the reader check stay on R10 and R-01, untouched. Source: the coordinator's message relaying Dustin's answer, logged as DR-195 and D2-974 in the decision log.
9. **BE-S1.** "Source: Office of Information Policy, U.S. Department of Justice, “Fiscal Year 2024 Annual Freedom of Information Act Report”, March 6, 2025, sections V.B.(1) and VI.B, fiscal year 2024, the Justice Department and its components, retrieved November 9, 2026. The categories behind the end words in Rule 11.8."
10. **BE-S2 with D2-961, BE-S3, BE-S4 and CD-S8, BE-S8.**
    - Rule 11.10's why: "The law lets an agency stop its 20 working days while it waits on the requester, once for more information and again to settle fees, and add up to 10 working days in unusual circumstances, so each wait belongs inside the step it falls in." Its rule says "an extension of up to 10 working days".
    - Rule 11.9's why: "the main way the law gives the public".
    - Rule 11.8 opens with the scope: "These steps and end words follow the federal Freedom of Information Act and the Justice Department’s categories; a request to a state or local agency follows that state’s law." The invented requests take subjects a federal agency holds: food safety inspection records, weather station repair records and prison inspection reports join bridge inspection reports and park ranger staffing records.
    - The research lead's state hearing line joins the sources after the Nebraska line, behind Rule 11.1, with "no page date" for the three undated pages and its closing clause recast (call below).
    - Every source line names a period: "as in force on November 9, 2026" after each statute, "no page date" after Nebraska's lawmaking page, FOIA.gov and RegInfo.gov. The rulemaking line also names Cornell Law School.
11. **PP-S11.** Rule 11.10 now says which statuses carry the warning mark: "A status taken from the agency’s own tracking service, or from the Federal Register for a rule, needs no mark. A status we piece together ourselves, such as a wait we learn of from the agency’s letter, carries the warning mark and the date we checked it." The Check date spec and the builders say the same. `s-11-8-correct`'s three requests read from the agency's tracking service, so they need no date; `s-11-10-correct`'s wait comes from a letter and keeps its mark.
12. **PP-S16.** Rule 11.16's why ends "so nothing it says is lost."
13. **CD-S6, CD-S9.** `s-11-marks` carries its Illustrative chip at the plate's head. The stepper's visible start line says "one connection at a time", in both plates.
14. **Craft and accessibility.**
    - CA-M1 (D2-972): Play holds each step 250 ms a word, counting every word the live region reads, never under 6 seconds, with reduced motion too: 9, 12.75 and 9.5 seconds for loop R1. Rule 11.14's specs state the pace and the step words. The step box holds the longest step, so the buttons never move.
    - CA-M2: "Clear the search" keeps 44 by 44 px (it had shrunk to 42 in the flex row). The check that types before it measures is the engineer's.
    - CA-S2: under the three rows, "The first three are listed here, and 117 more match."; an empty result says "No symbol matches. Clear the search or the filters to see more."
    - CA-S3: the menu panel's bar, with Close the menu, stays at its top while the list scrolls.
    - CA-S4: every hyphen between two letters or figures in a fixed chapter 11 plate is a non-breaking hyphen (U+2011), in the markup and in the text the reader and the library write by script. Alts and the library's search data keep the plain hyphen.

## Routine calls

- D2-xxx | The stepper runs loop R1 from one parameter, `LOOP_ID` in `apply_systems_ch11_ui.py`, and every word, alt, caption and spec about the loop reads from it | DR-195 and D2-974; the brief asked for one switch
- D2-xxx | The stepper's headlines keep round 2's form, the chain labels with a verb from the connection's sign, so step 2 reads "Money in politics can raise policy tilt to insiders." | The instruction relaying DR-195 says to read the steps as round 2 read R10; D2-969 sets "can" and the grade sentence
- D2-xxx | The build stops on a loop with more than one plausible step, or a grade the stepper has no words for | "the least certain in the loop" is true of one step only, and no grade may drop out (H08)
- D2-xxx | Play times each step from every word its live region reads, "Step 1 of 3:" included, at 250 ms a word with a 6 second floor | D2-972; a screen reader reads the step number too
- D2-xxx | The step box holds the longest step's height (14rem) and the report page the tallest page (14.5rem, page 1 cut to one sentence) | Controls that move as content changes misplace a pointer and a magnifier; measured steady at 360, 390 and 1440 px
- D2-xxx | The report reader is a four-page report | CD-M1's second option; four real pages teach the same controls as twelve at a third of the words
- D2-xxx | H.99009's figure draws two ovals, Local news supply as the target and Electoral pressure, through connection L26 | R-32's third target, connection LT03, starts at Variable TC2, whose only V7 name is a 51-character title that cannot fit a third oval at 360 px, and LT03 is negative, which an unsigned arrow would misstate
- D2-xxx | The figure's note gives R-32's own grade, a hypothesis | V7 grades R-32's remedy evidence a hypothesis; H08 and DR-93
- D2-xxx | H.99009's Illustrative label sits at the end of the card's kicker line | BE-S6 and CA-S9: beside the invented item, in one place
- D2-xxx | The 2 px line runs into a step that never happened, the last step included, and the words say so | The record moved past that step; a 1 px line into step 6 would read as a step still to come, and one rule now covers a skipped middle step and a skipped last one
- D2-xxx | Rule 11.5's spacing keeps the circles 60 px apart and says six fit a 328 px row | Spreading them to the far edge would put them on fractional pixels
- D2-xxx | "Drawing the marks" is a readable table after Rule 11.2 (`s-11-marks-drawn`), its figures computed from the drawing code | A rule's specs hold label and value pairs, not a table; a table built from `node()` cannot drift from the marks
- D2-xxx | The table writes color tokens as `-on-<surface>`, and its caption says to read "charcoal" on Charcoal | One row serves both surfaces, in PP-M3's own form
- D2-xxx | Rule 11.15's token chips drop the error mark token, which its specs list as "The red bar" | PP-M3: in a row of mark colors the name told a developer to paint the glyph red
- D2-xxx | Rule 11.10 sorts a status by its source: the agency's tracking service or the Federal Register needs no mark; a status we piece together ourselves carries the warning mark and the check date | PP-S11; the plates already follow this split, and only a status we put together ourselves can be older than the record a reader would check
- D2-xxx | The invented requests take federal subjects, and "20 working days" stays | BE-S3's first option keeps the rule's true federal clock in front of the reader
- D2-xxx | Rule 11.10's "A pause inside a step" becomes "A wait inside a step" | An extension adds days and pauses nothing (BE-S2)
- D2-xxx | The state hearing source line ends "and we read these five as examples and made no national count" where the research lead wrote "and these five are examples, not a count" | Chapter 02's W09 rules out the corrective "not" turn; the meaning is unchanged, and the editor reads it after this pass
- D2-xxx | Every hyphen between two letters or figures in a fixed chapter 11 plate is a non-breaking hyphen, in the markup and in text a script writes; alts and search data keep the plain hyphen | CA-S4 and D2-950; a screen reader and a search read the word as typed
- D2-xxx | The email error binds "an @," with a no-break space | CD-S5
- D2-xxx | The library's empty result says what to do: "No symbol matches. Clear the search or the filters to see more." | An empty state says why it is empty and what makes it fill (the UX lead's states list)
- D2-xxx | The reader's page header binds "· page 1" to the report's last word and balances its two lines | At 360 px "PAGE 1" fell alone onto a second line

## Questions for Dustin

None. The loop question is answered (DR-195), and nothing in this pass changes a decision from DR-95 to DR-198.

## Requests to other owners

- **Editor (D2-963).** The strings I changed or wrote, for your read: Rules 11.2 (why, specs, builders), 11.5 (two specs), 11.7 (Numbers), 11.8 (scope sentence), 11.9 (rule paragraph 2, why), 11.10 (rule, why, specs, builders), 11.14 (caption, two specs), 11.15 (specs, builders), 11.16 (caption, specs, why); the five source lines; the "Drawing the marks" table and its caption; the reader's four pages; the library's two count lines; the stepper's start line and step 2; H.99009's card and figure note; and the alts of `s-11-1-correct`, `-3-correct`, `-3-failure`, `-4-correct`, `-4-failure`, `-8-failure`, `-9-failure`, `-10-correct`, `-10-failure`, `-11-correct`, `-11-failure`, `-12-correct`, `-14-correct`, `-14-failure`, `-16-correct`, `-16-failure`, `s-11-marks`, `s-11-marks-drawn` and `s-11-menu`, with every failure alt's opening. Two wordings I would like you to look at first: the hearing source line's last clause (call above) and "Money in politics can raise policy tilt to insiders", which keeps V7's chain label "Policy tilt to insiders".
- **Editor, `s-01-pieces`.** Nothing to do: your generator already draws its marks with chapter 11's classes (item 3).
- **Engineer.** CA-M2's second half, the guide check typing into the search before it measures. The library's results and the reader's pages now hold U+2011 in text a script writes; nothing in `guide_check.js` reads those strings, as far as I found.
- **Main session.** Log the calls above; the counter table in my round 2 notes now names H.99009's new subject.

## Tested

(Filled in below.)

## Not tested

(Filled in below.)

## Change log

(Filled in below.)
