# Chat 11: board builder's notes

Started November 21, 2026 at 21:00 UTC; first draft written at 21:12 UTC; rebuilt from the final exports at 21:21 UTC (each time read with `date -u`). Work: chat 11's progress board for Dustin, modeled on chat 10's (`chat_10_progress_build.py`). It asks for no decision.

## What I built

- `work/build/scripts/phase-4/chat_11_progress_build.py`, run from the project folder with `python3 -I`. It writes `work/boards/phase-4/chat-11/20261121_Chat-11-Progress.html` and `img/`. Options: `--quick-check TEXT` fills the one row the main session owns ("Quick guide check at 1440 and 390 px: result to come."); `--guide-url URL` adds a panel linking the chapters page.
- What it reads: the 30 `20261121_Web-*` exports; the kit's plates `a06.json` to `a08.json` (`views[].screens`, contract C5); Rule 20.9's `section_words` from `phase4_ch20_build.py`, read as text and never run; `20-web.json` for the rule count; the chapter 21 plan for its groups, 16 rule titles, 712,600-byte estimate and 655,000 allocation.
- Sections: the opening; the website (each page's first screen large at 1440, 1024, 390 and 360 px light and 1440 and 390 px dark, each captioned with page, width and theme and linking its whole page; the menu open at 390 and 360 px light and 390 px dark; the share preview; the icons at their sizes, the ICO's three images also at four times, pixelated); Rule 05.1 under DR-310 (one table per page and view, 90 screens, Newsprint, dark and red percent); checked and not checked; chapter 21's plan; the seven items for Phase 4 board 1 with the studio's recommendations.
- Pictures: whole pages as WebP at quality 88, first screens (cropped to C5's window heights) at 92, menus and share card at 92; icons lossless; the SVG favicon copied as the file the site serves. The ICO's 16, 32 and 48 px images are extracted to three lossless WebP files.
- The main session's two corrections at about 21:05 UTC are in: the projected page's room is printed as the projection (15.82 MB projected, 13.08 MB today), and chapter 19's seven criteria are named with their rules.
- 21:21 UTC, the main session's second message: the page now prints the final strict build of 21:20:35 UTC (13,080,193 bytes, 393 rules, 731 specimens; chapter 20 at 838,748 against 757,000; 182,246 bytes under 16 MB projected) and a "Done after the board's first draft" paragraph naming the engineer's three fixes and the sweep. `CAPTION_NOTES` is empty, and the 1024 px article's alt describes the fixed panel. Every picture comes from the exports written 21:17:43 to 21:18:20 UTC; the plates a06 to a08 were written 21:18:00 to 21:18:19, and all 90 screens still pass.

**The folder:** 48 files (the page and 47 pictures), 6,817,834 bytes. The page alone is 67,429 bytes.

## Found while building, for the main session

Both are fixed in the 21:18 exports, and the engineer fixed a third ("How the Census Bureau counts them" set far from its text). I looked at the new pictures at 21:21 UTC: the article's 1024 px count panel shows 39,555 whole, with no ink in the panel's last 30 columns; the Census heading sits with its paragraph at 1440 and 390 px; "Who decides" has its space above it at 1440 and 390 px. Of the 18 first screens, only the article's 1024 px one changed from the first draft's, inside the count panel.

1. **The article at 1024 px:** the count panel's figure "39,555" runs to the panel's right edge and its last digit is cut (`20261121_Web-Article-Page-Special-Districts-1024-Light.png`, the panel ends at x = 984, and in its last column, x = 983, the digit's light ink fills 48 of the 70 rows from 505 to 574, so the glyph is cut at the edge). The frames match the exports, so Rule 20.7's plate in the guide shows it too. The board prints a caption note under that picture and its alt text says so; when the export is redrawn, clear `CAPTION_NOTES` and the alt in `ALT[('article', 1024, 'Light')]`, then rerun the script.
2. **The Act page, "Who decides":** the heading sits on the last line of "What the record shows" with no space above it, at 1440 px and at 390 px (the two widths I looked at). The board does not mention it.

## Tested

- The script runs clean (exit 0) and stops on: an unfilled placeholder, an em or en dash, the filler and corporate words chapter 02 lists, an image without alt text of 12 or more characters, a screen fault in the plates, a folder over 40 MB.
- By script on the written page: every tag closed; all 53 `img/` references resolve and every file in `img/` is referenced; 35 images, 35 with real alt text; no straight apostrophe in the text (the plan's rule titles are converted).
- The page's text read through against `CLAUDE.md` and chapter 02's rules; figures checked against the notes, the plates and the main session's build log in its scratch (13,079,965 bytes, 393 rules, 731 specimens, chapter 20 at 838,520, 182,474 under 16 MB projected, 96 PASS lines in the chart kit log, chapter 14's 99 of 99).
- Every first screen, the three menus, the share card and two icons looked at as images, to write the alt text. One WebP first screen compared with its PNG on a crop with small type and the red dot: mean difference about 1 level in 255.

## Not tested

- The page in a browser at any width, 390 and 1440 px included: held until the main session's message. The layout at 390 px is reasoned from the CSS (single columns under 300 px tracks, `min()` in every grid minimum, images at `max-width: 100%`), not seen.
- The links that open each whole page in a new tab, inside a published artifact.
- The page's dark theme, which follows chat 10's tokens.
- A screen reader on the page.
