# Apply pass: engineer notes, board 3 (chat 9)

Status: started 20:18 UTC. Reading the brief, decisions and register rows. Items: A5, A3, A4, A12, A7c, A1, A15, then A6 last.

## Fixed

| Item | What changed | File | Proof |
|---|---|---|---|
| A5 (reply 10) | The 16 px wordmark now shows through 23.25em (372 px), in place of under 22.5em; from 373 px the 24 px wordmark returns, so 375 px keeps it. Neither drawing changes. The scripts-off floor `--head-floor: 8.25rem` for 22.5em to 23.25em is gone, since no width at the default text size now drops the menu button; the 64em to 85.125em floor stays. Two comments say so | `work/build/guide/shell/guide-shell.css` | Chromium, scripts on and off, same numbers both ways. Before: 360 and 372 px, 24 px wordmark (221 px wide), menu button on a second line, masthead 133 px, head offset 156 px; 375 and 390 px, 24 px wordmark, one line, 89 px. After: 360 and 372 px, 16 px wordmark (152 px wide), button on the first line, masthead 89 px, head offset 112 px; 373, 374, 375 and 390 px unchanged at 89 px with the 24 px wordmark; 320 and 359 px unchanged. No sideways scroll at any width. Strict build exit 0, 0 warnings; page 12,178,909 to 12,178,831 bytes (the CSS rule and comment only) |

## Not fixed

(none yet)

## Calls

## Requests

## Tested

## Not tested
