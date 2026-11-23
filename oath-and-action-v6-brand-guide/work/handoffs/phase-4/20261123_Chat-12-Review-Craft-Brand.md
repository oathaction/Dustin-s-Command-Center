# Chat 12 review: craft and brand (CR, BR)

Written November 23, 2026 (started 17:12 UTC) by the craft and brand reader: the design director's role as a critic who has not seen this work, with the creative director's brand knowledge. Brief: `work/handoffs/phase-4/20261123_Chat-12-Review-Brief.md`, sections 1 to 8. Early findings first; the report grows as the review runs.

Status: in progress. The capture set was still being made at the start, so the review begins with the kit's export PNGs at true size.

## 1. Score

Pending.

## 2. Must fix

Pending. Early findings sit in section 2a until the review sorts them.

## 2a. Early findings (exports at true size, A11 to A14, 17:12 to 17:18 UTC)

- A14 Loop R18: the weakest step's red arrowhead floats about 20 px clear of its dashed line at the bottom left corner (1440 and 390 px). The dashes end at the corner and the up run to the arrowhead carries no ink.
- A11 home 1440: "This question reaches / here" ends on one word in Wealth and Checks; "6 variables, 6 / connections inside" and "2 variables, no / connections inside" break inside a phrase; Policy's wrapped question drops its model title 21 px below its row's.
- A11 home: question buttons sit 8 px inside their category heads at every width; "Public services where you / live" ends on one word; three phone buttons end on one word ("up?", "long?", "get?").
- A12 R-23: the chip row under the drawing reads "Variable A4 : Reform R-24 Reform R-25 Reform R-26 Reform R-31 also aim here", a detached colon and no commas; one view prints "Households’" and "Households'" both.
- A12 and A14: route rows run their parts together with no separator ("Legislatures High feasibility Not checked"); a double rule (17 px apart) above "Sources for this page".
- A13 Register: grade cells wrap the word under the sample for Documented, Well supported and Hypothesis but not Plausible; "years" ends alone in every Delay cell; "194, one / retired" in the total row; the grade samples in the head row sit at two heights; "Filters, 1 on" carries an empty 30 px check slot; "9 of 20 issue records" sits 4 px under the chips.
- A14: a 500 px hole in the left column at 1440 between the read-aloud text and the reform chooser; the loop drawing at about 300 px is the page's exhibit and its smallest part.
- Effects tables (A12, A13, A14): "Income and wealth / equality" ends on one word; the range's join (R12) lands on a half pixel and reads gray.
- A06 Act page (export and the guide's frames of it): the two links under "The rule at a glance" read "The rule on the FederalRegister" and "The rule as a PDF ongovinfo.gov". The markup holds the space ("Federal <span class="ws-out">Register"); the link's flex layout drops it.
- Chapter 16: every caption and label set as a `<p>` sits flush under its photograph (0 to 2 px of line box), because `.w p{margin:0}` in `phase4_ch16_build.py`'s BASE outranks `.cap{margin-top:12px}` and the `.mt8` to `.mt24` helpers. Seen on the opener, 16.2 to 16.7 and 16.13.
- 16.2 correct: the placeholder sits 20 px below the photograph's top and at 318 by 212 beside a 360 by 240 photograph (Rule 16.8: the photograph's ratio and display size).
- 16.6 correct: marker 1 is a filled disc, marker 2 an outline ring; the key under the photograph draws both as filled discs.
- 21.5 failure: the targets turn into rounded boxes with a Charcoal edge and left-set labels, so the plate shows three differences from the correct one, one of them a keyline DR-305 removed.
- A11 every variable (browser, true size): four pills hold their widest line 3.2 to 4.8 px from the curved stroke (Court rulings, Incumbents, Entrenched control, Policy advantages). Words clear; the margin is thin.
- Apostrophes: the stored titles hold a straight apostrophe. A12's pill prints "Households’" and its prose "Households'"; A11's pills and A13's tables print straight ones ("Congress's", "Workers'", "Homeowners'").
- Chapter 20, 16 and 21 openers carry no caption; chapter 20's `W['opener_caption']` is written and unplaced (named place 12).


## 3. Should fix

Pending.

## 4. The named places

Pending.

## 5. For Dustin

Pending.

## 6. Tested

Pending.

## 7. Not tested

Pending.
