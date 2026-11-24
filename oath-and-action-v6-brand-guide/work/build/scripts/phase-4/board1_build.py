"""Phase 4 board 1: the review board Dustin answers after chats 10 to 12b (Gate 3 report, section 9).

It shows chapter 16's rules with their photographs and placeholders, the website chapter 20 teaches at 1440, 1024, 390
and 360 px and in its dark theme, the atlas's views with the atlas test, the application kit's measured bytes and the
allocations, the platform specifications table and the creative director's rescore. It sets every item that changes
approved work beside its original at true size, and it asks Dustin only what he must decide, ranked, with the studio's
recommendation, the register code and one reply that takes every recommendation.

Usage, from the project folder:
  python3 -I work/build/scripts/phase-4/board1_build.py [--caps DIR] [--report JSON] [--wall DIR]
  python3 -I work/build/scripts/phase-4/board1_build.py --capture --now PAGE [--before PAGE] [--only a,b] [--caps DIR]

The first form writes work/boards/phase-4/board-1/20261124_Phase-4-Board-1.html and its img/ folder (lossless WebP).
It reads the exports in work/build/exports/phase-4/, the captures in --caps (made by the second form), the strict
build's report (--report) for the chapters' bytes and the projection, the creative director's scores
(work/handoffs/phase-4/20261123_Chat-12-CD-Scores.json), the platform specifications
(work/research/20261121_Platform-Specifications.json), the atlas test (work/build/app-kit/plates/atlas-test.json) and
the chapter JSON for rule titles. It never runs a generator and never writes outside the board folder.

The second form captures pictures in a browser. It runs only when the chat's browser gate prints "OK to open one"
(browsers.sh beside the build lock), writes its script to the captures folder and runs it with node from work/build.
--now is a strict build of today's page; --before is the page built in scratch from commit bc91667e (`git archive
bc91667e | tar -x -C <scratch>`, never a checkout) for PR-M1's before. Every proposal picture it makes is a studio
sketch: the change is made in the browser's copy of the page, and no chapter's file changes.

Late parts are slots until they land: chapter 16's video plates after A21 (CH16_VIDEO_FINAL), the rescore of C16-V
(C16V_RESCORE), the wall test's covered pictures (--wall), A21's final frames (A21_FINAL), chapter 21's opener after
CD-R1 (OPENERS_FINAL) and Engineer M's final weight table (WEIGHT_TABLE). Each slot prints a marked line saying what will fill it.
"""
import argparse
import html
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / 'work/boards/phase-4/board-1'
IMG = OUT / 'img'
PAGE = OUT / '20261124_Phase-4-Board-1.html'
EXP = ROOT / 'work/build/exports/phase-4'
SCRATCH = Path('/tmp/claude-0/-home-user-Dustin-s-Command-Center/ade8e70b-f71c-536b-8654-9b651b94da3a/scratchpad/c12b')
GATE = SCRATCH / 'browsers.sh'
DAY = '20261124'
LIMIT_BYTES = 40 * 1024 * 1024
LIMIT_FILES = 250
VH = {1440: 900, 1024: 768, 390: 844, 360: 780}   # one window's height at each width (contract C5)

e = html.escape
META = {}   # the captures' measures (caps.json), read in main()
CAPS = Path('.')   # the captures folder, set in main()


def n(v):
    return f'{v:,}'


WORDS = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']


def num(v):
    """H06: one to nine in words in prose."""
    return WORDS[v] if 0 <= v < 10 else n(v)


# ================================================================ late parts (slots until they land)

CH16_VIDEO_FINAL = True    # True once the captures of Rules 16.10 and 16.11 are taken from a page with A21 placed
C16V_RESCORE = None        # read in main() from 20261124_Chat-12b-CD-Scores.json, block rescore_12b, key c16v_for_board
CD12B = {}                 # that rescore block, for its notes on CD-R1 to CD-R5 and the risk it names
# Engineer M's final table: work/handoffs/phase-4/20261124_Chat-12b-Engineer-Weight-Notes.md, "On the final page"
# (the strict build of commit 84163752, 14,444,690 bytes). Figures copied from that table; reader loss in its words.
WEIGHT_TABLE = {
    'note': ('Engineer M measured every option on the final page, 14,444,690 bytes, each as a variant page built whole and '
             'weighed the way the build weighs it. “Approved” chapters are those a gate approved. With 4a or 2a, chapters '
             '20 and 21 fall under their allocations, and the build holds part of the saving until those chapters leave '
             'its list of chapters in progress: C3’s projection holds 594,413 bytes that way.'),
    'rows': [
        {'option': '1a. Release chapter 15’s hold, which Gate 3’s approval left in the build', 'saved': '29,899 off the projection', 'loss': 'None', 'touches': 'The build’s settings only', 'proof': 'The build report’s hold'},
        {'option': '1b. Chapters 22 to 25, 27 and 28 estimated again from units measured on this page', 'saved': 'None; a forecast', 'loss': 'None', 'touches': 'None', 'proof': 'Mid 2,269,789 and high 3,895,739 against the 1,972,000 allocated'},
        {'option': '2a. Every 1440 and 1024 px frame of a page that also has a phone frame becomes a line naming its export', 'saved': '643,013', 'loss': 'A desktop reader no longer sees those pages’ desktop and tablet layouts, light or dark; the export opens only where the asset package sits beside the guide', 'touches': '20, 21', 'proof': 'Changes the screen by design'},
        {'option': '2b. Only the 1024 px frames and the 1440 px dark frames', 'saved': '326,796', 'loss': 'The tablet width of chapter 20’s pages and every page’s dark desktop', 'touches': '20, 21', 'proof': 'Changes the screen by design'},
        {'option': '2c. Only the 1440 px dark frames', 'saved': '236,683', 'loss': 'The dark desktop; dark stays at 390 px', 'touches': '20, 21', 'proof': 'Changes the screen by design'},
        {'option': '3a. Each plate style drawn once, shared by every plate that repeats it', 'saved': '799,531', 'loss': 'None', 'touches': 'Every chapter but 14 and 15, approved ones among them (their output, never their sources)', 'proof': 'Inside C1’s 764 of 764 identical captures'},
        {'option': '3b. The page’s PNGs compressed again without loss', 'saved': '40,600', 'loss': 'None', 'touches': '04, 09, 10, 17 (approved)', 'proof': 'Decoded pixels the same; inside C1’s captures'},
        {'option': '3c. Chapter 20’s repeated drawings drawn once and placed by reference', 'saved': '58,999', 'loss': 'None', 'touches': '20', 'proof': 'Inside C1’s captures'},
        {'option': '3d. Quote marks and angle brackets written as themselves where the page escapes them', 'saved': '38,548', 'loss': 'None', 'touches': '18 and 26 mostly (approved)', 'proof': 'The same document in Chromium, character for character'},
        {'option': '3e. The latin-ext font faces left out', 'saved': '193,255', 'loss': 'None on this page; a later chapter printing an accented name outside Latin-1 would get a fallback font', 'touches': 'Every chapter’s type', 'proof': 'No character on the page in their ranges'},
        {'option': '3i. The frame parts no reader meets left out (PR-S7)', 'saved': '81,008', 'loss': 'None on screen; a frame stops matching its export’s markup word for word', 'touches': '20, 21', 'proof': 'Measured by computed style; not built'},
        {'option': '4a. Chapters 20 and 21’s frames carried compressed and opened at load', 'saved': '1,284,042', 'loss': 'A sighted reader with scripts off sees each plate’s label over an empty stage; a screen reader still hears each frame’s alt', 'touches': '20, 21', 'proof': 'Measured; not proved this chat'},
        {'option': '4c. The two token downloads carried compressed', 'saved': '516,489', 'loss': 'A reader with scripts off cannot download tokens.css or tokens.json', 'touches': '26 (approved), the colophon', 'proof': 'Bytes only'},
    ],
    'combos': [
        {'name': 'Today', 'page': '14,444,690', 'projection': '16,466,622'},
        {'name': 'C1, keeps everything: 1a, 3a, 3b, 3c and 3d', 'page': '13,507,012', 'projection': '15,509,989'},
        {'name': 'C2: C1 and 3e', 'page': '13,313,757', 'projection': '15,316,734'},
        {'name': 'C3: C2 without 3c, and 4a', 'page': '12,089,362', 'projection': '14,686,752'},
        {'name': '4a alone', 'page': '13,160,648', 'projection': '15,740,130'},
        {'name': '2a alone', 'page': '13,801,677', 'projection': '16,002,621'},
    ],
}
A21_FINAL = True           # True once A21's frames carry the editor's words and the data lead's sign-off
OPENERS_FINAL = True       # True once the opener captures come from a page built after CD-R1 (chapter 21's load state)
# The guide check's runs on the final page (the main session, from $S/check/selftest.json and $S/check5/run.log)
GUIDE_CHECK = {
    'selftest': ('The guide check’s self-test, on the tree of commit 8ac73595 from 01:21 to 01:38 UTC, caught 167 of 167 '
                 'planted faults and left 63 of 63 allowed cases alone.'),
    'four_widths': 'PENDING',
    'not_tested': ('The four-width check ran with its own screenshots turned off. Its first run stopped at 03:21 UTC when a '
                   'screenshot timed out on a photograph, so that run is not counted. Every test other than the '
                   'screenshots ran.'),
}

# A21, the application kit's video frame with chart S04 (Engineer W), as exported; alt text read from the frames
A21 = [
    ('20261124_Video-Frame-S04-Vertical-1080x1920', 'Vertical frame, 1080 by 1920 px', 360,
     'The vertical video frame on Newsprint, with chart S04 drawn by the chart kit in its upper part: reported voting by age in 2020 and 2024. 18 to 24 at 47.7 percent, down 3.7 points from 51.4; 25 to 44 at 60.2, down 2.4 from 62.6; 45 to 64 at 70.0 against 71.0, too close to call; 65 and over at 74.7 against 74.5, no clear change. A full-width Charcoal band holds S04’s source line and the caption Citizens 18 to 24 reported voting at 47.7 percent, down 3.7 points. A small O&A mark at the top right.'),
    ('20261124_Video-Frame-S04-Vertical-Safe-Areas-1080x1920', 'Vertical frame with its safe areas', 360,
     'The same vertical frame with its safe-area overlay switched on: a dashed box marks the area clear of the app, labeled 120 px and 269 px at the top and 672 px at the foot, a hatched column at the right marks TikTok’s buttons, and words under the box name TikTok’s and Instagram’s ad guides, retrieved November 21, 2026.'),
    ('20261124_Video-Frame-S04-Vertical-Misheard-Caption-1080x1920', 'Failure: a misheard caption', 360,
     'The vertical frame as a failure: the caption reads Citizens 18 to 24 reported voting at 47.7 percent, down 37 points, where the chart says 3.7.'),
    ('20261124_Video-Frame-S04-Storyboard-0-08-1920x1080', 'Storyboard at 0:08, 1920 by 1080 px', 640,
     'The storyboard frame at 0:08 on Newsprint: chart S04 at video size across the upper left with its source line under it, and a full-width Charcoal caption band at the foot, Citizens 18 to 24 reported voting at 47.7 percent, down 3.7 points.'),
    ('20261124_Video-Frame-S04-Storyboard-0-30-Safe-Areas-1920x1080', 'Storyboard at 0:30, with its safe areas', 640,
     'The storyboard frame at 0:30 with its safe areas shown: the same chart and source line, the caption So the gap between the youngest and the oldest grew from 23 points to 27, a dashed box 96 px in from the left and 54 px from the top labeled Our margin until chapter 23 sets one, and a hatched band 54 px tall across the foot labeled The player’s controls.'),
]

# ================================================================ the decisions, ranked

REPLY = None   # written from DECISIONS (D4-428): the settled items are named one by one

DECISIONS = [
    {
        'id': 'd-chapters', 'title': 'Chapters 16, 20 and 21 as built',
        'codes': 'Gate 3 report, section 9; C16-V (DR-191)',
        'what': 'Chapter 16, Photography, illustration and video; chapter 20, Web, which draws your website; and chapter '
                '21, The atlas. After chat 12’s review and fix pass, the creative director passed 15 of their 16 items '
                'at 4 or more on all six criteria. C16-V, the video rules 16.10 to 16.13, took this chat’s second pass: '
                'chart S04 now fills the video frames, and C16-V reaches 4 on every criterion, so all 16 items pass.',
        'rec': 'Approve chapter 16’s rules, the website’s look at its four widths in both themes, and the atlas’s views.',
        'see': 'ch16',
    },
    {
        'id': 'd-nf1', 'byname': True, 'title': 'Ampersand B in a hinge headline, on Newsprint',
        'codes': 'DD10-NF1; locked identity, so its own named approval (CLAUDE.md gate rule 4)',
        'what': 'In a hinge headline such as “The zoning code & the rent.”, B stands for the word “and” in a line a '
                'reader must read, so the accessibility lead rules it is text. Pillar Red on Newsprint measures 2.96 to '
                '1, under the 3 to 1 that WCAG 2.2 sets for large text (criterion 1.4.3), and WCAG does not round. B in '
                'the wordmark, the lockmark, the favicon, the avatars and the badge names the brand and keeps WCAG’s '
                'logotype exception.',
        'rec': 'On Newsprint, give a hinge headline’s B Rule 05.3’s keyline, a 1 px Charcoal edge drawn inside the mark '
               '(13.29 to 1). B keeps its red, its shape and its size. On White (4.17 to 1) and Charcoal (4.49 to 1) B '
               'already passes and takes no keyline. The other way, B in the headline’s ink, needs no keyline and '
               'spends no red, and it changes Rule 04.3’s red moment.',
        'see': 'x-nf1',
    },
    {
        'id': 'd-weight', 'title': 'The page’s weight and the room for chapters 22 to 28',
        'codes': 'C11C-W1, PR-S7 (DR-271)',
        'what': None,   # filled from the build report
        'rec': 'The creative director’s order: the lossless savings first, combination C1, which keeps every word, form '
               'and picture and moves no pixel at 1440 or 390 px; then allocations estimated again from measured units, '
               'shown as a forecast beside the projection; then wide frames as exports, only for the frames a reader '
               'meets today at half size or smaller (C11-1, the next decision). C1 changes the bytes of approved '
               'chapters’ output with no pixel moved, so it needs your word. Leave PR-S7’s strip, the frame parts no '
               'reader meets, for later, since a frame would then differ from its export’s markup. Hold 3e, the '
               'latin-ext faces, until chapters 22 to 25 are written, and keep 4a, the compressed frames, as the reserve.',
        'see': 'x-weight',
    },
    {
        'id': 'd-c111', 'title': 'Wide page frames on a phone',
        'codes': 'C11-1, with C11C-W1’s option 2',
        'what': None,   # filled from the capture's measure of Rule 20.7's plate at 390 px
        'rec': 'Under 48em, show the 390 and 360 px frames first, and turn each wide frame into a line that opens its '
               'export at true size, as the accessibility and craft readers propose. The production reader’s other way '
               'keeps each wide frame inside the guide’s one file, in a scroll box at true size.',
        'see': 'x-c111',
    },
    {
        'id': 'd-e11b', 'title': 'Chapter 18’s masthead code: the current part and the menu’s first row',
        'codes': 'E11b-1 and E11b-2, approved chapter 18',
        'what': 'The masthead reads any aria-current attribute as the current part, including aria-current="false", '
                'which some page builders write on every other link, so a partner’s copy would draw every part as current '
                'and open the menu on the first (E11b-1). No page writes "false" today. In the open menu, the 2 px focus '
                'ring on the first row draws its top side under the title row’s 1 px rule (E11b-2); WCAG 2.4.11 is met, '
                'and the website’s own menu leaves a gap there.',
        'rec': 'Apply both as one change to chapter 18’s code set: match [aria-current]:not([aria-current="false"]), as '
               'the guide check already reads it, and leave a 4 px gap between the title row and the first row, as '
               'the website does.',
        'see': 'x-e11b',
    },
    {
        'id': 'd-r14d', 'byname': True, 'title': 'Chapter 15’s red target case on a dark page',
        'codes': 'C11C-R14d, approved chapter 15 (G3-01)',
        'what': 'Seven of chapter 15’s drawings draw the 6 px case under a red target in the surface’s essential ink. '
                'Every guide plate sits on Newsprint, where that ink is Charcoal, so no reader meets a fault today. A '
                'builder who reuses the drawing on a Charcoal page gets a light rim beside the red line, as five plates '
                'showed under a Charcoal stage.',
        'rec': 'Draw the case in the on-Newsprint ink token, as chapter 21 draws it. On Newsprint no pixel changes; on '
               'Charcoal the rim goes.',
        'see': 'x-r14d',
    },
    {
        'id': 'd-1516', 'byname': True, 'title': 'One sentence for Rule 15.16 on the effects’ confidence',
        'codes': 'Rule 15.16’s confidence sentence, approved chapter 15',
        'what': 'Rules 15.16 and 15.20 do not name the confidence words the atlas stores for a reform’s effects. The data '
                'lead requires them (R12), and chapter 21’s reform and loop pages print them, so the next builder of a '
                'reform chooser could miss them.',
        'rec': 'Add one sentence to Rule 15.16: “Print the atlas’s confidence in these effects, quoted as stored, once '
               'under the four rows.”',
        'see': 'x-1516',
    },
    {
        'id': 'd-length', 'byname': True, 'title': '“The same length” in Rules 01.16 and 13.2',
        'codes': 'Rules 01.16 and 13.2, approved chapters 01 and 13',
        'what': 'Both rules ask for the two readings of a contested claim at the same length. Chapter 21 prints the '
                'atlas’s stored readings at the length the record holds (D4-253), so a reader who sets Rule 01.16 beside '
                'Reform R-23’s page sees the guide break its own rule.',
        'rec': 'Rule 01.16’s Length row gains “Readings quoted from a record print at the length the record holds '
               '(DR-37, DR-93); readings we write run the same length”, and Rule 13.2’s Contested row cites it.',
        'see': 'x-length',
    },
    {
        'id': 'd-prm1', 'title': 'Rule 15.15’s plate after the style leak',
        'codes': 'PR-M1, approved chapters 14 and 15',
        'what': 'From chat 11 until chat 12’s fix pass, the share card’s style leaked into three approved plates and drew '
                'a 1,200 by 630 px Charcoal block over Rule 15.15’s drawing and Rule 14.143’s two plates. Engineer W '
                'scoped every kit style to its own frames, and no file of chapter 14 or 15 changed.',
        'rec': 'Keep the fix. Against version 15 of the chapters page, 12 of 24 captures match pixel for pixel and 12 '
               'differ by anti-aliasing or a 1 px shift, which also shows on plates the leak never reached.',
        'see': 'x-prm1',
    },
    {
        'id': 'd-prussian', 'title': 'Prussian beside the red target in the dark theme',
        'codes': 'The creative director’s risk, held for board 1',
        'what': 'In the dark theme, the stepper’s current step fills with Prussian, chapter 18’s approved selected look. '
                'On Loop R18’s page that band sits about 250 px under the reform’s red targets. It marks the step a '
                'reader is on, and the creative director and the craft reader each read it as a state and found no red '
                'and blue pairing.',
        'rec': 'Keep chapter 18’s selected look in both themes.',
        'see': 'x-prussian',
    },
    {
        'id': 'd-134', 'byname': True, 'title': 'Two meanings of a dashed line',
        'codes': 'Rule 13.4, approved chapter 13',
        'what': 'A dashed line means plausible in chapters 13, 15 and 21. A dashed edge means unavailable or empty in '
                'chapters 17 and 18. On Loop R18’s page the two sit about 300 px apart: the weakest step, and the '
                'Previous step and Reset buttons before a reader starts.',
        'rec': 'Keep both, and at Phase 5 add one sentence to Rule 13.4 saying a dashed line carries a grade only on a '
               'connection. The sentence in the picture is the studio’s draft; the editor writes the final words.',
        'see': 'x-134',
    },
    {
        'id': 'd-s66', 'byname': True, 'title': 'Chart S66’s source line',
        'codes': 'S66’s source line, the approved chart kit (G3-02); low',
        'what': 'The line ends “Steps as the law sets them, not how long agencies take.”, the turn chapter 02’s W09 '
                'removes. It prints under chart S66 in chapter 14 and on the Act page.',
        'rec': 'Use the wording of the chart’s own note: “Steps as the law sets them; how long an agency takes is its '
               'own practice.”',
        'see': 'x-s66',
    },
]

# ================================================================ alt text for the exports (read from the pictures)

HEAD_WIDE = ('the masthead with the wordmark, its lockmark, the seven parts Explain, Track, Connect, Act, Who Do They '
             'Answer To?, About and Subscribe, and the theme switch, Light, Dark and Match my device')
HEAD_PHONE = 'the masthead with the wordmark and a Menu button'
WEB_PAGES = [
    ('home', '20261121_Web-Home-Page', 'Home page'),
    ('article', '20261121_Web-Article-Page-Special-Districts', 'Article page'),
    ('act', '20261121_Web-Act-Page-Comment-On-A-Proposed-Rule', 'Act page'),
]
WEB_VIEWS = [(1440, 'Light'), (1024, 'Light'), (390, 'Light'), (360, 'Light'), (1440, 'Dark'), (390, 'Dark')]
WEB_ALT = {
    'home': {
        (1440, 'Light'): f'The home page’s first screen at 1440 px on Newsprint: {HEAD_WIDE}, Light chosen. A Charcoal band holds the four pillar cells with their icons, Explain, Track, Connect and Act. Under them sit four pieces: the explainer What a special district does; the tracker for H.R. 7008, the Stop Insider Trading Act, at step 5 of 6, Second chamber, with its source line; the guide Who sets your electric bill; and Comment on the FDA’s proposed rule on NAC, its step 3 marked with a red dot, with the link How to send a comment.',
        (1024, 'Light'): f'The home page’s first screen at 1024 px on Newsprint: {HEAD_WIDE}. The pillar band holds Explain and Track over two columns: the explainer What a special district does, and the H.R. 7008 tracker at step 5 of 6 with its source line.',
        (390, 'Light'): f'The home page’s first screen at 390 px on Newsprint: {HEAD_PHONE}. The Explain cell on Charcoal, the explainer What a special district does, then the Track cell and the start of the H.R. 7008 tracker.',
        (360, 'Light'): f'The home page’s first screen at 360 px on Newsprint: {HEAD_PHONE}, the wordmark from its smaller master. The Explain cell, the explainer, the Track cell and the top of the tracker.',
        (1440, 'Dark'): 'The home page’s first screen at 1440 px in the dark theme on Charcoal, Dark chosen: the same masthead, the pillar row edged by thin rules, and the same four pieces with the red dot on the NAC rule’s step 3.',
        (390, 'Dark'): 'The home page’s first screen at 390 px in the dark theme: the masthead with Menu, then the Explain and Track cells edged by thin rules, the explainer and the start of the tracker.',
    },
    'article': {
        (1440, 'Light'): f'The article’s first screen at 1440 px on Newsprint: {HEAD_WIDE}, Explain underlined as the current part. The pillar row in small type, the kicker Explainer, Local government, the headline What a special district does in display type, the opening paragraph and the byline Dustin Cathcart, Founder and Editor, November 21, 2026. A Charcoal count panel at the right reads 39,555 special districts in 2022, the most common kind of government, of the 90,888 governments the Census Bureau counted, over the start of its source line.',
        (1024, 'Light'): f'The article’s first screen at 1024 px on Newsprint: {HEAD_WIDE}, Explain current. The headline, the opening paragraph and the byline, with the Charcoal count panel, 39,555, at the right.',
        (390, 'Light'): f'The article’s first screen at 390 px on Newsprint: {HEAD_PHONE}. The pillar row on two lines with Explain current, the kicker, the headline on three lines, the opening paragraph and the top of the Charcoal count panel, 39,555 special districts in 2022.',
        (360, 'Light'): f'The article’s first screen at 360 px on Newsprint: {HEAD_PHONE}, from the smaller master. The pillar row, the kicker, the headline on three lines, the opening paragraph and the top of the count panel.',
        (1440, 'Dark'): 'The article’s first screen at 1440 px in the dark theme, Dark chosen: the same headline, paragraph and byline in light type on Charcoal, and the count panel, 39,555, edged by a thin rule.',
        (390, 'Dark'): 'The article’s first screen at 390 px in the dark theme: the headline on three lines, the opening paragraph and the top of the count panel edged by a thin rule.',
    },
    'act': {
        (1440, 'Light'): f'The Act page’s first screen at 1440 px on Newsprint: {HEAD_WIDE}, Act underlined as the current part. The headline How to comment on the FDA’s proposed rule on NAC in display type, and a paragraph saying anyone may comment until January 19, 2027, with the docket FDA-2025-N-2699. A Charcoal panel at the right, Where the rule stands, lists six steps: Early notice, done, April 22, 2022; Proposed, done, November 17, 2026; Comments open, now, until January 19, 2027, marked with a red dot; then Comments closed, Final rule and In effect, not yet. Under them, You can take part now, and the docket number.',
        (1024, 'Light'): f'The Act page’s first screen at 1024 px on Newsprint: {HEAD_WIDE}, Act current. The headline, the opening paragraph and the status panel Where the rule stands, its steps running to the window’s foot with step 3, Comments open, marked by a red dot.',
        (390, 'Light'): f'The Act page’s first screen at 390 px on Newsprint: {HEAD_PHONE}. The pillar row with Act current, the headline on four lines, the opening paragraph and the head of the status panel, Where the rule stands.',
        (360, 'Light'): f'The Act page’s first screen at 360 px on Newsprint: {HEAD_PHONE}, from the smaller master. The headline on five lines, the opening paragraph and the top edge of the status panel.',
        (1440, 'Dark'): 'The Act page’s first screen at 1440 px in the dark theme, Dark chosen: the headline and paragraph in light type on Charcoal, and the status panel edged by a thin rule, its step 3 marked with a red dot.',
        (390, 'Dark'): 'The Act page’s first screen at 390 px in the dark theme: the headline on four lines, the opening paragraph and the head of the status panel, edged by a thin rule.',
    },
}
WEB_STILLS = [
    ('20261121_Web-Menu-Open-390-Light', 'Menu open, 390 px, light', 'The menu open at 390 px on Newsprint: a title row with Menu and Close the menu, the theme switch with Light chosen, Dark and Match my device, then the seven parts as rows, Explain marked as the current part with a bar at its left.'),
    ('20261121_Web-Menu-Open-360-Light', 'Menu open, 360 px, light', 'The menu open at 360 px on Newsprint, the same rows, with Match my device on a second line of the theme switch.'),
    ('20261121_Web-Menu-Open-390-Dark', 'Menu open, 390 px, dark', 'The menu open at 390 px on Charcoal, Dark chosen, with Explain on a Prussian band as the current part.'),
    ('20261121_Web-Share-Preview-Special-Districts-1200x630', 'Share preview, 1200 by 630 px', 'The share preview card on Newsprint: the kicker Explainer, Local government, and the headline What a special district does on two lines, over a Charcoal band with the wordmark at the left and the lockmark at the right.'),
]
ATLAS_VIEWS = [
    ('home', '20261122_Atlas-Home-Page', 'Atlas home', [(1440, 'Light'), (1440, 'Dark'), (390, 'Light'), (390, 'Dark')]),
    ('reform', '20261122_Atlas-Reform-R-23-Page', 'Reform R-23', [(1440, 'Light'), (1440, 'Dark'), (390, 'Light'), (390, 'Dark')]),
    ('register', '20261122_Atlas-Register-D04-Page', 'The Register, sheet D04', [(1440, 'Light'), (1440, 'Dark'), (390, 'Light'), (390, 'Dark')]),
    ('loop', '20261122_Atlas-Loop-R18-Page', 'Loop R18', [(1440, 'Light'), (1440, 'Dark'), (390, 'Light'), (390, 'Dark')]),
    ('howto', '20261122_Atlas-How-To-Read-Page', 'How to read', [(1440, 'Light'), (390, 'Light')]),
    ('index', '20261122_Atlas-Loop-Index-Page', 'The loop index', [(1440, 'Light'), (390, 'Light')]),
]
ATLAS_BAR = 'the site’s masthead with Who Do They Answer To? current, then the atlas’s Charcoal title bar, Who do they answer to?, The Oath & Action Systems Atlas, Snapshot of October 15, 2026'
ATLAS_BAR_PHONE = 'the site’s masthead with Menu, then the atlas’s Charcoal title bar with its snapshot date and a Views button'
ATLAS_ALT = {
    'home': {
        'wide': f'the atlas home’s first screen: {ATLAS_BAR}, with the views Home, Loops, Reforms, The Register and How to read, Home current. A Charcoal band holds the title Who do they answer to?, a paragraph saying our systems atlas holds 51 variables and 118 connections, traces 23 loops, weighs 50 reforms and files 194 issue records, and the button Show every variable. Below, the whole system: Outside forces across the top, then Wealth, Voice, Elections, Checks and Policy, each with its question and its counts, and Your household and Technology beneath, joined by arrows that each carry a count, with the key under the drawing.',
        'phone': f'the atlas home’s first screen: {ATLAS_BAR_PHONE}. The title Who do they answer to? with Show every variable, the paragraph of counts, and the first parts as stacked boxes, Outside forces with its arrows listed in words, then Wealth.',
    },
    'reform': {
        'wide': f'Reform R-23’s first screen: {ATLAS_BAR}, Reforms current, then the trail Home, Reforms, Reform R-23 and a small locator. The chip Reform R-23 and the kind Parameter, the title Minimum wage that rises with an index in display type and a paragraph on what it would do. A Charcoal panel, Where it stands, gives the check date October 15, 2026, the state count and the two grades, Documented for the problem and Contested for the remedy. Below begins Where it acts, the variable Household income outlined in red.',
        'phone': f'Reform R-23’s first screen: {ATLAS_BAR_PHONE}. The trail, the chip and kind, the title on three lines, the paragraph, and the top of the Where it stands panel.',
    },
    'register': {
        'wide': f'The Register’s first screen with sheet D04 chosen: {ATLAS_BAR}, The Register current. A Charcoal band holds the title The Register and a paragraph on how the atlas files every connection once. Below, the index of sheets as a table: each sheet’s chip and name with its counts of variables, connections, numbered loops, reforms and issue records, and one column for each grade, Documented, Well supported, Plausible, Contested and Hypothesis, each headed by its line sample.',
        'phone': f'The Register’s first screen: {ATLAS_BAR_PHONE}. The chip Domain D04, the title The Register, the paragraph, a Charcoal key of the five grade lines, and the first sheet’s card with its counts.',
    },
    'loop': {
        'wide': f'Loop R18’s first screen: {ATLAS_BAR}, Loops current. The chip Loop R18 and Reinforcing loop, the quoted title “Weakening watchdogs lowers the cost of further unilateral action” in display type, and the line Documented for Connection L14, Plausible for Connection L15. A Charcoal panel, This loop, lists its kind, two steps, two minus signs, how it closes, a delay of 2 to 10 years and its weakest step, Connection L15, Plausible. The band Step through the loop begins at the foot.',
        'phone': f'Loop R18’s first screen: {ATLAS_BAR_PHONE}. The chip, the quoted title on five lines, the grade line with its two chips, How it closes, and the top of the This loop panel.',
    },
    'howto': {
        'wide': f'How to read’s first screen: {ATLAS_BAR}, How to read current. A Charcoal band holds the title How to read our atlas. Below, Signs and types: the plus sign, raises; the minus sign, lowers; money, information and ownership; and the open diamond, decides, each drawn beside its meaning, then the heading Grades.',
        'phone': f'How to read’s first screen: {ATLAS_BAR_PHONE}. The Charcoal band with the title, then Signs and types with the plus and minus signs drawn beside their meanings.',
    },
    'index': {
        'wide': f'The loop index’s first screen: {ATLAS_BAR}, Loops current. The title Every loop in our atlas and a paragraph on reinforcing and balancing loops, a Charcoal band Reinforcing (18), and the table’s first rows: Loop R1 and Loop R1b with their titles, steps, minus signs, how each closes and its grade.',
        'phone': f'The loop index’s first screen: {ATLAS_BAR_PHONE}. The title, the paragraph, the Charcoal band Reinforcing (18), and the first loop’s card.',
    },
}

# ================================================================ captured pictures and their words

def cap_alt_ch16(sid, rules):
    if sid == 's-16-opener':
        return 'Chapter 16’s opening figure as the guide draws it at 1440 px.'
    if sid == 's-16-picture-kinds':
        return 'The table after Rule 16.9: five kinds of picture, where each may appear, how each is labeled and the rule that sets it.'
    m = re.match(r's-16-(\d+)-(correct|failure)', sid)
    rid = f'16.{m.group(1)}'
    kind = 'correct application' if m.group(2) == 'correct' else 'failure case'
    return f'Rule {rid}’s {kind} as the guide draws it at 1440 px: {rules[rid]["correct" if m.group(2) == "correct" else "failure"]["caption_text"]}'


# ================================================================ helpers

def save_webp(src, name, crop=None, scale=None):
    """A lossless WebP in img/; returns (file name, pixel width, pixel height)."""
    im = Image.open(src)
    im = im.convert('RGBA') if im.mode in ('P', 'LA', 'RGBA') else im.convert('RGB')
    if crop:
        im = im.crop(crop)
    if scale:
        im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
    fn = f'{DAY}_{name}.webp'
    im.save(IMG / fn, 'WEBP', lossless=True, quality=80, method=4, exact=True)   # lossless; quality sets effort only
    return fn, im.width, im.height


def fig(fn, css_w, css_h, alt, cap, cls='', link=None, eager=False, pixel=False):
    lazy = '' if eager else ' loading="lazy"'
    style = ' class="px"' if pixel else ''
    img = (f'<img src="img/{fn}" width="{css_w}" height="{css_h}"{lazy} decoding="async"{style} '
           f'alt="{e(alt)}">')
    if link:
        img = f'<a class="imglink" href="img/{link}" target="_blank" rel="noopener">{img}</a>'
    return f'<figure class="pic {cls}">{img}<figcaption>{cap}</figcaption></figure>'


def labels(*ls):
    return ''.join(f'<span class="label">{e(x)}</span>' for x in ls)


def slot(text):
    return f'<div class="slot" role="note"><p class="slot-k">To come</p><p>{text}</p></div>'


def plain(s):
    return re.sub(r'<[^>]+>', '', s)


# ================================================================ inputs

def load_inputs(args):
    rep = json.loads(Path(args.report).read_text())
    scores = json.loads((ROOT / 'work/handoffs/phase-4/20261123_Chat-12-CD-Scores.json').read_text())
    specs = json.loads((ROOT / 'work/research/20261121_Platform-Specifications.json').read_text())
    atest = json.loads((ROOT / 'work/build/app-kit/plates/atlas-test.json').read_text())
    chapters = {}
    for f in ['16-photography', '20-web', '21-atlas']:
        chapters[f[:2]] = json.loads((ROOT / f'work/build/guide/chapters/{f}.json').read_text())
    caps = Path(args.caps)
    meta = json.loads((caps / 'caps.json').read_text()) if (caps / 'caps.json').exists() else {}
    return rep, scores, specs, atest, chapters, caps, meta


def rule_words(ch):
    out = {}
    for r in ch['rules']:
        rule = r['rule'] if isinstance(r['rule'], str) else ' '.join(r['rule'])
        d = {'title': r['title'], 'rule': plain(rule)}
        for k in ('correct', 'failure'):
            c = r.get(k) or {}
            d[k] = {'caption_text': re.sub(r'^Fails Rule \d+\.\d+\.\s*', '', plain(c.get('caption', '')))}
        out[r['id']] = d
    return out


# ================================================================ sections

def sec_decisions(rep):
    w = rep['weight']
    pr = w['projection']
    over = pr['projected_bytes'] - w['limit']
    for d in DECISIONS:
        if d['id'] == 'd-weight':
            d['what'] = (f'The page of record weighs {n(w["bytes"])} bytes. The build projects {n(pr["projected_bytes"])} '
                         f'once chapters 22 to 25, 27 and 28 reach their allocations, {n(over)} bytes past the page’s '
                         '16 MB limit, the only figure that stops a build (DR-271). Nothing was cut. Combination C1 saves '
                         '937,678 bytes, keeps every word, form and picture, and brings the projection to 15,509,989, '
                         '490,011 under 16 MB; 764 of 764 plate captures came out identical. C2, which also leaves out '
                         'the latin-ext font faces, reaches 15,316,734, and C3, which also carries chapters 20 and 21’s '
                         'frames compressed, reaches 14,686,752 at a cost to readers with scripts off. Estimated again '
                         'from units measured on this page, chapters 22 to 28 could need 2,269,789 bytes, or 3,895,739 at '
                         'the high estimate, against the 1,972,000 allocated.')
    sc = {f['frame'].split(' ')[1]: f for f in META.get('c111-scale', [])}
    for d in DECISIONS:
        if d['id'] == 'd-c111':
            if sc.get('1440-light') and sc.get('390-light'):
                a, b = sc['1440-light'], sc['390-light']
                pa, pb = round(100 * a['shown'] / a['w']), round(100 * b['shown'] / b['w'])
                d['what'] = (f'On a 390 px phone, Rule 20.7’s plate draws the 1440 px article page {a["shown"]} px wide, '
                             f'{pa} percent of its size, and its three phone frames side by side at {b["shown"]} px each, '
                             f'{pb} percent, so a 16 px line of the page prints between 3 and 4 px. The label over the '
                             'first frame reads “1440 px, light, shown at 50 percent on a 1440 px screen” (D4-422), so it '
                             'states its scale on a desktop. Chapters 20 and 21’s other page plates draw the same way.')
            else:
                d['what'] = 'On a 390 px phone the guide draws chapters 20 and 21’s wide page frames at about a fifth of their size.'
    def listed(xs):
        xs = [str(x) for x in xs]
        return xs[0] if len(xs) == 1 else ', '.join(xs[:-1]) + ' and ' + xs[-1]
    plain_ = [i for i, d in enumerate(DECISIONS, 1) if not d.get('byname')]
    named = [i for i, d in enumerate(DECISIONS, 1) if d.get('byname')]
    reply = f'Board 1: items {listed(plain_)} as recommended; and by name, items {listed(named)} as recommended.'
    items = []
    for i, d in enumerate(DECISIONS, 1):
        items.append(
            f'<li class="dec" id="{d["id"]}"><div class="dec-n" aria-hidden="true">{i}</div><div class="dec-b">'
            f'<h3><span class="vh">Decision {i}: </span>{e(d["title"])}</h3><p class="code">{e(d["codes"])}</p>'
            + ('<p><span class="label">Settled work: needs your answer by name</span></p>' if d.get('byname') else '') +
            f'<p>{e(d["what"])}</p>'
            f'<p class="rec"><strong>The studio recommends:</strong> {e(d["rec"])}</p>'
            f'<p class="seelink"><a href="#{d["see"]}">See the pictures and figures</a></p></div></li>')
    return (
        '<section aria-labelledby="h-decide"><h2 id="h-decide">What you decide</h2>'
        f'<p>{num(len(DECISIONS)).capitalize()} items, ranked by how much each changes: the three chapters first, then '
        'the change to locked identity, the page’s weight, and the changes to approved chapters, smallest last. '
        'Each lists its register code and the studio’s recommendation, and the pictures for each sit further down the '
        'board, with the original beside the proposal at true size.</p>'
        f'<ol class="decs">{"".join(items)}</ol>'
        '<div class="reply" id="reply"><p class="reply-k">One reply that takes every recommendation</p>'
        f'<p class="reply-t">“{e(reply)}”</p>'
        f'<p class="note">Items {listed(named)} change settled work: locked identity, or a chapter or kit you have '
        'already approved. Each needs your answer by name, so the reply names them.</p>'
        '<p class="note">To answer an item another way, name its number and your answer, as in “3: hold C1”.</p>'
        '</div></section>')


def cmp_row(items):
    """Pictures side by side at true size; each item (fn, css_w, css_h, alt, cap)."""
    return '<div class="cmp">' + ''.join(fig(*it) for it in items) + '</div>'


def capped(caps, meta, key, name, alt, cap, dpr=1, cls=''):
    p = caps / f'{key}.png'
    if not p.exists():
        return slot(f'The capture {e(key)} has not been made yet.')
    fn, pw, ph = save_webp(p, name)
    return fig(fn, round(pw / dpr), round(ph / dpr), alt, cap, cls, link=fn)


def sec_approved(caps, meta, rep):
    S = []
    # ---- DD10-NF1
    S.append(
        '<article class="xitem" id="x-nf1"><h3>Decision 2: ampersand B in a hinge headline (DD10-NF1)</h3>'
        '<p>Rule 04.3’s correct plate as the guide draws it, three hinge headlines at the title, section and H3 sizes, '
        'then the same plate with the keyline drawn inside each B, then the other way. Each picture is at true size; '
        'open any of them to see it alone. The two proposals are studio sketches, drawn in the browser’s copy of the page '
        'for this board; chapter 04’s files are unchanged.</p>')
    S.append(cmp_row([
        cap_item(caps, 'nf1-043-today', 'DD10-NF1-Rule-04-3-Today', 2,
                 'Three hinge headlines on Newsprint at true size: The zoning code & the rent. at 56 px, The filing deadline & the ballot. at 44 px and The records law & the answer. at 26 px, each ampersand B in Pillar Red with no edge.',
                 labels('Today, as approved') + 'Rule 04.3’s plate. B in Pillar Red, 2.96 to 1 on Newsprint.'),
        cap_item(caps, 'nf1-043-keyline', 'DD10-NF1-Rule-04-3-Keyline', 2,
                 'The same three hinge headlines at true size, each ampersand B in Pillar Red with a 1 px Charcoal edge drawn inside the mark.',
                 labels('Recommended', 'Studio sketch') + 'B keeps its red, shape and size, with a 1 px Charcoal keyline inside the mark, 13.29 to 1.'),
        cap_item(caps, 'nf1-043-ink', 'DD10-NF1-Rule-04-3-Ink', 2,
                 'The same three hinge headlines at true size, each ampersand B in the headline’s Charcoal ink.',
                 labels('The other way', 'Studio sketch') + 'B in the headline’s ink: no red spent and no keyline needed.'),
    ]))
    S.append('<p>The keyline at eight times, on the 26 px headline’s B, so its edge shows; each square of the picture is '
             'one eighth of a pixel.</p>')
    S.append(cmp_row([
        cap_item(caps, 'nf1-zoom-today', 'DD10-NF1-B-26px-Today-8x', 1,
                 'Ampersand B from the 26 px headline drawn eight times larger, solid Pillar Red on Newsprint.',
                 labels('Today', 'Eight times') + 'B at 26 px.', pixel=True),
        cap_item(caps, 'nf1-zoom-keyline', 'DD10-NF1-B-26px-Keyline-8x', 1,
                 'The same B eight times larger with its keyline: a Charcoal edge one pixel wide runs inside the red along every contour.',
                 labels('Recommended', 'Eight times') + 'The keyline is one pixel wide at true size.', pixel=True),
    ]))
    S.append('<p>The link-preview card’s headline, B from the display master at 110 px, at true size, as the identity '
             'proofs draw it.</p>')
    S.append(cmp_row([
        cap_item(caps, 'nf1-social-today', 'DD10-NF1-Link-Card-Today', 2,
                 'The link-preview card’s headline at true size: The zoning code on the first line and B, the ampersand, in Pillar Red leading the rent. on the second.',
                 labels('Today') + 'The identity proofs’ link-preview card, 1200 by 630 px, its headline at 110 px.'),
        cap_item(caps, 'nf1-social-keyline', 'DD10-NF1-Link-Card-Keyline', 2,
                 'The same headline at true size, B with a 1 px Charcoal keyline inside the mark.',
                 labels('Recommended', 'Studio sketch') + 'The same B with its keyline.'),
    ]))
    S.append('<p class="note">Where else it applies: the application kit’s Instagram sample, A01 (“The records law & your '
             'answer.”), takes the same keyline. No plate in chapters 16, 20 or 21 draws a hinge headline.</p></article>')

    # ---- weight
    S.append(sec_weight(rep))

    # ---- C11-1
    S.append(
        '<article class="xitem" id="x-c111"><h3>Decision 4: wide page frames on a phone (C11-1)</h3>'
        '<p>Rule 20.7’s correct plate on a 390 px phone, at true size. Today the 1440 px article page comes first, drawn '
        'about a fifth of its size. The proposal is a studio sketch made in the browser’s copy of the page: the 390 and '
        '360 px frames come first, and each wide frame becomes a line that opens its export at true size. The pictures '
        'stop at the first 1,100 px of the plate.</p>')
    S.append(cmp_row([
        cap_item(caps, 'c111-today', 'C11-1-Rule-20-7-390-Today', 2,
                 'Rule 20.7’s plate on a 390 px phone today: under the label 1440 px, light, shown at 50 percent on a 1440 px screen, the whole article page drawn about 290 px wide, its words too small to read, then the start of the 1024 px frame.',
                 labels('Today', '390 px') + 'The 1440 px frame first, about a fifth of its size.'),
        cap_item(caps, 'c111-proposal', 'C11-1-Rule-20-7-390-Proposal', 2,
                 'The same plate in the studio sketch: the 390 px article page first, its masthead, headline, paragraph and count panel readable, and further down a list of the wider pages, each a line that opens it at true size.',
                 labels('Proposed', 'Studio sketch', '390 px') + 'The phone frames first; the wide frames as lines to their exports.'),
    ]))
    S.append('</article>')

    # ---- E11b
    S.append(
        '<article class="xitem" id="x-e11b"><h3>Decision 5: chapter 18’s masthead code (E11b-1 and E11b-2)</h3>')
    e11 = [k for k in ('e11b1-today', 'e11b1-proposal', 'e11b2-today', 'e11b2-proposal') if (caps / f'{k}.png').exists()]
    if len(e11) == 4:
        S.append('<p>E11b-1: a partner’s copy of the masthead that writes aria-current="false" on every part but the '
                 'current one. E11b-2: the open menu with the focus ring on its first row. Both proposals are studio '
                 'sketches in the browser’s copy of chapter 18’s plate; its code files are unchanged.</p>')
        S.append(cmp_row([
            cap_item(caps, 'e11b1-today', 'E11b-1-Today', 2, 'The masthead bar with every part bold and underlined, as if each were the current part.', labels('Today', 'E11b-1') + 'Every part reads as current.'),
            cap_item(caps, 'e11b1-proposal', 'E11b-1-Proposal', 2, 'The same masthead bar with only the current part bold and underlined.', labels('Proposed', 'Studio sketch') + 'Only the current part reads as current.'),
        ]))
        S.append(cmp_row([
            cap_item(caps, 'e11b2-today', 'E11b-2-Today', 3, 'The open menu’s title row and first row, the focus ring’s top side hidden under the title row’s rule.', labels('Today', 'E11b-2') + 'The ring’s top side sits under the rule.'),
            cap_item(caps, 'e11b2-proposal', 'E11b-2-Proposal', 3, 'The same rows with a 4 px gap, the focus ring whole on all four sides.', labels('Proposed', 'Studio sketch') + 'A 4 px gap; the ring shows whole.'),
        ]))
    else:
        S.append(slot('The masthead pictures, today beside the proposal at true size, are captured with the next browser '
                      'run. The change in code: in <code>c-18-masthead.css</code> and <code>c-18-masthead.js</code>, '
                      '<code>[aria-current]</code> becomes <code>[aria-current]:not([aria-current="false"])</code>, and the '
                      'menu’s first row starts 4 px under the title row’s rule.'))
    S.append('</article>')

    # ---- R14d
    S.append(
        '<article class="xitem" id="x-r14d"><h3>Decision 6: chapter 15’s red target case on Charcoal (C11C-R14d)</h3>'
        '<p>Rule 15.12’s correct plate, cropped to its red target, at true size. ' + r14d_same(caps) + ' Under a Charcoal stage, the case today draws a light '
        'rim on each side of the red line; with the on-Newsprint ink the rim goes. The Charcoal stage and the proposal are '
        'studio sketches in the browser’s copy of the page.</p>')
    sid = 's-15-12-correct'
    S.append(cmp_row([
        cap_item(caps, f'r14d-{sid}-newsprint', 'C11C-R14d-Newsprint-Today', 2, 'A vertical red target on Newsprint, a red line in a Charcoal case with ticks, a sign tag and an arrowhead, at true size.', labels('Newsprint, today') + 'As every guide plate draws it.'),
        cap_item(caps, f'r14d-{sid}-newsprint-proposal', 'C11C-R14d-Newsprint-Proposal', 2, 'The same red target on Newsprint with the proposal, identical to today.', labels('Newsprint, proposed') + 'Identical, pixel for pixel.'),
        cap_item(caps, f'r14d-{sid}-charcoal-today', 'C11C-R14d-Charcoal-Today', 2, 'The same red target on a Charcoal stage: a thin light rim runs along both sides of the red line.', labels('Charcoal, today', 'Studio sketch') + 'A light rim beside the red.'),
        cap_item(caps, f'r14d-{sid}-charcoal-proposal', 'C11C-R14d-Charcoal-Proposal', 2, 'The same red target on Charcoal with the case in Charcoal ink: the red line stands with no rim.', labels('Charcoal, proposed', 'Studio sketch') + 'No rim.'),
    ]))
    if (caps / 'r14d-zoom-today.png').exists():
        S.append(cmp_row([
            cap_item(caps, 'r14d-zoom-today', 'C11C-R14d-Charcoal-Today-8x', 1, 'The top of the red line on Charcoal at eight times: light stripes run beside the red.', labels('Charcoal, today', 'Eight times') + 'The rim.', pixel=True),
            cap_item(caps, 'r14d-zoom-proposal', 'C11C-R14d-Charcoal-Proposal-8x', 1, 'The same at eight times with the proposal: red on Charcoal with no stripe.', labels('Charcoal, proposed', 'Eight times') + 'No rim.', pixel=True),
        ]))
    S.append('</article>')

    # ---- 15.16
    S.append(
        '<article class="xitem" id="x-1516"><h3>Decision 7: one sentence for Rule 15.16</h3>'
        '<p>Rule 15.16 as the guide prints it at 1440 px, and the same rule with the sentence in bold where the studio '
        'would place it, after the effects and before the routes. Studio sketch; chapter 15’s files are unchanged.</p>')
    S.append(cmp_row([
        cap_item(caps, 'text-1516-text-today', 'Rule-15-16-Today', 2, 'Rule 15.16’s title and its two paragraphs as the guide prints them.', labels('Today, as approved')),
        cap_item(caps, 'text-1516-text-proposal', 'Rule-15-16-Proposal', 2, 'Rule 15.16 with one new sentence in bold after “and print no row that adds them.”: Print the atlas’s confidence in these effects, quoted as stored, once under the four rows.', labels('Proposed', 'Studio sketch')),
    ]))
    S.append('</article>')

    # ---- 01.16 and 13.2
    S.append(
        '<article class="xitem" id="x-length"><h3>Decision 8: “the same length” in Rules 01.16 and 13.2</h3>'
        '<p>Rule 01.16’s Length row and Rule 13.2’s Contested row, each as the guide prints it and with the new words in '
        'bold. The words for Rule 01.16 are the words and readers reviewer’s; the Contested row’s wording is the studio’s '
        'draft. Studio sketches; chapters 01 and 13 are unchanged.</p>')
    S.append(cmp_row([
        cap_item(caps, 'text-0116-length-today', 'Rule-01-16-Length-Today', 2, 'Rule 01.16’s Length row: The same number of words in each reading.', labels('Rule 01.16, today')),
        cap_item(caps, 'text-0116-length-proposal', 'Rule-01-16-Length-Proposal', 2, 'Rule 01.16’s Length row with the new words in bold: Readings quoted from a record print at the length the record holds (DR-37, DR-93); readings we write run the same length.', labels('Rule 01.16, proposed', 'Studio sketch')),
    ]))
    S.append(cmp_row([
        cap_item(caps, 'text-132-contested-today', 'Rule-13-2-Contested-Today', 2, 'Rule 13.2’s Contested row: Both readings at the same length (Rule 01.16).', labels('Rule 13.2, today')),
        cap_item(caps, 'text-132-contested-proposal', 'Rule-13-2-Contested-Proposal', 2, 'Rule 13.2’s Contested row with the new words in bold: Both readings at the same length, or at the length the record holds for readings quoted from it (Rule 01.16).', labels('Rule 13.2, proposed', 'Studio sketch')),
    ]))
    S.append('</article>')

    # ---- PR-M1
    S.append(
        '<article class="xitem" id="x-prm1"><h3>Decision 9: Rule 15.15’s plate before and after the leak was fixed (PR-M1)</h3>'
        '<p>The before is the page as it was carried at the opening of chat 12, built in scratch from commit bc91667e '
        '(14,189,507 bytes, the page of record then); the after is today’s strict build. Both at true size, 1440 px and '
        '390 px.</p>')
    S.append(cmp_row([
        cap_item(caps, 'prm1-before-1440', 'PR-M1-Rule-15-15-Before-1440', 1, 'Rule 15.15’s correct plate as the page carried it before the fix: a large Charcoal block with rounded corners covers the right half of Loop B4’s drawing and most of Loop R10’s, hiding its pills, its steps and its text.', labels('Before', 'Commit bc91667e', '1440 px')),
        cap_item(caps, 'prm1-after-1440', 'PR-M1-Rule-15-15-After-1440', 1, 'Rule 15.15’s correct plate today: Loop B4 and Loop R10 side by side, Variable C3, Risk of losing office, filled in ink in both, with the connections in and out of it and the atlas’s words on where the two loops meet.', labels('After', 'Today', '1440 px')),
    ]))
    S.append(cmp_row([
        cap_item(caps, 'prm1-before-390', 'PR-M1-Rule-15-15-Before-390', 1, 'The same plate at 390 px before the fix, the Charcoal block over the drawing.', labels('Before', '390 px')),
        cap_item(caps, 'prm1-after-390', 'PR-M1-Rule-15-15-After-390', 1, 'The same plate at 390 px today, the two loops one under the other.', labels('After', '390 px')),
    ]))
    S.append('</article>')

    # ---- Prussian
    S.append(
        '<article class="xitem" id="x-prussian"><h3>Decision 10: Prussian beside the red target</h3>'
        '<p>Loop R18’s working page with the stepper on its first step, as a reader meets it, at true size: the dark '
        'theme, then the light theme for comparison, then the dark theme at 390 px.</p>')
    S.append(cmp_row([
        cap_item(caps, 'prussian-loop-r18-1440-dark', 'Prussian-Loop-R18-1440-Dark', 2, 'Loop R18 in the dark theme at 1440 px with the stepper on step 1: the loop drawing with Reform R-11’s red targets, the lines naming where it acts, the stepper’s buttons, and below them the current step’s row filled in Prussian with a bar at its left.', labels('Dark', '1440 px')),
        cap_item(caps, 'prussian-loop-r18-1440-light', 'Prussian-Loop-R18-1440-Light', 2, 'The same view in the light theme: the current step’s row filled in White on Newsprint under the red targets.', labels('Light', '1440 px')),
        cap_item(caps, 'prussian-loop-r18-390-dark', 'Prussian-Loop-R18-390-Dark', 2, 'The same in the dark theme at 390 px: the red targets above, the stepper, and the Prussian row for step 1.', labels('Dark', '390 px')),
    ]))
    S.append('</article>')

    # ---- 13.4
    S.append(
        '<article class="xitem" id="x-134"><h3>Decision 11: two meanings of a dashed line (Rule 13.4)</h3>'
        '<p>Loop R18’s working page at 1440 px before a reader presses Play, at true size: the weakest step’s dashed red '
        'line, which means plausible, above the Reset and Previous step buttons, whose dashed edges mean unavailable for '
        'now. Then Rule 13.4 with the studio’s draft sentence in bold, a sketch for Phase 5.</p>')
    S.append(cmp_row([cap_item(caps, 'dash-loop-r18-1440', 'Rule-13-4-Two-Dashes-Loop-R18', 2, 'Part of Loop R18’s page at 1440 px: the loop drawing with its weakest step as a dashed red line, the lines that name where Reform R-11 acts, and the stepper row, where Reset the loop and Previous step have dashed edges until a reader presses Next step or Play.', labels('Today', 'Loop R18, 1440 px'))]))
    S.append(cmp_row([
        cap_item(caps, 'text-134-text-today', 'Rule-13-4-Today', 2, 'Rule 13.4’s title and its two paragraphs as the guide prints them.', labels('Today, as approved')),
        cap_item(caps, 'text-134-text-proposal', 'Rule-13-4-Proposal', 2, 'Rule 13.4 with a draft sentence in bold at the end of its first paragraph: A dashed line carries a grade only on a connection; a dashed edge on a box or a button keeps the meaning chapters 17 and 18 give it.', labels('At Phase 5', 'Studio draft')),
    ]))
    S.append('</article>')

    # ---- S66
    S.append(
        '<article class="xitem" id="x-s66"><h3>Decision 12: chart S66’s source line</h3>'
        '<p>The source line as chapter 14’s plate of S66 prints it, and the proposal with the changed words in bold. '
        'Studio sketch; the chart kit’s data is unchanged.</p>')
    S.append(cmp_row([
        cap_item(caps, 'text-s66-source-today', 'S66-Source-Today', 2, 'S66’s source line, ending Steps as the law sets them, not how long agencies take.', labels('Today, as approved')),
        cap_item(caps, 'text-s66-source-proposal', 'S66-Source-Proposal', 2, 'S66’s source line ending Steps as the law sets them; how long an agency takes is its own practice.', labels('Proposed', 'Studio sketch')),
    ]))
    S.append('</article>')
    return ('<section aria-labelledby="h-approved"><h2 id="h-approved">Changes to approved work, beside the originals</h2>'
            '<p>Each item below goes with a decision above. The original is the guide as approved, captured from today’s '
            'strict build; the proposal is a studio sketch, labeled as one. Pictures are at true size on a wide screen, '
            'and on a phone they shrink to the column; open any picture to see it at true size.</p>'
            + ''.join(S) + '</section>')


def same_pixels(a, b):
    if not (a.exists() and b.exists()):
        return None
    from PIL import ImageChops
    x, y = Image.open(a).convert('RGB'), Image.open(b).convert('RGB')
    return x.size == y.size and ImageChops.difference(x, y).getbbox() is None


def r14d_same(caps):
    res = [same_pixels(caps / f'r14d-{sid}-newsprint.png', caps / f'r14d-{sid}-newsprint-proposal.png')
           for sid in CAPTURE_CFG.get('r14d', [])]
    res = [r for r in res if r is not None]
    META['r14d-same'] = res
    if res and all(res):
        return (f'On Newsprint the proposal changes no pixel: today’s and the proposal’s pictures are identical by script on '
                f'{"both" if len(res) == 2 else num(len(res))} plates checked.')
    return 'On Newsprint the two pictures were compared by script and differ; see the notes.'


def cap_item(caps, key, name, dpr, alt, cap, pixel=False):
    p = caps / f'{key}.png'
    if not p.exists():
        return None
    fn, pw, ph = save_webp(p, name)
    return (fn, round(pw / dpr), round(ph / dpr), alt, cap, 'pxl' if pixel else '', fn, False, pixel)


def cmp_row(items):  # noqa: F811  (the form that skips missing captures)
    have = [it for it in items if it]
    if not have:
        return slot('These pictures are captured with the next browser run.')
    return '<div class="cmp">' + ''.join(fig(*it) for it in have) + '</div>'


def sec_weight(rep):
    w = rep['weight']
    pr = w['projection']
    built = pr['phase_4_built']
    rows = ''.join(
        f'<tr><th scope="row">{c}</th><td class="num">{n(v["bytes"])}</td><td class="num">{n(v["allocation"])}</td>'
        f'<td class="num">{round(100 * v["bytes"] / v["allocation"])}</td></tr>' for c, v in sorted(built.items()))
    unb = ''.join(f'<tr><th scope="row">{c}</th><td class="num">{n(v)}</td></tr>' for c, v in sorted(pr['unbuilt'].items()))
    held = ''.join(f'<tr><th scope="row">{c}</th><td class="num">{n(v)}</td></tr>' for c, v in sorted(pr['held_to_allocation'].items()))
    kit = w['application_kit']
    kitrows = ''.join(f'<tr><th scope="row">{e(k)}</th><td>{e(v["chapter"])}</td><td class="num">{n(v["bytes"])}</td></tr>'
                      for k, v in sorted(kit.items(), key=lambda kv: (kv[1]['chapter'], kv[0])))
    table = (WEIGHT_TABLE_HTML() if WEIGHT_TABLE else slot(
        'Engineer M’s final table: each option measured again on this chat’s final page, with its bytes, what a reader '
        'gains or loses, the chapters it touches and its proof, and each combination’s projection against 16,000,000. '
        'Chat 12 measured the same options on the 14,189,507-byte page of its opening '
        '(<code>work/handoffs/phase-4/20261123_Chat-12-Engineer-Notes.md</code>, “Weight options”); chapter 21 has grown '
        'since, so those figures are not repeated here.'))
    return (
        '<article class="xitem" id="x-weight"><h3>Decision 3: the page’s weight</h3>'
        f'<div class="facts"><div class="fact"><b>{n(w["bytes"])}</b><span>bytes, the page of record (strict build)</span></div>'
        f'<div class="fact"><b>{n(pr["projected_bytes"])}</b><span>bytes projected with every unbuilt chapter at its allocation</span></div>'
        f'<div class="fact"><b>{n(w["limit"])}</b><span>bytes, the one limit that stops a build (DR-271)</span></div></div>'
        '<div class="twocol"><div><h4>Phase 4’s built chapters against their allocations</h4>'
        '<table><thead><tr><th scope="col">Chapter</th><th scope="col" class="num">Bytes</th><th scope="col" class="num">Allocation</th><th scope="col" class="num">Percent</th></tr></thead>'
        f'<tbody>{rows}</tbody></table></div>'
        '<div><h4>What the projection adds</h4><table><thead><tr><th scope="col">Unbuilt chapter</th><th scope="col" class="num">Allocation</th></tr></thead>'
        f'<tbody>{unb}</tbody></table><table><thead><tr><th scope="col">Held at its allocation</th><th scope="col" class="num">Bytes</th></tr></thead>'
        f'<tbody>{held}</tbody></table></div></div>'
        '<p class="note">Chapter 15 is still held at its allocation although Gate 3 approved it (option 1a releases the '
        'hold). Chapter 16 is held until board 1 approves it.</p>'
        f'<h4>The weight options, measured on the final page</h4>{table}'
        '<h4>The application kit’s renderers, as the page carries them</h4>'
        '<p>Each renderer’s shared style and code, counted once for its chapter, from the strict build’s report.</p>'
        '<table class="narrow"><thead><tr><th scope="col">Renderer</th><th scope="col">Chapter</th><th scope="col" class="num">Bytes</th></tr></thead>'
        f'<tbody>{kitrows}</tbody></table>'
        '</article>')


def WEIGHT_TABLE_HTML():
    t = WEIGHT_TABLE
    rows = ''.join(f'<tr><th scope="row">{e(r["option"])}</th><td class="num">{e(r["saved"])}</td><td>{e(r["loss"])}</td>'
                   f'<td>{e(r["touches"])}</td><td>{e(r["proof"])}</td></tr>' for r in t['rows'])
    combos = ''.join(f'<tr><th scope="row">{e(c["name"])}</th><td class="num">{e(c["page"])}</td><td class="num">{e(c["projection"])}</td></tr>'
                     for c in t['combos'])
    return (f'<p>{e(t["note"])}</p><div class="tablewrap"><table class="stack"><thead><tr><th scope="col">Option</th><th scope="col" class="num">Bytes saved</th>'
            f'<th scope="col">What a reader gains or loses</th><th scope="col">Chapters touched</th><th scope="col">Proof</th></tr></thead><tbody>{rows}</tbody></table></div>'
            f'<table><thead><tr><th scope="col">Combination</th><th scope="col" class="num">Page</th><th scope="col" class="num">Projection</th></tr></thead><tbody>{combos}</tbody></table>')


def sec_ch16(caps, meta, ch, rep):
    words = rule_words(ch)
    groups = {g['before_rule']: g for g in ch['groups']}
    built = rep['weight']['projection']['phase_4_built']['16']
    out = [
        '<section aria-labelledby="h-ch16" id="ch16"><h2 id="h-ch16">Chapter 16, Photography, illustration and video</h2>',
        f'<p>{e(plain(ch["intro"] if isinstance(ch["intro"], str) else " ".join(ch["intro"])))}</p>' if ch.get('intro') else '',
        f'<p class="note">{len(ch["rules"])} rules in four groups; {n(built["bytes"])} bytes against an allocation of '
        f'{n(built["allocation"])}. Each plate below is the guide’s own frame captured at 1440 px from today’s strict build, at '
        'true size; open any plate to see it alone.</p>',
    ]
    op = caps / 'opener-16-1440.png'
    if op.exists():
        fn, pw, ph = save_webp(op, 'Chapter-16-Opening-1440')
        out.append(fig(fn, pw, ph, 'Chapter 16’s opening as the guide prints it at 1440 px: the chapter title, its introduction and its opening figure.',
                       labels('Chapter 16’s opening', '1440 px'), link=fn))
    for r in ch['rules']:
        rid = r['id']
        if rid in groups:
            g = groups[rid]
            out.append(f'<h3 class="grp">Group {g["number"]}: {e(g["title"])}</h3><p>{e(g["line"])}</p>')
        if rid == '16.10':
            out.append(a21_block())
        video = rid in ('16.10', '16.11')
        out.append(f'<div class="rule"><p class="rid">Rule {rid}</p><p class="rt">{e(words[rid]["title"])}</p>')
        if video and not CH16_VIDEO_FINAL:
            out.append(slot(f'Rule {rid}’s plates after A21, the application kit’s video frame with chart S04 drawn '
                            'in it, which Engineer W builds and the design director places in this chat’s second pass '
                            '(CD-S7). Until it lands, the plates hold labeled empty frames, the reason C16-V scored 3 on '
                            'craft.'))
            out.append('</div>')
            continue
        row = []
        for kind in ('correct', 'failure'):
            key = f'ch16-1440-s-16-{rid.split(".")[1]}-{kind}'
            p = caps / f'{key}.png'
            if not p.exists():
                continue
            fn, pw, ph = save_webp(p, f'Chapter-16-Rule-{rid.replace(".", "-")}-{kind.title()}')
            cap = labels('Correct' if kind == 'correct' else 'Failure', '1440 px')
            row.append(fig(fn, pw, ph, cap_alt_ch16(f's-16-{rid.split(".")[1]}-{kind}', words), cap, link=fn))
        out.append(f'<div class="cmp">{"".join(row)}</div></div>')
        if rid == '16.9':
            p = caps / 'ch16-1440-s-16-picture-kinds.png'
            if p.exists():
                fn, pw, ph = save_webp(p, 'Chapter-16-Picture-Kinds')
                out.append(fig(fn, pw, ph, cap_alt_ch16('s-16-picture-kinds', words), labels('After Rule 16.9', '1440 px'), link=fn))
    out.append('<h3>At a phone’s width</h3><p>Two plates at 390 px, as a phone shows them: a photograph rule and a placeholder.</p>')
    row = []
    for sid, name, alt in [('s-16-1-correct', 'Chapter-16-Rule-16-1-Correct-390', 'Rule 16.1’s correct plate at 390 px, its photograph and caption in one column.'),
                           ('s-16-8-correct', 'Chapter-16-Rule-16-8-Correct-390', 'Rule 16.8’s correct plate at 390 px: frames that say Placeholder, each with its ratio and label.')]:
        p = caps / f'ch16-390-{sid}.png'
        if p.exists():
            fn, pw, ph = save_webp(p, name)
            row.append(fig(fn, pw, ph, alt, labels(f'Rule {sid[2:4]}.{sid.split("-")[2]}', '390 px'), link=fn))
    out.append(f'<div class="cmp">{"".join(row)}</div>')
    out.append('</section>')
    return ''.join(out)


def a21_block():
    have = [a for a in A21 if (EXP / f'{a[0]}.png').exists()]
    if not have:
        return slot('A21, the application kit’s video frame with chart S04 drawn in it (CD-S7), as Engineer W exports it.')
    head = ('<h4>A21, chart S04 in the video frames</h4><p>The application kit’s new video frame draws chart S04 from the chart '
            'kit at video size, with the caption band over the caption-safe area and S04’s source line on screen (CD-S7). '
            'Each frame is shown at a third of its size; open it for true size.</p>')
    if not A21_FINAL:
        head += ('<p class="note"><span class="label">In progress</span>These are the frames as Engineer W exported them at '
                 '00:40 UTC. The editor’s words, the design director’s placement in Rules 16.10 and 16.11, the data lead’s '
                 'sign-off and the creative director’s rescore follow, and the board is built again from the final '
                 'frames.</p>')
    risk = [r for r in CD12B.get('risks_for_dustin', []) if 'vertical frame' in r]
    if risk:
        head += ('<p class="note"><span class="label">For chapter 23</span>The creative director names one cost to settle '
                 'at chapter 23: in the vertical frame S04’s words draw at about 9 px on a 390 px phone, since its '
                 'full source line stays on screen. Only a shorter on-screen source line frees that room, against Rule '
                 '13.6’s six parts.</p>')
    figs = []
    for stem, label, cw, alt in have:
        fn, pw, ph = save_webp(EXP / f'{stem}.png', stem.split('_', 1)[1])
        figs.append(fig(fn, cw, round(ph * cw / pw), alt, labels('A21', label), link=fn))
    return head + '<div class="cmp">' + ''.join(figs) + '</div>'


def opener(caps, n_, title):
    row = []
    for w in (1440, 390):
        p = caps / f'opener-{n_}-{w}.png'
        if p.exists():
            fn, pw, ph = save_webp(p, f'Chapter-{n_}-Opening-{w}')
            fig_words = {'20': 'the website’s home page in its frames', '21': 'the atlas home’s first screens as they load with nothing pressed, at 1440 px light and 390 px dark, then the rules by group'}.get(n_, 'its opening figure')
            row.append(fig(fn, pw, ph, f'Chapter {n_}’s opening as the guide prints it at {w} px: its title, its introduction and {fig_words}.',
                           labels(f'Chapter {n_}’s opening', f'{w} px'), link=fn))
    return f'<div class="cmp">{"".join(row)}</div>' if row else ''


def sec_web(rep):
    out = ['<section aria-labelledby="h-web" id="web"><h2 id="h-web">Chapter 20, your website</h2>',
           '<p>The website chapter 20 teaches, drawn by the application kit and exported at true size: the home page, an '
           'article and an Act page at 1440, 1024, 390 and 360 px on Newsprint, and at 1440 and 390 px in the dark theme. '
           'Each picture is the page’s first screen, the height of one window at that width; open it to see the whole '
           'page.</p>']
    built = rep['weight']['projection']['phase_4_built']['20']
    out.append(f'<p class="note">Chapter 20 carries {n(built["bytes"])} bytes against an allocation of {n(built["allocation"])}.</p>')
    out.append('<h3>Chapter 20 in the guide</h3><p>The chapter’s opening as the guide prints it, at 1440 and 390 px; the '
               'guide itself stays on Newsprint (D2-1133), and its plates show the dark theme in their frames.</p>'
               + opener(CAPS, '20', 'Web'))
    for key, stem, label in WEB_PAGES:
        out.append(f'<h3>{e(label)}</h3>')
        figs = {}
        for w, t in WEB_VIEWS:
            src = EXP / f'{stem}-{w}-{t}.png'
            im = Image.open(src)
            if im.width != w:
                sys.exit(f'{src.name}: {im.width} px wide, expected {w}')
            full, fw, fh = save_webp(src, f'{stem.split("_", 1)[1]}-{w}-{t}')
            first, pw, ph = save_webp(src, f'{stem.split("_", 1)[1]}-{w}-{t}-First-Screen', crop=(0, 0, w, min(VH[w], im.height)))
            cap = (labels(label, f'{w} px', t) + f'First screen, {n(pw)} by {n(ph)} px. '
                   f'<a href="img/{full}" target="_blank" rel="noopener">The whole page, {n(fw)} by {n(fh)} px</a>.')
            figs[(w, t)] = fig(first, pw, ph, WEB_ALT[key][(w, t)], cap)
        out.append(f'<div class="wide">{figs[(1440, "Light")]}</div>')
        out.append(f'<div class="pair">{figs[(1024, "Light")]}{figs[(1440, "Dark")]}</div>')
        out.append(f'<div class="phones">{figs[(390, "Light")]}{figs[(360, "Light")]}{figs[(390, "Dark")]}</div>')
    out.append('<h3>The menu and the share preview</h3><div class="phones">')
    for stem, label, alt in WEB_STILLS:
        fn, pw, ph = save_webp(EXP / f'{stem}.png', stem.split('_', 1)[1])
        cw = pw if pw <= 400 else pw // 2
        out.append(fig(fn, cw, round(ph * cw / pw), alt, labels(label) + ('' if cw == pw else 'Shown at half size; open it for true size.'), link=fn))
    out.append('</div></section>')
    return ''.join(out)


def sec_atlas(rep, atest, ch, wall):
    built = rep['weight']['projection']['phase_4_built']['21']
    out = ['<section aria-labelledby="h-atlas" id="atlas"><h2 id="h-atlas">Chapter 21, the atlas</h2>',
           '<p>The atlas’s views, drawn by the application kit from the atlas model and exported at true size: the home '
           'page, a reform’s page, the Register with a sheet open and a loop page, each at 1440 and 390 px in both themes, '
           'then How to read and the loop index. Each picture is the view’s first screen; open it for the whole page.</p>',
           f'<p class="note">Chapter 21 carries {n(built["bytes"])} bytes against an allocation of {n(built["allocation"])}, '
           f'{round(100 * built["bytes"] / built["allocation"])} percent. Its {len(ch["rules"])} rules sit in five groups.</p>']
    out.append('<h3>Chapter 21 in the guide</h3><p>The chapter’s opening as the guide prints it, at 1440 and 390 px: the '
               'atlas home’s first screens, 1440 px light and 390 px dark.</p>')
    if not OPENERS_FINAL:
        out.append('<p class="note"><span class="label">Before CD-R1</span>Captured from the page as it stood before '
                   'Engineer A’s fixes; CD-R1 draws these frames with nothing pressed, and the board is built again from '
                   'the final page.</p>')
    out.append(opener(CAPS, '21', 'The atlas'))
    for key, stem, label, views in ATLAS_VIEWS:
        out.append(f'<h3>{e(label)}</h3>')
        figs = []
        for w, t in views:
            src = EXP / f'{stem}-{w}-{t}.png'
            im = Image.open(src)
            full, fw, fh = save_webp(src, f'{stem.split("_", 1)[1]}-{w}-{t}')
            first, pw, ph = save_webp(src, f'{stem.split("_", 1)[1]}-{w}-{t}-First-Screen', crop=(0, 0, w, min(VH[w], im.height)))
            theme = 'on Newsprint' if t == 'Light' else 'in the dark theme, on Charcoal'
            alt = f'At {w} px {theme}: ' + ATLAS_ALT[key]['wide' if w > 600 else 'phone']
            cap = (labels(label, f'{w} px', t) + f'First screen. <a href="img/{full}" target="_blank" rel="noopener">'
                   f'The whole page, {n(fw)} by {n(fh)} px</a>.')
            figs.append((w, fig(first, pw, ph, alt, cap)))
        wide = [f for w, f in figs if w > 600]
        phone = [f for w, f in figs if w <= 600]
        out.append(f'<div class="pair">{"".join(wide)}</div><div class="phones">{"".join(phone)}</div>')
    out.append(sec_atlas_test(atest))
    out.append(sec_wall(wall))
    out.append('</section>')
    return ''.join(out)


def sec_atlas_test(atest):
    names, counts = {}, {}
    for line in atest['lines']:
        m = re.match(r'(PASS|FAIL) (T\d+) (\S+) (.*?): ([^,]+),', line)
        if not m:
            continue
        st, t, _, _, name = m.groups()
        names[t] = name
        c = counts.setdefault(t, [0, 0])
        c[0 if st == 'PASS' else 1] += 1
    tp = sum(c[0] for c in counts.values())
    tf = sum(c[1] for c in counts.values())
    rows = ''.join(f'<tr><th scope="row">{t}</th><td>{e(names[t][0].upper() + names[t][1:])}</td><td class="num">{n(c[0])}</td>'
                   f'<td class="num">{n(c[1])}</td></tr>' for t, c in sorted(counts.items(), key=lambda kv: int(kv[0][1:])))
    return ('<h3 id="atlas-test">The atlas test</h3>'
            f'<p>The atlas test reads every view the kit draws against the atlas model before it ships (Rule 21.16). Its '
            f'last run, {e(atest["ran"][:16].replace("T", " at "))} UTC on views {e(", ".join(atest["ids"]))}, read '
            f'{n(tp)} checks as passing and {n(tf)} as failing, and its self-test, which plants faults to prove it catches '
            f'them, reads {e(atest["self_test"])}. The test runs again on this chat’s rebuilt views.</p>'
            '<table class="narrow"><thead><tr><th scope="col">Test</th><th scope="col">What it reads</th><th scope="col" class="num">Pass</th>'
            f'<th scope="col" class="num">Fail</th></tr></thead><tbody>{rows}</tbody></table>')


def sec_wall(wall):
    head = ('<h3 id="wall">The wall test, as evidence</h3>'
            '<p>This asks you nothing. With the wordmark, the lockmark and the atlas’s own name covered by patches of the '
            'ground they sit on, the creative director judged whether each of the atlas’s four views still reads as Oath '
            '& Action among public civic data pages. All four pass, the atlas home narrowly, and they passed again on the '
            'rebuilt views (DR-315). The colored layer rule closes (ED-F1), and Rule 15.25’s resolution, a part named by a '
            'frame and a name, stands.</p>')
    if not wall or not Path(wall).exists():
        return head + slot('The covered pictures, which the creative director makes again for this board: the four views '
                           'at 1440 px light and dark and at 390 px light, covered as in reading B, beside chapter 20’s '
                           'home page covered.')
    wall = Path(wall)
    what = {
        'Atlas-Home': ('The atlas home', 'the drawing of the whole system, Outside forces over Wealth, Voice, Elections, Checks and Policy, with Your household and Technology beneath, under the Charcoal title band'),
        'Atlas-Reform-R-23': ('Reform R-23', 'the chip Reform R-23, the title Minimum wage that rises with an index in display type, and the Charcoal Where it stands panel with its two grades'),
        'Atlas-Register-D04': ('The Register, sheet D04', 'the title The Register on its Charcoal band and the index of sheets, each grade column headed by its line sample'),
        'Atlas-Loop-R18': ('Loop R18', 'the quoted title on Weakening watchdogs in display type, the grade line with its chips and the Charcoal This loop panel'),
        'Chapter-20-Web-Home-Control': ('Chapter 20’s home page, the control', 'the Charcoal pillar row, Explain, Track, Connect and Act, over the four pieces with the red dot on the NAC rule’s step'),
    }
    out = [head, '<p>Reading B covers the masthead’s wordmark and lockmark, the footer’s lockmark, the atlas’s own name and '
           'subtitle in its title bar, and the footer’s column head “Oath & Action”. Each picture is the view’s first '
           'screen, covered; open it for the whole page covered. The creative director’s method and every patch are in '
           '<code>20261124_Chat-12b-CD-Rescore.md</code>.</p>']
    for key, (label, desc) in what.items():
        figs = []
        for w, t in ((1440, 'Light'), (1440, 'Dark'), (390, 'Light')):
            whole = wall / f'{key}-{w}-{t}-Reading-B.png'
            first = wall / 'first-screens' / f'{key}-{w}-{t}-Reading-B-First-Screen.png'
            if not first.exists():
                continue
            ffn, pw, ph = save_webp(first, f'Wall-Test-{key}-{w}-{t}-First-Screen')
            link = save_webp(whole, f'Wall-Test-{key}-{w}-{t}')[0] if whole.exists() else ffn
            theme = 'on Newsprint' if t == 'Light' else 'in the dark theme'
            alt = (f'{label}, first screen at {w} px {theme}, covered for the wall test: the wordmark, the lockmark and the '
                   f'atlas’s name replaced by flat patches of the ground, leaving {desc}.')
            cw = pw if w == 390 else 720
            figs.append(fig(ffn, cw, round(ph * cw / pw), alt, labels('Covered', f'{w} px', t) + ('Shown at half size.' if cw < pw else 'True size.'), link=link))
        if figs:
            out.append(f'<h4>{e(label)}</h4><div class="cmp">{"".join(figs)}</div>')
    return ''.join(out)


def sec_specs(specs):
    by = {}
    for r in specs['rows']:
        by.setdefault(r['channel'], []).append(r)
    order = ['website', 'substack', 'email', 'x', 'threads', 'instagram', 'youtube', 'tiktok', 'linkedin', 'video', 'print', 'slides']
    names = {'website': 'Website', 'substack': 'Substack', 'email': 'Email', 'x': 'X', 'threads': 'Threads', 'instagram': 'Instagram',
             'youtube': 'YouTube', 'tiktok': 'TikTok', 'linkedin': 'LinkedIn', 'video': 'Video frames', 'print': 'Print', 'slides': 'Slides'}
    status = {'read': 'Read on the official page', 'search-result': 'From a search result', 'not-found': 'Not found; the studio’s choice'}
    blocks = []
    for ch in order:
        rows = by.get(ch, [])
        if not rows:
            continue
        trs = []
        for r in rows:
            size = ' by '.join(str(x) for x in (r['width'], r['height']) if x is not None)
            size = f'{size} {r["unit"]}' if size else 'Any size'
            src = (r.get('source') or '').split(' ; ')[0].strip()
            link = f'<a href="{e(src)}" rel="noopener" target="_blank">Source</a>' if src.startswith('http') else ''
            app = re.sub(r'`([^`]+)`', r'<code>\1</code>', e(r['application'].replace(chr(39), '’')))   # typographic apostrophes
            trs.append(f'<tr><th scope="row">{app}</th><td data-k="Size">{e(size)}</td><td data-k="Aspect">{e(r["aspect"] or "")}</td>'
                       f'<td data-k="Fits">{e(r["match"])}</td><td data-k="Safe area">{"Yes" if r["safe_area"] else "No"}</td>'
                       f'<td data-k="Status">{e(status.get(r["status"], r["status"]))}</td><td data-k="Page">{link}</td></tr>')
        blocks.append(f'<details class="spec"><summary><span>{e(names[ch])}</span><span class="count">{num(len(rows)).capitalize()} '
                      f'{"row" if len(rows) == 1 else "rows"}</span></summary><table class="stack"><thead><tr><th scope="col">Application</th>'
                      '<th scope="col">Size</th><th scope="col">Aspect</th><th scope="col">Fits</th><th scope="col">Safe area</th>'
                      f'<th scope="col">Status</th><th scope="col">Page</th></tr></thead><tbody>{"".join(trs)}</tbody></table></details>')
    from collections import Counter
    c = Counter(r['status'] for r in specs['rows'])
    return ('<section aria-labelledby="h-specs" id="specs"><h2 id="h-specs">The platform specifications</h2>'
            f'<p>The research lead read each channel’s official help pages on November 21, 2026 and wrote one row per '
            f'application: {n(len(specs["rows"]))} rows, {c["read"]} read on the platform’s own page, {c["search-result"]} '
            f'from a search result, and {c["not-found"]} where no page states a figure and the studio chose one. The '
            'dimension script checks every export against these rows. “Fits” says how: exact, at least this size, at most '
            'this size, or any size at the ratio. Each row’s note is in '
            '<code>work/research/20261121_Platform-Specifications.json</code>.</p>' + ''.join(blocks) + '</section>')


def sec_rescore(scores):
    rs = scores['rescore']['items']
    crit = ['craft', 'clarity', 'brand_fidelity', 'usefulness', 'evidence_honesty', 'accessibility']
    heads = ['Craft', 'Clarity', 'Brand', 'Useful', 'Evidence', 'Access']
    rows = []
    for item, v in rs.items():
        sc = v['scores']
        note = ''
        if item == 'C16-V':
            if C16V_RESCORE:
                sc = C16V_RESCORE['scores']
                v = dict(v, ready=C16V_RESCORE['ready'])
                note = f' <span class="label">Rescored in chat 12b</span>'
            else:
                note = ' <span class="label">Rescore to come</span>'
        cells = ''.join(f'<td class="num{" low" if sc[c] < 4 else ""}" data-k="{h}">{sc[c]}</td>' for c, h in zip(crit, heads))
        rows.append(f'<tr><th scope="row">{e(item)}{note}</th>{cells}<td data-k="Ready">{"Yes" if v["ready"] else "Not yet"}</td></tr>')
    th = ''.join(f'<th scope="col" class="num">{h}</th>' for h in heads)
    closed = [c for c, v in CD12B.get('chat_12_second_pass_codes', {}).items() if v.get('closed')]
    closed_p = (f'<p>The creative director also saw {e(", ".join(closed[:-1]))} and {e(closed[-1])} closed on the rebuilt '
                'frames, and the wall test pass again.</p>') if len(closed) > 1 else ''
    ready = sum(1 for item, v in rs.items() if (C16V_RESCORE['ready'] if item == 'C16-V' and C16V_RESCORE else v['ready']))
    tail = (f'<p><strong>{ready} of {len(rs)} items are ready.</strong> {e(C16V_RESCORE["note"].replace(chr(39), "’"))}</p>{closed_p}' if C16V_RESCORE else slot(
        'The creative director’s rescore of C16-V alone, once A21 is placed and the data lead signs it off (DR-191), with '
        'whether the five small faults, CD-R1 to CD-R5, and CD-S6 are closed.'))
    return ('<section aria-labelledby="h-rescore" id="rescore"><h2 id="h-rescore">The creative director’s rescore</h2>'
            '<p>Each item scored from 1 to 5 on six criteria after chat 12’s fix pass, and C16-V again after this chat’s '
            'second pass; an item ships at 4 or more on all six. '
            'C stands for chapter, then the chapter’s number and its group: C16-A covers Rules 16.1 to 16.4, C20-P the '
            'website’s three pages, C21-L the loop pages, and AK the application kit. Scores under 4 are marked.</p>'
            f'<div class="tablewrap"><table class="scores"><thead><tr><th scope="col">Item</th>{th}<th scope="col">Ready</th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table></div>{tail}</section>')


def sec_tested(meta, caps, rep):
    w = rep['weight']
    return ('<section aria-labelledby="h-tested" id="tested"><h2 id="h-tested">What the studio checked for this board</h2>'
            '<div class="twocol"><div><h3>Tested</h3><ul class="plain">'
            f'<li>The final page, from the main session’s strict build: {len(rep["warnings"])} warnings in its report, {n(w["bytes"])} '
            f'bytes, {rep["rules"] if isinstance(rep["rules"], int) else len(rep["rules"])} rules and '
            f'{rep["specimens_placed"] if isinstance(rep["specimens_placed"], int) else len(rep["specimens_placed"])} specimens. '
            'Every guide picture on this board comes from it.</li>'
            '<li>Commit bc91667e’s page was built in scratch from <code>git archive</code>, with no checkout. It weighs '
            '14,189,507 bytes, the page of record at chat 12’s opening, and gives PR-M1’s before.</li>'
            '<li>Every original here was captured from those pages in Chromium with reduced motion, and every proposal is a '
            'studio sketch drawn in the browser’s copy of the page. No chapter file changed.</li>'
            '<li>For C11C-R14d, a script compared today’s and the proposal’s Newsprint pictures pixel by pixel.</li>'
            '<li>The board itself was opened at 1440, 1024, 390 and 360 px, light and dark: no sideways scroll, no broken '
            'picture, and axe found no violation at 1440, 390 and 360 px. The script that writes it stops on an em or en '
            'dash, chapter 02’s filler and corporate words, a picture without alt text, and a picture it does not '
            'use.</li>'
            f'<li>{GUIDE_CHECK["selftest"]}</li>'
            f'<li>{GUIDE_CHECK["four_widths"]}</li></ul></div>'
            '<div><h3>Not tested</h3><ul class="plain">'
            '<li>Real screen readers, Safari and Firefox were not tried (DR-279).</li>'
            '<li>Each proposal is a sketch, so its code, its contrast in every place it appears and its effect on the guide '
            'check are tested when the change is made.</li>'
            f'<li>{GUIDE_CHECK["not_tested"]}</li>'
            '<li>The board ran no weight measure of its own. Its weight table is copied from Engineer M’s notes.</li></ul></div></div></section>')


# ================================================================ page

CSS = r'''
:root {
  --ground: {newsprint};   /* oa.color.palette.newsprint */
  --ink: {charcoal};       /* oa.color.palette.charcoal */
  --quiet: {deep_stone};   /* oa.color.derived.deep-stone */
  --rule: {stone};         /* oa.color.palette.stone */
  --red: {red};            /* oa.color.palette.pillar-red: the wordmark's ampersand only */
  --card: {tint_white};    /* oa.color.tint.white-n55 */
  --panel: {charcoal};
  --on-panel: {newsprint};
  --focus: {verdigris};    /* oa.color.palette.verdigris */
  --display: "Inter Tight", "Inter", system-ui, sans-serif;
  --text: "Inter", system-ui, -apple-system, "Segoe UI", sans-serif;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --ground: {charcoal}; --ink: {newsprint}; --quiet: {dim_newsprint}; --rule: {prussian_n56}; --card: #1E1F21;
  --panel: #1E1F21; --on-panel: {newsprint}; --focus: #7FB3A9; color-scheme: dark } }
:root[data-theme="dark"] {
  --ground: {charcoal}; --ink: {newsprint}; --quiet: {dim_newsprint}; --rule: {prussian_n56}; --card: #1E1F21;
  --panel: #1E1F21; --on-panel: {newsprint}; --focus: #7FB3A9; color-scheme: dark }
* { box-sizing: border-box }
html { -webkit-text-size-adjust: 100% }
body { margin: 0; background: var(--ground); color: var(--ink); font: 400 16px/1.55 var(--text); overflow-wrap: break-word }
.wrap { max-width: 1504px; margin: 0 auto; padding: 32px max(16px, env(safe-area-inset-right, 0px)) 80px max(16px, env(safe-area-inset-left, 0px)) }
.col { max-width: 46rem }
a { color: inherit; text-underline-offset: 3px }
a:focus-visible, summary:focus-visible { outline: 3px solid var(--focus); outline-offset: 3px }
.vh { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap }
.mast { display: flex; flex-wrap: wrap; align-items: baseline; justify-content: space-between; gap: 8px 24px; border-bottom: 1px solid var(--rule); padding-bottom: 12px }
.word { font: 800 22px/1 var(--display); letter-spacing: -0.01em }
.word .amp { color: var(--red) }
.kick { font: 700 13px/1.3 var(--text); letter-spacing: 0.06em; text-transform: uppercase; color: var(--quiet) }
h1 { font: 800 clamp(34px, 6vw, 60px)/1.03 var(--display); letter-spacing: -0.02em; margin: 32px 0 16px; text-wrap: balance; max-width: 22ch }
h2 { font: 800 clamp(26px, 3.6vw, 36px)/1.1 var(--display); letter-spacing: -0.015em; margin: 72px 0 12px; padding-top: 16px; border-top: 3px solid var(--ink); text-wrap: balance }
h3 { font: 800 clamp(20px, 2.2vw, 24px)/1.2 var(--display); letter-spacing: -0.01em; margin: 40px 0 8px; text-wrap: balance }
h4 { font: 700 13px/1.3 var(--text); letter-spacing: 0.06em; text-transform: uppercase; color: var(--quiet); margin: 24px 0 8px }
p { margin: 0 0 12px; max-width: 46rem }
.lede { font-size: 19px; line-height: 1.5 }
.note { font-size: 14px; color: var(--quiet) }
code { font: 400 0.9em/1.4 ui-monospace, "SF Mono", Menlo, Consolas, monospace; overflow-wrap: anywhere }
nav.toc ol { list-style: none; padding: 0; margin: 16px 0 0; display: flex; flex-wrap: wrap; gap: 8px 20px; font-size: 15px }
.decs { list-style: none; padding: 0; margin: 24px 0 0; display: grid; gap: 16px; max-width: 60rem }
.dec { display: grid; grid-template-columns: 44px minmax(0, 1fr); gap: 0 16px; background: var(--card); padding: 20px 20px 16px; border-left: 3px solid var(--ink) }
.dec-n { font: 800 32px/1 var(--display); font-variant-numeric: tabular-nums }
.dec h3 { margin: 0 0 4px; font-size: 21px }
.dec .code { font: 700 13px/1.4 var(--text); letter-spacing: 0.04em; text-transform: uppercase; color: var(--quiet); margin-bottom: 10px }
.dec .rec { padding-top: 10px; border-top: 1px solid color-mix(in srgb, var(--rule) 50%, transparent) }
.dec .seelink { margin: 0; font-size: 14px }
@media (max-width: 480px) { .dec { grid-template-columns: minmax(0, 1fr); padding: 16px } .dec-n { font-size: 24px; margin-bottom: 6px } }
.reply { background: var(--panel); color: var(--on-panel); padding: 24px; margin-top: 24px; max-width: 60rem }
.reply .reply-k { font: 700 13px/1.3 var(--text); letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 8px }
.reply .reply-t { font: 800 clamp(20px, 2.6vw, 26px)/1.25 var(--display); margin: 0 0 12px }
.reply .note { color: inherit; opacity: 0.85; margin: 0 0 8px }
.xitem { margin-top: 48px; padding-top: 8px; border-top: 1px solid var(--rule) }
figure { margin: 0; min-width: 0 }
.pic img { display: block; max-width: 100%; height: auto; border: 1px solid var(--rule); background: #DCD9D2 }
.pic img.px { image-rendering: pixelated }
.pic .imglink { display: block; width: fit-content; max-width: 100% }
figcaption { font-size: 14px; color: var(--quiet); margin-top: 8px; max-width: 46rem }
.label { display: inline-block; font: 700 12px/1 var(--text); letter-spacing: 0.06em; text-transform: uppercase; border: 1px solid currentColor; padding: 3px 6px; margin: 0 6px 4px 0; color: var(--ink) }
.cmp { display: flex; flex-wrap: wrap; gap: 24px 32px; align-items: flex-start; margin: 20px 0 8px }
.cmp > .pic { flex: 0 1 auto; max-width: 100% }
.wide { margin-top: 20px }
.wide .pic img, .pair .pic img { width: 100% }
.pair { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(320px, 100%), 1fr)); gap: 24px; margin-top: 24px; align-items: start }
.phones { display: flex; flex-wrap: wrap; gap: 24px; margin-top: 24px; align-items: flex-start }
.phones .pic { flex: 0 1 390px; max-width: 100% }
.rule { margin: 28px 0 0 }
.rule .rid { font: 700 13px/1.3 var(--text); letter-spacing: 0.06em; text-transform: uppercase; color: var(--quiet); margin: 0 }
.rule .rt { font: 800 20px/1.25 var(--display); margin: 2px 0 0 }
h3.grp { margin-top: 56px }
.slot { border: 2px dashed var(--rule); padding: 16px 20px; margin: 16px 0; max-width: 46rem }
.slot .slot-k { font: 700 13px/1.3 var(--text); letter-spacing: 0.06em; text-transform: uppercase; color: var(--quiet); margin-bottom: 6px }
.slot p:last-child { margin: 0 }
.facts { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(220px, 100%), 1fr)); gap: 16px; margin: 20px 0 }
.fact { border-top: 3px solid var(--ink); padding-top: 10px; min-width: 0 }
.fact b { display: block; font: 800 30px/1.05 var(--display); font-variant-numeric: tabular-nums }
.fact span { font-size: 14px; color: var(--quiet) }
.twocol { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(300px, 100%), 1fr)); gap: 8px 40px }
table { border-collapse: collapse; width: 100%; font-size: 15px; margin: 8px 0 16px }
table.narrow { max-width: 40rem }
th, td { text-align: left; padding: 8px 12px 8px 0; border-bottom: 1px solid color-mix(in srgb, var(--rule) 45%, transparent); vertical-align: top }
thead th { font: 700 12px/1.3 var(--text); letter-spacing: 0.06em; text-transform: uppercase; color: var(--quiet); border-bottom: 1px solid var(--rule) }
td.num, th.num { font-variant-numeric: tabular-nums; text-align: right; white-space: nowrap }
td.low { font-weight: 800 }
tbody th { font-weight: 600 }
.scores td.num { min-width: 2.5em }
details.spec { border-top: 1px solid var(--rule); max-width: 72rem }
details.spec:last-of-type { border-bottom: 1px solid var(--rule) }
details.spec summary { cursor: pointer; display: flex; flex-wrap: wrap; justify-content: space-between; gap: 4px 16px; padding: 12px 0; font-weight: 700 }
details.spec summary .count { font-weight: 400; color: var(--quiet); font-size: 14px }
@media (max-width: 760px) {
  table.stack, table.stack tbody, table.stack tr, table.stack th, table.stack td { display: block; width: 100% }
  table.stack thead { display: none }
  table.stack tr { padding: 10px 0; border-bottom: 1px solid var(--rule) }
  table.stack th, table.stack td { border: 0; padding: 2px 0 }
  table.stack td[data-k]::before { content: attr(data-k) ": "; font-weight: 700 }
  table.stack td:empty { display: none }
  table.scores thead { display: none }
  table.scores, table.scores tbody { display: block }
  table.scores tr { display: grid; grid-template-columns: repeat(auto-fill, minmax(96px, 1fr)); gap: 2px 12px; padding: 10px 0; border-bottom: 1px solid var(--rule) }
  table.scores th { grid-column: 1 / -1; border: 0; padding: 0 0 4px }
  table.scores td { border: 0; padding: 0; text-align: left; font-size: 14px }
  table.scores td[data-k]::before { content: attr(data-k) " "; color: var(--quiet); font-weight: 400 }
}
@media (max-width: 480px) { table { font-size: 14px } th, td { padding-right: 8px } }
.tablewrap { max-width: 100% }
ul.plain { padding-left: 20px; margin: 0 0 12px } ul.plain li { margin-bottom: 6px; max-width: 44rem }
.foot { margin-top: 72px; padding-top: 16px; border-top: 1px solid var(--rule); font-size: 14px; color: var(--quiet) }
'''


def tokens():
    css = (ROOT / 'work/build/tokens/tokens.css').read_text()

    def tok(name):
        m = re.search(r'--' + re.escape(name) + r':\s*(#[0-9A-Fa-f]{6})', css)
        if not m:
            sys.exit(f'token --{name} not found in tokens.css')
        return m.group(1)
    return {
        'newsprint': tok('oa-color-palette-newsprint'), 'charcoal': tok('oa-color-palette-charcoal'),
        'red': tok('oa-color-palette-pillar-red'), 'stone': tok('oa-color-palette-stone'),
        'verdigris': tok('oa-color-palette-verdigris'), 'deep_stone': tok('oa-color-derived-deep-stone'),
        'dim_newsprint': tok('oa-color-derived-dim-newsprint'), 'prussian_n56': tok('oa-color-tint-prussian-n56'),
        'tint_white': tok('oa-color-tint-white-n55'),
    }


def page(body, rep):
    css = CSS
    for k, v in tokens().items():
        css = css.replace('{' + k + '}', v)
    w = rep['weight']
    return ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<title>Phase 4 Board 1</title>\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Inter+Tight:wght@700;800&display=swap">\n'
            f'<style>{css}</style>\n</head>\n<body>\n<div class="wrap">'
            '<header class="mast"><span class="word" role="img" aria-label="Oath &amp; Action">OATH<span class="amp">&amp;</span>ACTION</span>'
            '<span class="kick">Edition 06, Phase 4 board 1, November 24, 2026</span></header><main>'
            '<p class="kick" style="margin-top:32px">For Dustin Cathcart, Founder and Editor</p>'
            '<h1>Phase 4 board 1: chapters 16, 20 and 21, and the changes they ask of approved work</h1>'
            '<p class="lede">Chats 10 to 12b built and reviewed three chapters: photography, illustration and video; your '
            'website; and the atlas inside it. This board shows them as built and asks you to decide 12 items, ranked, '
            'each with the studio’s recommendation. One reply at the end of the list takes every recommendation.</p>'
            '<nav class="toc" aria-label="On this board"><ol>'
            '<li><a href="#h-decide">What you decide</a></li><li><a href="#h-approved">Changes to approved work</a></li>'
            '<li><a href="#ch16">Chapter 16</a></li><li><a href="#web">Chapter 20, the website</a></li>'
            '<li><a href="#atlas">Chapter 21, the atlas</a></li><li><a href="#specs">Specifications</a></li>'
            '<li><a href="#rescore">The rescore</a></li><li><a href="#tested">Checked</a></li></ol></nav>'
            + body +
            f'</main><footer class="foot"><p>Built by <code>work/build/scripts/phase-4/board1_build.py</code> from the exports, '
            f'today’s strict build ({n(w["bytes"])} bytes) and the studio’s notes. Board builder’s notes: '
            '<code>work/handoffs/phase-4/20261124_Chat-12b-Board-Builder-Notes.md</code>.</p></footer></div>\n</body>\n</html>\n')


# ================================================================ checks on the written page

BANNED = (r'\b(genuinely|really|truly|actually|simply|just|leverage[sd]?|underscores?|reflects?|very|extremely|'
          r'incredibly|seamless(ly)?|robust|delve)\b')


def check(page_html):
    if re.search(r'\{\{|\{[a-z_]+\}', re.sub(r'<style.*?</style>', '', page_html, flags=re.S)):
        sys.exit('an unfilled placeholder is on the page')
    if '—' in page_html or '–' in page_html:
        sys.exit('an em or en dash is on the page')
    text = re.sub(r'<style.*?</style>', ' ', page_html, flags=re.S)
    text = re.sub(r'<code>.*?</code>', ' ', text, flags=re.S)
    text = html.unescape(re.sub(r'<[^>]+>', ' ', text))
    bad = re.findall(BANNED, text, re.I)
    if bad:
        sys.exit(f'filler or corporate words on the page: {sorted(set(b[0] if isinstance(b, tuple) else b for b in bad))}')
    for m in re.finditer(r'<img\b[^>]*>', page_html):
        if not re.search(r'\balt="[^"]{12,}"', m.group(0)):
            sys.exit(f'an image without real alt text: {m.group(0)[:160]}')
    refs = set(re.findall(r'(?:src|href)="img/([^"]+)"', page_html))
    files = {p.name for p in IMG.iterdir()}
    missing, unused = refs - files, files - refs
    if missing:
        sys.exit(f'pictures referenced but not written: {sorted(missing)[:5]}')
    for f in unused:
        (IMG / f).unlink()
    straight = re.findall(r"[A-Za-z]'[A-Za-z]", text)
    if straight:
        sys.exit(f'a straight apostrophe in the text: {straight[:5]}')


# ================================================================ capture

def capture(args):
    words = subprocess.run(['bash', str(GATE)], capture_output=True, text=True).stdout.strip()
    print('browsers.sh:', words)
    if 'OK to open one' not in words:
        sys.exit('the browser gate says wait; run again later')
    caps = Path(args.caps)
    caps.mkdir(parents=True, exist_ok=True)
    js = caps / 'board1_capture.js'
    js.write_text(CAPTURE_JS)
    cfg = dict(CAPTURE_CFG, out=str(caps), now=args.now, before=args.before or '',
               loopPage=str(EXP / '20261122_Atlas-Loop-R18-Page.html'))
    if args.only:
        cfg['only'] = args.only.split(',')
    cf = caps / 'board1_capture.json'
    cf.write_text(json.dumps(cfg, indent=1))
    env = dict(os.environ, TMPDIR=str(caps.parent / 'tmp'))
    (caps.parent / 'tmp').mkdir(exist_ok=True)
    r = subprocess.run(['node', str(js), str(cf)], cwd=ROOT / 'work/build', env=env)
    sys.exit(r.returncode)


# What the capture script reads besides the pages: the plates of C11C-R14d, the rule texts and their studio sketches
# (each an element finder and an edit made in the browser's copy), C11-1's plate and its crop height.
CAPTURE_CFG = {
 "r14d": [
  "s-15-12-correct",
  "s-15-11-correct"
 ],
 "texts": [
  {
   "name": "0116-length",
   "js": "const r=document.querySelector('#rule-01-16'); const row=[...r.querySelectorAll('.spec-row')].find(x=>x.querySelector('dt').textContent.trim()==='Length'); return [...row.children];",
   "edit": "const r=document.querySelector('#rule-01-16'); const d=[...r.querySelectorAll('.spec-row')].find(x=>x.querySelector('dt').textContent.trim()==='Length').querySelector('dd'); d.innerHTML=d.innerHTML+'<ins style=\"font-weight:700;text-decoration:none\">. Readings quoted from a record print at the length the record holds (DR-37, DR-93); readings we write run the same length</ins>';"
  },
  {
   "name": "132-contested",
   "js": "const r=document.querySelector('#rule-13-2'); const row=[...r.querySelectorAll('.spec-row')].find(x=>x.querySelector('dt').textContent.trim()==='Contested'); return [...row.children];",
   "edit": "const r=document.querySelector('#rule-13-2'); const d=[...r.querySelectorAll('.spec-row')].find(x=>x.querySelector('dt').textContent.trim()==='Contested').querySelector('dd'); d.innerHTML='Both readings at the same length<ins style=\"font-weight:700;text-decoration:none\">, or at the length the record holds for readings quoted from it</ins> (Rule 01.16)';"
  },
  {
   "name": "1516-text",
   "js": "return [document.querySelector('#rule-15-16 .rule-h'), ...document.querySelectorAll('#rule-15-16 .rule-body > .rule-text')];",
   "edit": "const p=document.querySelector('#rule-15-16 .rule-body > .rule-text'); p.innerHTML=p.innerHTML.replace('and print no row that adds them.', 'and print no row that adds them. <ins style=\"font-weight:700;text-decoration:none\">Print the atlas’s confidence in these effects, quoted as stored, once under the four rows.</ins>');"
  },
  {
   "name": "134-text",
   "js": "return [document.querySelector('#rule-13-4 .rule-h'), ...document.querySelectorAll('#rule-13-4 .rule-body > .rule-text')];",
   "edit": "const p=document.querySelector('#rule-13-4 .rule-body > .rule-text'); p.innerHTML=p.innerHTML+' <ins style=\"font-weight:700;text-decoration:none\">A dashed line carries a grade only on a connection; a dashed edge on a box or a button keeps the meaning chapters 17 and 18 give it.</ins>';"
  },
  {
   "name": "s66-source",
   "js": "return [document.querySelector('[data-specimen=\"s-14-s66\"] .oac-source')];",
   "edit": "const p=document.querySelector('[data-specimen=\"s-14-s66\"] .oac-source'); p.innerHTML=p.innerHTML.replace('Steps as the law sets them, not how long agencies take.', 'Steps as the law sets them<ins style=\"font-weight:700;text-decoration:none\">; how long an agency takes is its own practice</ins>.');"
  }
 ],
 "prussian": [
  "A19 1440-dark-stepper",
  "A19 390-light-stepper"
 ],
 "c111": "s-20-7-correct",
 "c111h": 1100
}

# The browser script, written into the captures folder and run with node from work/build.
CAPTURE_JS = r'''// Phase 4 board 1: the browser captures. Written by board1_build.py --capture and run from work/build (axe-core and
// playwright resolve there). Reads a JSON of inputs (argv[2]); writes PNGs and caps.json into its out folder.
// Every proposal picture here is a studio sketch: the change is made in the browser's copy of the page, never in a file.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const cfg = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const OUT = cfg.out;
const ONLY = cfg.only ? new Set(cfg.only) : null;
fs.mkdirSync(OUT, { recursive: true });
const meta = fs.existsSync(path.join(OUT, 'caps.json')) ? JSON.parse(fs.readFileSync(path.join(OUT, 'caps.json'), 'utf8')) : {};
const save = () => fs.writeFileSync(path.join(OUT, 'caps.json'), JSON.stringify(meta, null, 1));
const want = (k) => !ONLY || ONLY.has(k);

// The shell's sticky parts sit over a plate when a capture scrolls to it; set them in the flow while capturing.
const CALM = '.masthead,nav.rail,.chapter>.local-toc,.route-head,.rail-more{position:static!important}.skip{display:none!important}'
  + '*{animation:none!important;transition:none!important;caret-color:transparent!important}';

async function open(browser, file, width, height, dpr) {
  const ctx = await browser.newContext({ viewport: { width, height }, deviceScaleFactor: dpr, reducedMotion: 'reduce', colorScheme: 'light' });
  const page = await ctx.newPage();
  await page.goto('file://' + file, { waitUntil: 'load', timeout: 180000 });
  await page.addStyleTag({ content: CALM });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(400);
  return { ctx, page };
}

// A capture by boxes: js returns the elements whose union is the picture. The viewport grows to hold a tall box,
// the page scrolls the box into view, and the clip is taken from the viewport (no full-page capture of a 14 MB page).
async function shotBox(page, js, name, pad, extra) {
  pad = pad || 0;
  const vp = page.viewportSize();
  let box = await unionBox(page, js);
  if (!box) { meta[name] = { missing: true }; save(); return null; }
  let grown = false;
  if (box.height + 2 * pad > vp.height) {
    await page.setViewportSize({ width: vp.width, height: Math.min(Math.ceil(box.height + 2 * pad), 14000) });
    grown = true; await page.waitForTimeout(300);
    box = await unionBox(page, js);
  }
  const x0 = Math.max(0, Math.floor(box.x - pad)), y0 = Math.max(0, Math.floor(box.y - pad));
  const sy = await page.evaluate((y) => { window.scrollTo(0, y); return window.scrollY; }, y0);
  await page.waitForTimeout(200);
  const sx = await page.evaluate(() => window.scrollX);
  const cur = page.viewportSize();
  const clip = { x: x0 - sx, y: y0 - sy, width: Math.min(Math.ceil(box.width + 2 * pad), cur.width - (x0 - sx)), height: Math.min(Math.ceil(box.height + 2 * pad), cur.height - (y0 - sy)) };
  await page.screenshot({ path: path.join(OUT, name + '.png'), clip, animations: 'disabled' });
  meta[name] = Object.assign({ w: Math.round(clip.width), h: Math.round(clip.height) }, extra || {});
  save();
  if (grown) { await page.setViewportSize(vp); await page.waitForTimeout(200); }
  return box;
}
async function shotEl(page, sel, name, extra) {
  return shotBox(page, `return [document.querySelector(${JSON.stringify(sel)})];`, name, 0, Object.assign({ sel }, extra || {}));
}
async function shotClip(page, rect, name, pad, extra) {
  return shotBox(page, `return [{getBoundingClientRect(){return new DOMRect(${rect.x}-scrollX, ${rect.y}-scrollY, ${rect.width}, ${rect.height});}}];`, name, pad, extra);
}

// page-coordinate box of the union of elements
async function unionBox(page, js) {
  return page.evaluate((js) => {
    const els = (new Function(js))();
    let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
    els.forEach((e) => { const r = e.getBoundingClientRect(); if (!r.width && !r.height) return;
      x0 = Math.min(x0, r.left + scrollX); y0 = Math.min(y0, r.top + scrollY); x1 = Math.max(x1, r.right + scrollX); y1 = Math.max(y1, r.bottom + scrollY); });
    return x1 < x0 ? null : { x: x0, y: y0, width: x1 - x0, height: y1 - y0 };
  }, js);
}

// In-page sketches -------------------------------------------------------------------------------------------------
const SKETCH = `
window.__bb = {
  reds(stage) { return [...stage.querySelectorAll('svg')].filter((s) => getComputedStyle(s).color.replace(/\\s/g, '') === 'rgb(230,57,70)'); },
  keyline(stage) {           // Rule 05.3's keyline: a 1 px Charcoal edge inside the mark, drawn as a clipped 2 px stroke
    const ns = 'http://www.w3.org/2000/svg';
    this.reds(stage).forEach((svg, i) => {
      if (svg.querySelector('[data-bb-key]')) return;
      const p = svg.querySelector('path'); if (!p) return;
      const id = 'bbkl' + i + Math.random().toString(36).slice(2, 7);
      const defs = document.createElementNS(ns, 'defs'), cp = document.createElementNS(ns, 'clipPath');
      cp.setAttribute('id', id); const pc = p.cloneNode(); pc.removeAttribute('fill'); cp.appendChild(pc); defs.appendChild(cp);
      svg.insertBefore(defs, svg.firstChild);
      const s = p.cloneNode(); s.setAttribute('data-bb-key', ''); s.setAttribute('fill', 'none');
      s.setAttribute('stroke-width', '2'); s.setAttribute('vector-effect', 'non-scaling-stroke');
      s.setAttribute('clip-path', 'url(#' + id + ')'); s.style.stroke = 'var(--oa-color-palette-charcoal)';
      svg.appendChild(s);
    });
  },
  unkey(stage) { stage.querySelectorAll('[data-bb-key]').forEach((e) => e.remove()); },
  ink(stage) { this.reds(stage).forEach((s) => { s.dataset.bbInk = '1'; s.style.color = 'var(--oa-color-text-primary-on-newsprint)'; }); },
};`;

async function sketchReady(page) { await page.addScriptTag({ content: SKETCH }); }

(async () => {
  const browser = await chromium.launch();
  const t0 = Date.now();
  try {
    // ---------------------------------------------------------------- the page of record at 1440 px, 1x
    if (['ch16', 'openers', 'prm1'].some(want)) {
      const { ctx, page } = await open(browser, cfg.now, 1440, 900, 1);
      if (want('ch16')) {
        const ids = await page.$$eval('figure[id^="fig-s-16-"]', (fs) => fs.map((f) => f.id));
        for (const id of ids) await shotEl(page, '#' + id, 'ch16-1440-' + id.replace('fig-', ''), { width: 1440 });
      }
      if (want('openers')) for (const n of ['16', '20', '21']) await shotEl(page, `section.chapter[data-chapter="${n}"] > .ch-head`, `opener-${n}-1440`, { width: 1440 });
      if (want('prm1')) await shotEl(page, '#fig-s-15-15-correct', 'prm1-after-1440', { width: 1440 });
      await ctx.close();
    }
    if (['openers', 'prm1', 'ch16'].some(want)) {
      const { ctx, page } = await open(browser, cfg.now, 390, 844, 1);
      if (want('openers')) for (const n of ['16', '20', '21']) await shotEl(page, `section.chapter[data-chapter="${n}"] > .ch-head`, `opener-${n}-390`, { width: 390 });
      if (want('prm1')) await shotEl(page, '#fig-s-15-15-correct', 'prm1-after-390', { width: 390 });
      if (want('ch16')) for (const id of ['s-16-1-correct', 's-16-8-correct']) await shotEl(page, '#fig-' + id, 'ch16-390-' + id, { width: 390 });
      await ctx.close();
    }
    // ---------------------------------------------------------------- PR-M1's before: commit bc91667e's page, built in scratch
    if (want('prm1') && cfg.before) {
      for (const w of [1440, 390]) {
        const { ctx, page } = await open(browser, cfg.before, w, w === 1440 ? 900 : 844, 1);
        await shotEl(page, '#fig-s-15-15-correct', 'prm1-before-' + w, { width: w });
        await ctx.close();
      }
    }
    // ---------------------------------------------------------------- sketches at 2x (shown at true size)
    if (['nf1', 'r14d', 'texts'].some(want)) {
      const { ctx, page } = await open(browser, cfg.now, 1440, 900, 2);
      await sketchReady(page);
      if (want('nf1')) {
        const st = '[data-specimen="s-04-3-correct"]';
        await shotEl(page, st, 'nf1-043-today');
        await page.evaluate((s) => __bb.keyline(document.querySelector(s)), st);
        await shotEl(page, st, 'nf1-043-keyline');
        await page.evaluate((s) => { const e = document.querySelector(s); __bb.unkey(e); __bb.ink(e); }, st);
        await shotEl(page, st, 'nf1-043-ink');
        // the link-preview card's headline, B from the display master at 110 px
        const so = '[data-specimen="s-proofs-social"]';
        const hb = await unionBox(page, `const st=document.querySelector('${so}'); const b=__bb.reds(st).filter(s=>s.getBoundingClientRect().height>40); return b.map(s=>s.closest('p')||s);`);
        if (hb) {
          await shotClip(page, hb, 'nf1-social-today', 24);
          await page.evaluate((s) => __bb.keyline(document.querySelector(s)), so);
          await shotClip(page, hb, 'nf1-social-keyline', 24);
        }
      }
      if (want('r14d')) {
        for (const sid of cfg.r14d) {
          const st = `[data-specimen="${sid}"]`;
          await page.locator(st).first().scrollIntoViewIfNeeded();
          const rt = await unionBox(page, `return [...document.querySelectorAll('${st} .rt')];`);
          if (!rt) { meta['r14d-missing-' + sid] = true; save(); continue; }
          await shotClip(page, rt, `r14d-${sid}-newsprint`, 48);
          await page.evaluate((s) => { const e = document.querySelector(s); e.classList.replace('oa-surface-newsprint', 'oa-surface-charcoal'); e.dataset.surface = 'charcoal'; }, st);
          await page.waitForTimeout(100);
          await shotClip(page, rt, `r14d-${sid}-charcoal-today`, 48);
          await page.evaluate((s) => document.querySelectorAll(s + ' .rt .ak-case').forEach((c) => { c.style.stroke = 'var(--oa-color-graphic-essential-on-newsprint)'; }), st);
          await page.waitForTimeout(100);
          await shotClip(page, rt, `r14d-${sid}-charcoal-proposal`, 48);
          await page.evaluate((s) => { const e = document.querySelector(s); e.classList.replace('oa-surface-charcoal', 'oa-surface-newsprint'); e.dataset.surface = 'newsprint'; }, st);
          await page.waitForTimeout(100);
          await shotClip(page, rt, `r14d-${sid}-newsprint-proposal`, 48);
        }
      }
      if (want('texts')) {
        for (const t of cfg.texts) {
          const box = await unionBox(page, t.js);
          if (!box) { meta['text-missing-' + t.name] = true; save(); continue; }
          await shotClip(page, box, `text-${t.name}-today`, 24);
          const box2 = await page.evaluate((js) => { (new Function(js))(); return true; }, t.edit);
          await page.waitForTimeout(100);
          const after = await unionBox(page, t.js);
          await shotClip(page, after, `text-${t.name}-proposal`, 24);
        }
      }
      await ctx.close();
    }
    // ---------------------------------------------------------------- zooms: B at 26 px and a red target, eight times
    if (['nf1', 'r14d'].some(want)) {
      const { ctx, page } = await open(browser, cfg.now, 1440, 900, 8);
      await sketchReady(page);
      if (want('nf1')) {
        const st = '[data-specimen="s-04-3-correct"]';
        const small = `const b=__bb.reds(document.querySelector('${st}')); return [b[b.length-1]];`;
        await page.locator(st).first().scrollIntoViewIfNeeded();
        const bx = await unionBox(page, small);
        await shotClip(page, bx, 'nf1-zoom-today', 3, { zoom: 8 });
        await page.evaluate((s) => __bb.keyline(document.querySelector(s)), st);
        await shotClip(page, bx, 'nf1-zoom-keyline', 3, { zoom: 8 });
      }
      if (want('r14d')) {
        const sid = cfg.r14d[0], st = `[data-specimen="${sid}"]`;
        await page.locator(st).first().scrollIntoViewIfNeeded();
        await page.evaluate((s) => { const e = document.querySelector(s); e.classList.replace('oa-surface-newsprint', 'oa-surface-charcoal'); }, st);
        let hd = await unionBox(page, `return [...document.querySelectorAll('${st} .rt .ak-mark')].slice(0,1);`);
        if (hd) hd = { x: hd.x - 14, y: hd.y + 4, width: hd.width + 28, height: 34 };
        if (hd) {
          await shotClip(page, hd, 'r14d-zoom-today', 0, { zoom: 8 });
          await page.evaluate((s) => document.querySelectorAll(s + ' .rt .ak-case').forEach((c) => { c.style.stroke = 'var(--oa-color-graphic-essential-on-newsprint)'; }), st);
          await shotClip(page, hd, 'r14d-zoom-proposal', 0, { zoom: 8 });
        }
      }
      await ctx.close();
    }
    // ---------------------------------------------------------------- Prussian beside the red target: Loop R18's working
    // page with the stepper on its first step, the device dark (the switch on Match my device) and light
    if (want('prussian') && cfg.loopPage) {
      for (const [w, h, scheme] of [[1440, 900, 'dark'], [1440, 900, 'light'], [390, 844, 'dark']]) {
        const ctx = await browser.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 2, reducedMotion: 'reduce', colorScheme: scheme });
        const page = await ctx.newPage();
        await page.goto('file://' + cfg.loopPage, { waitUntil: 'load' });
        await page.evaluate(() => document.fonts.ready);
        await page.locator('.oa-stepper-next').first().click();
        await page.waitForTimeout(600);
        const find = await page.evaluate(() => {
          const flat = (v) => (v || '').replace(/\s/g, '');
          const cur = [...document.querySelectorAll('*')].filter((e) => { const s = getComputedStyle(e); const b = e.getBoundingClientRect();
            return b.width > 40 && ['rgb(31,45,90)', 'rgb(255,255,255)'].includes(flat(s.backgroundColor)) && e.closest('.oa-stepper, [class*="stepper"]'); });
          const r = (e) => { const b = e.getBoundingClientRect(); return { x: b.left + scrollX, y: b.top + scrollY, r: b.right + scrollX, b: b.bottom + scrollY }; };
          const step = cur.length ? r(cur[0]) : null;
          const reds = [...document.querySelectorAll('svg *')].filter((e) => { const s = getComputedStyle(e);
            return [s.stroke, s.fill].some((v) => flat(v) === 'rgb(230,57,70)') && e.getBoundingClientRect().width; }).map(r)
            .filter((d) => step && d.b <= step.b && step.y - d.y < 900);
          return { step, stepBg: cur.length ? getComputedStyle(cur[0]).backgroundColor : null, reds, nCur: cur.length };
        });
        meta[`prussian-find-${w}-${scheme}`] = { step: find.step, stepBg: find.stepBg, nReds: find.reds.length, nCur: find.nCur }; save();
        if (find.step) {
          const all = [find.step, ...find.reds];
          const x0 = Math.min(...all.map((a) => a.x)), y0 = Math.min(...all.map((a) => a.y)), x1 = Math.max(...all.map((a) => a.r)), y1 = Math.max(...all.map((a) => a.b));
          await shotClip(page, { x: x0, y: y0, width: x1 - x0, height: y1 - y0 }, `prussian-loop-r18-${w}-${scheme}`, 40, { width: w, scheme });
        }
        await ctx.close();
      }
    }
    // ---------------------------------------------------------------- C11-1: a wide frame on a 390 px phone
    if (want('c111')) {
      const { ctx, page } = await open(browser, cfg.now, 390, 844, 2);
      const fig = '#fig-' + cfg.c111;
      await page.locator(fig).first().scrollIntoViewIfNeeded();
      const figTop = async () => { const b = await unionBox(page, `return [document.querySelector('${fig}')];`); return { x: b.x, y: b.y, width: b.width, height: Math.min(b.height, cfg.c111h || 1100) }; };
      const top = await figTop();
      meta['c111-scale'] = await page.evaluate((fig) => [...document.querySelectorAll(fig + ' .oa-app-frame')].map((f) => ({ frame: f.dataset.oaPageFrame, shown: Math.round(f.getBoundingClientRect().width), w: +f.dataset.w })), fig); save();
      await shotClip(page, top, 'c111-today', 0, { width: 390 });
      // studio sketch: the phone frames first, and each wide frame a line that opens its export at true size
      await page.evaluate((fig) => {
        const stage = document.querySelector(fig + ' .plate-stage');
        const blocks = [...stage.querySelectorAll('.sx-rw2')];
        if (!blocks.length) return;
        const isWide = (b) => [...b.querySelectorAll('.oa-app-frame')].some((f) => +f.dataset.w > 600);
        const first = blocks[0], parent = first.parentElement;
        blocks.filter((b) => !isWide(b)).forEach((b) => { parent.insertBefore(b, first);
          b.querySelectorAll('.oa-app-row').forEach((r) => { r.style.flexDirection = 'column'; r.style.flexWrap = 'nowrap'; });
          b.querySelectorAll('.oa-app-frame').forEach((f) => { f.style.flex = 'none'; f.style.width = '100%'; }); });
        const list = document.createElement('div'); list.className = 'sx-rw2';
        const head = document.createElement('p'); head.className = 'sx-lab sx-sec'; head.textContent = 'The wider pages, each at true size'; list.appendChild(head);
        const ul = document.createElement('ul'); ul.style.cssText = 'margin:0;padding:0 0 0 20px;font:var(--oa-type-body-small)'; list.appendChild(ul);
        blocks.filter(isWide).forEach((b) => { const lab = b.querySelector('.sx-lab'); const words = lab ? lab.textContent.replace(/,\s*shown at.*$/i, '') : 'A wide frame';
          const li = document.createElement('li'); li.style.margin = '0 0 8px'; li.innerHTML = '<a href="#" style="color:inherit">' + words + ': open the page at true size</a>'; ul.appendChild(li); b.remove(); });
        parent.insertBefore(list, parent.querySelector('.sx-rw2'));
        parent.insertBefore(parent.querySelectorAll('.sx-rw2')[1], list);
      }, fig);
      await page.waitForTimeout(200);
      const top2 = await figTop();
      await shotClip(page, top2, 'c111-proposal', 0, { width: 390 });
      await ctx.close();
    }
    // ---------------------------------------------------------------- E11b-1 and E11b-2: chapter 18's masthead plate
    if (want('e11b')) {
      const st = '[data-specimen="c-18-masthead--light"]';
      {
        const { ctx, page } = await open(browser, cfg.now, 1440, 900, 2);
        const bar = `return [document.querySelector('${st} .oa-masthead-bar')];`;
        await page.evaluate((st) => document.querySelectorAll(st + ' .oa-masthead-part:not([aria-current]), ' + st + ' .oa-masthead-row-link:not([aria-current])').forEach((a) => a.setAttribute('aria-current', 'false')), st);
        await shotBox(page, bar, 'e11b1-today', 8);
        const changed = await page.evaluate(() => { let k = 0; const walk = (rs) => { for (const r of rs) {
            if (r.selectorText && /oa-masthead/.test(r.selectorText) && r.selectorText.includes('[aria-current]') && !r.selectorText.includes('false')) { r.selectorText = r.selectorText.replace(/\[aria-current\]/g, '[aria-current]:not([aria-current="false"])'); k++; }
            if (r.cssRules) walk(r.cssRules); } };
          for (const sh of document.styleSheets) { try { walk(sh.cssRules); } catch (e) { } } return k; });
        meta['e11b1-rules-changed'] = changed; save();
        await page.waitForTimeout(150);
        await shotBox(page, bar, 'e11b1-proposal', 8);
        await ctx.close();
      }
      for (const [name, extra] of [['e11b2-today', ''], ['e11b2-proposal', '.oa-masthead-dialog .oa-masthead-dialog-nav{margin-top:4px}']]) {
        const { ctx, page } = await open(browser, cfg.now, 390, 844, 3);
        if (extra) await page.addStyleTag({ content: extra });
        const menu = page.locator(st + ' .oa-masthead-menu').first();
        await menu.evaluate((e) => e.scrollIntoView({ block: 'center' }));
        await menu.focus(); await page.keyboard.press('Enter'); await page.waitForTimeout(500);
        const r = await page.evaluate(() => { const d = document.querySelector('dialog[open]'); if (!d) return null;
          const a = d.querySelector('.oa-masthead-dialog-head').getBoundingClientRect(), b = d.querySelector('.oa-masthead-list > li').getBoundingClientRect();
          const f = document.activeElement; return { x: Math.max(0, Math.min(a.left, b.left) - 6), y: Math.max(0, a.top - 6), width: Math.max(a.right, b.right) - Math.min(a.left, b.left) + 12, height: b.bottom - a.top + 12, focus: f ? f.textContent.trim().slice(0, 40) : null, fv: f ? f.matches(':focus-visible') : null }; });
        meta[name + '-find'] = r; save();
        if (r) { await page.screenshot({ path: path.join(OUT, name + '.png'), clip: { x: r.x, y: r.y, width: Math.min(r.width, 390 - r.x), height: r.height }, animations: 'disabled' });
          meta[name] = { w: Math.round(Math.min(r.width, 390 - r.x)), h: Math.round(r.height) }; save(); }
        await ctx.close();
      }
    }
    // ---------------------------------------------------------------- Rule 13.4: the two dashes on Loop R18's page
    if (want('dash') && cfg.loopPage) {
      const { ctx, page } = await open(browser, cfg.loopPage, 1440, 900, 2);
      const box = await page.evaluate(() => {
        const btn = [...document.querySelectorAll('button')].find((b) => /Previous step/.test(b.textContent));
        const dashed = [...document.querySelectorAll('svg path, svg line, svg polyline')].filter((p) => { const d = getComputedStyle(p).strokeDasharray; return d && d !== 'none' && p.getBoundingClientRect().width > 20; });
        const r = (e) => { const b = e.getBoundingClientRect(); return { x: b.left + scrollX, y: b.top + scrollY, r: b.right + scrollX, b: b.bottom + scrollY }; };
        const bb = btn ? r(btn) : null; const row = btn ? r(btn.parentElement) : null; const svgEl = [...document.querySelectorAll('svg')].find((v) => v.querySelector('.rt, [data-red]') && v.getBoundingClientRect().width > 200); const svg = svgEl ? r(svgEl) : null; const near = dashed.map(r).filter((d) => bb && Math.abs(d.y - bb.y) < 700);
        return { btn: bb, row, svg, btnStyle: btn ? getComputedStyle(btn).borderTopStyle : null, dashed: near, n: dashed.length };
      });
      meta['dash-find'] = box; save();
      if (box.btn && box.dashed.length) {
        const all = [box.btn, box.row, box.svg, ...box.dashed].filter(Boolean);
        const x0 = Math.min(...all.map((a) => a.x)), y0 = Math.min(...all.map((a) => a.y)), x1 = Math.max(...all.map((a) => a.r)), y1 = Math.max(...all.map((a) => a.b));
        await shotClip(page, { x: x0, y: y0, width: x1 - x0, height: y1 - y0 }, 'dash-loop-r18-1440', 24);
      }
      await ctx.close();
    }
  } finally {
    await browser.close();
    meta._ran = { at: new Date().toISOString(), seconds: Math.round((Date.now() - t0) / 1000) };
    save();
  }
})().catch((e) => { console.error(e); process.exit(1); });
'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--caps', default=str(SCRATCH / 'board-builder/caps'))
    ap.add_argument('--report', default=str(SCRATCH / 'board-builder/now-build/20261124_Guide-Now-Build-Report.json'))
    ap.add_argument('--wall', default='')
    ap.add_argument('--capture', action='store_true')
    ap.add_argument('--now', default=str(SCRATCH / 'board-builder/now-build/20261124_Guide-Now.html'))
    ap.add_argument('--before', default=str(SCRATCH / 'board-builder/before-build/20261124_Guide-bc91667e.html'))
    ap.add_argument('--only', default='')
    args = ap.parse_args()
    if args.capture:
        capture(args)
        return
    rep, scores, specs, atest, chapters, caps, meta = load_inputs(args)
    META.update(meta)
    global C16V_RESCORE, CD12B
    sc12b = ROOT / 'work/handoffs/phase-4/20261124_Chat-12b-CD-Scores.json'
    if sc12b.exists():
        CD12B = json.loads(sc12b.read_text()).get('rescore_12b', {})
        C16V_RESCORE = CD12B.get('c16v_for_board')
    global CAPS
    CAPS = caps
    OUT.mkdir(parents=True, exist_ok=True)
    if IMG.exists():
        shutil.rmtree(IMG)
    IMG.mkdir(parents=True)
    body = (sec_decisions(rep) + sec_approved(caps, meta, rep) + sec_ch16(caps, meta, chapters['16'], rep)
            + sec_web(rep) + sec_atlas(rep, atest, chapters['21'], args.wall) + sec_specs(specs) + sec_rescore(scores)
            + sec_tested(meta, caps, rep))
    html_out = page(body, rep)
    check(html_out)
    PAGE.write_text(html_out)
    files = [p for p in OUT.rglob('*') if p.is_file()]
    size = sum(p.stat().st_size for p in files)
    if size > LIMIT_BYTES or len(files) > LIMIT_FILES:
        sys.exit(f'the board folder holds {len(files)} files and {size:,} bytes, past {LIMIT_FILES} files or {LIMIT_BYTES:,} bytes')
    print('wrote', PAGE.relative_to(ROOT), f'{len(html_out.encode()):,} bytes;', f'{len(list(IMG.iterdir()))} pictures;',
          f'folder {len(files)} files, {size:,} bytes')


if __name__ == '__main__':
    main()
