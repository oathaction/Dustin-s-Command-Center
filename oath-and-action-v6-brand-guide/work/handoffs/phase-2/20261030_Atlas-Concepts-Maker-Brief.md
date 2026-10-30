# Atlas concepts: the maker's brief

Oath & Action Brand Guide, Edition 06. Phase 2, October 30, 2026. Every concept maker reads this file after its own task message. Your task message names your concept, its folder and its sources.

## The bar

Dustin asked for the atlas to be "distinct, very visual, intuitive and beautiful", and for every piece to look like "a finished product that looks like it was made by the best branding and design team in the world." Treat that literally. Your page sits beside eleven others on Board 2, scored by the creative director on craft, clarity, brand fidelity, usefulness, evidence honesty, accessibility, and beauty and distinctiveness ("would a renowned studio show this?"), with 4 of 5 as the ship line on every one. Two more tests: a first-time reader looking at your overview for ten seconds can say what the system is about and where to click; and the overview would hold a wall at poster size.

Push your one big idea as far as it goes. Keep everything around it quiet and exact.

## Read first, in this order

All paths are relative to `/home/user/Dustin-s-Command-Center/oath-and-action-v6-brand-guide/`.

1. `CLAUDE.md`: studio rules. Follow its writing rules in every word on the page: plain spoken prose, active voice, no em dashes, none of the listed patterns.
2. `work/handoffs/phase-2/20261030_Atlas-Concepts-Brief.md`: the brief, all nine sections. Section 4 holds the brand rules and Rule 05.3, section 8 the technical contract.
3. The four approved memos (DR-24), in `work/handoffs/phase-2/`:
   - `20261030_Atlas-Civic-Education-Memo.md`: what each level teaches, the wording rules, the read-aloud line.
   - `20261030_Atlas-Dataviz-Memo.md`: loops as routes, the data contract per level, the overview options.
   - `20261030_Atlas-Interaction-Memo.md`: views with a panel, keyboard, step-through, phone.
   - `20261030_Atlas-Design-Frame-Memo.md`: page frame, type scale, stroke family, arrowheads, sign tags, grounds, the finish checklist.
4. The shared files in `work/boards/phase-2/atlas-concepts/shared/`: the type and line specimen, the kit (`atlas-kit.js`, `atlas-kit.css`) and its demo, the loop-route study and `20261030_Loop-Route-Geometry.json`, and `20261030_Variable-Icon-Map.json`. Open the HTML files in Chromium and look at them.
5. Your own sources, named in your task message.

## What you build

One self-contained HTML page with hash views, built by a Python script from the model export `work/boards/phase-2/maps/20261028_Maps-Model-Data.json`. Never type a label, sign, grade, delay, count or title by hand.

**Views** (D2-64):
- `#overview`: the whole system in your concept's idea, written for a first-time public reader (DR-19). It carries a headline and deck (studio drafts, written by you from the civic education memo's lines or your own, every fact from the model), a one-line "how to read this", and the strip of all 23 loops (or a clear link to a `#loops` view that holds it).
- `#area-c`: Electoral competition with all five variables (C1 to C5), their connections in and out, and the loops grouped under it (R4a, R10, R12, B4). Include it wherever your idea has a middle level; it is the step between the system and R10.
- `#loop-r10`: R10, "Safe seats shift accountability to small primary electorates", at full size. It shows each station with its "a higher value means" line; each step's name, its verb ("raises" or "lowers") beside the sign mark, its evidence texture and grade word with a gloss, and its delay; the weakest step, L53; the read-aloud line built by script from the signs; the loop's summary and qualification; and where reform R-01 acts (its targets L25, L08 and C2), drawn in the view's one working red (DR-18).
- Optional `#loops`: the strip of all 23 loops on its own, if it does not fit the overview.

**The loop strip.** All 23 loops (`loop_order`), each a small drawing of the loop's real route in your concept's idiom (DR-15), with its ID, kind ("Reinforcing, feeds itself" or "Balancing, pushes back") and V7 title, and, where room allows, its stations and weakest step. Dustin asked for "a page with lots of slightly different looking loops" and likes catalogs that carry more text per loop. Mark the two loops closed with a hypothesized step (R2, R16) and the three sketches (B2, B3, R9) plainly. Wrap the strip in `data-strip="loops"`.

**Frame.** The approved wordmark master inlined as delivered (`work/build/assets/identity/wordmark/20261028_Wordmark-24px-Master.svg`, the 16 px master at 390 px; on Prussian the White files in `work/build/assets/identity/prussian/`), wrapped in `data-red="signature"`. A breadcrumb, and a footer source line: "Who Do They Answer To? Systems Atlas V7, snapshot October 15, 2026." with the counts.

**Phone.** Every view works at 390 px with no sideways scroll. A wide drawing may sit in a focusable scroll region (`role="region"`, `tabindex="0"`, an `aria-label`) with "the lines in words" below it.

**Icons.** Civic Line icons may stand beside variables and reforms, exactly as drawn, inlined with `icon_svg()` from `work/build/scripts/phase-2/atlas_concepts_common.py` (one-color editions in rows; D2-52, D2-58). Print the V7 label, never the icon's name.

**Interaction.** Inline `atlas-kit.js` and `atlas-kit.css` (you may restyle the CSS to your concept; keep the behavior): hash views, the selection panel, keyboard model, focus on view change, reduced motion. Hover never carries anything focus and tap do not also give. A step-through of R10 is welcome.

**Contract** (brief section 8): `<meta name="atlas-views" content="overview area-c loop-r10">` listing your views; `data-view-root` on each view's root; `data-node` with `data-name`, `data-link` with `data-sign`, `data-grade` and `data-delay`, `data-loop` with `data-steps` (`sketch` for B2, B3, R9), `data-reform` with `data-targets`, `data-count` on printed counts; `data-red` and `data-red-job` on every Pillar Red mark; every drawing an `<svg data-view="...">`; Google Fonts only (Inter Tight, Inter, Lora Italic), no other outside request.

## How you work

1. Study your sources and the data. Decide the idea's strongest form before drawing.
2. Write the build script beside your page as `build_concept.py`. Run Python with `-I` and import the shared helpers by path, as the docstring of `atlas_concepts_common.py` shows.
3. Render and look. Capture your views with Playwright in Node (`require('playwright')` works from any directory; `chromium.launch()` needs no options) and view the images with the Read tool. Make at least two full refinement passes on craft: alignment to the grid, label placement and collisions, line weights, spacing, the hierarchy of type, color discipline, the phone form. Fix what you see.
4. Run both checks until they pass:
   - `python3 -I work/build/scripts/phase-2/atlas_concepts_verify.py <your page>`
   - `node work/build/scripts/phase-2/atlas_concepts_check.js <your page>` (this also writes captures to your folder's `captures/`)
5. Write your notes (below) and stop.

## Your notes

`work/handoffs/phase-2/20261030_Concept-NN-Notes.md` (NN is your number), 500 to 900 words: the idea in one paragraph; what each view shows and why; the decisions you made, one line each with its reason; your own score on the seven rubric lines with one line each; what you tested and what you could not test, as two lists; and a change log of the files you created.

## Limits

- Write only inside your concept folder and your notes file. Everything else is read-only: the shared files, the scripts other than your own, the icons, the identity masters, the ledgers, other concepts' folders and `source/`.
- Never invent a variable, connection, statistic or name. Headlines are studio drafts; say so in your notes.
- Do not commit. The main session commits.
- Scope: two or three views and the strip. Do not build more.
- When you finish, reply with a summary under 200 words: the idea, the views, the check and verify results, and the one thing you would improve with more time.
