# Board conventions for Phase 1

Every Phase 1 board is a standalone HTML file in `work/boards/` that Dustin can open in a browser.

- Start each board with `<!doctype html>`, a charset meta, a viewport meta, a `<title>`, a link to Google Fonts (Inter Tight 600 and 800, Inter 400, 600 and 700, Lora Italic 400) and `<link rel="stylesheet" href="board-base.css">`. Add board-specific CSS inline.
- Reference images and SVGs by relative path from `work/boards/`. Keep each board's assets in `work/boards/phase-1/<board-slug>/`.
- Show marks as inline SVG or `<img>` at true pixel sizes, with magnified views rendered without smoothing (`class="pix"`).
- Put every proposal beside the original it changes. Label each item "Defect fix" (`.tag.defect`) or "Option" (`.tag`).
- End each board with a "Decisions for Gate 1" panel (`.decision`): each decision, the options, and the studio's recommendation with a one-line reason.
- Follow the writing rules in `CLAUDE.md`. Boards are review documents, not guide chapters, so they may use the current V5 palette freely.
- Phase 1 changes no master. Proposals live in the board folders only.
