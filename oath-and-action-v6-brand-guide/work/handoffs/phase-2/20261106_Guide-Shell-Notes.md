# Guide shell notes, stage board A

Oath & Action Edition 06, Phase 2, November 6, 2026. Written by the guide engineer for the editor, the identity designer and the systems designer, under `work/handoffs/phase-2/20261106_Stage-A-Brief.md`. This is a living file: the sections marked "for makers" stay stable; the engineer's report sits at the end.

## 1. Preview your chapter (for makers)

From the repository root:

```
python3 -I work/build/scripts/phase-2/guide_build.py
```

It writes `work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html` and, beside it, `20261106_Stage-A-Chapters-Build-Report.json`. Open the page in a browser and look at your chapters at 1440 and 390 px. The build never stops on a content problem. It prints each one as a `warning [where] message` line and stores the list in the report. Fix your own warnings before you hand back.

- It builds with none, some or all chapter files. A chapter of 01 to 08 with no file gets a placeholder that keeps its anchor, number and contents entry.
- `--demo` fills the first missing chapter with the shell's sample rules (two rules, every block, labeled "Template demonstration"), so you can see each block before your file exists.
- `--strict` exits 1 on any warning. The main session uses it at hand-back.
- `--out PATH` writes somewhere else, for a private test build. `--chapters DIR` and `--specimens DIR` point at other folders.

The rendered checks (section 6):

```
node work/build/scripts/phase-2/guide_check.js work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html
```

## 2. Where files go

| What | Path | Owner |
|---|---|---|
| Chapter content | `work/build/guide/chapters/NN-anchor.json`, for example `05-color.json`, `08-signal-grid.json` | each maker |
| Proofs appendix order and captions (optional) | `work/build/guide/chapters/proofs.json` | identity designer |
| Specimens | `work/build/guide/specimens/<id>.html` | each maker |
| Specimen manifests | `work/build/guide/specimens/manifest-<maker>.json` | each maker |
| Shell style, script, sample fixtures | `work/build/guide/shell/` | engineer |
| Build | `work/build/scripts/phase-2/guide_build.py` | engineer |

The file name's number and anchor must match the architecture map (`01-purpose`, `02-voice`, `03-identity`, `04-ampersand`, `05-color`, `06-type`, `07-layout`, `08-signal-grid`). The build warns when they do not.

## 3. Chapter JSON: what the shell reads (for makers)

The content contract in the Stage A brief stands. The shell reads these fields, and three optional ones the brief does not name:

| Field | Shell use |
|---|---|
| `number`, `anchor`, `title`, `instruction` | h2 "05 Color" and the instruction line under it. `title` and `instruction` also feed the contents, the part opener, the rail and the phone menu |
| `intro` | at most two paragraphs under the instruction line |
| `rules[]` | one rule block each, in order (section 4) |
| `rules[].why.basis` | the "Basis" tag. Write `Design judgment`, `WCAG 2.2 SC 1.4.3`, or a named source |
| `rules[].tokens`, `specs[].token` | token chips with the value from `tokens.json`. Write the DTCG name (`oa.color.text.primary.onNewsprint`); the shell shows the CSS name (`--oa-color-text-primary-on-newsprint`). A name the token file lacks is a warning |
| `rules[].files` | repository paths, shown as code. A path that does not exist is a warning. Download buttons arrive with the asset package in Phase 5 |
| `rules[].related` | chapter numbers, shown as links under "Related chapters" inside the rule. A chapter not in this page shows its number and name with "later stage", never a dead link |
| `extras[]` | `{ "after_rule": "05.3", "specimen": "...", "caption": "...", "label": "optional label" }`. Leave `after_rule` out to place the extra above the first rule |
| `sources[]` | a numbered "Sources" list at the end of the chapter, before the closers |
| `related_chapters[]` (optional) | `{ "chapter": "06", "reason": "Which sizes count as large text." }` for the chapter's own "Related chapters" closer. Without it the shell uses the map's section 10 list with short reasons, plus any chapter a rule cites |

**Inline text.** Every string is escaped, then these inline tags are kept: `<em> <strong> <code> <abbr title> <q> <cite> <sup> <sub> <br> <span class="..."> <a href="#..."> <a href="https://...">`. Anything else shows as text. The shell links each "Rule 05.2" it finds to `#rule-05-2` when that rule is in the page, and each "chapter 06" to `#type`, so you rarely need an `<a>`. Use `<span class="illus">Illustrative</span>` for an inline Illustrative label.

## 4. The block markup the shell renders (for makers)

You never write this markup; it is here so you know what your fields become, and what the checks look for. A chapter:

```html
<section class="chapter" id="color" data-track="chapter" data-part="foundations" data-label="05 Color" data-chapter="05">
  <div class="ch-head">
    <p class="loc-line"><a href="#part-foundations">Foundations</a> · Chapter 05 of 28</p>
    <h2 class="ch-title" id="color-h"><span class="n">05</span> <span class="t">Color</span></h2>
    <p class="instr">Choose a surface first, then the text and graphic colors that pass on it.</p>
    <p class="intro">...</p>
  </div>
  <div class="local-toc">In this chapter: every rule, then the three closers</div>
  <div class="ch-body">
    rules and extras, then Sources, then three closers:
    <div class="closer" id="color-specs"><h3>Specifications</h3> every token the chapter names, with its value and the rules that use it; every file</div>
    <div class="closer" id="color-related"><h3>Related chapters</h3> two to five chapters, each with its reason</div>
    <div class="closer" id="color-builders"><h3>For builders</h3> the chapter's custom properties as a CSS block, with a Copy button</div>
  </div>
  <div class="chapnav">Previous, Next, Back to contents</div>
</section>
```

One rule, in the Master Brief section 7 order. The h3 starts with the Rule ID and the rule block owns the matching anchor (map section 4). Everything after the h3 is a visible label, not a heading (map section 5):

```html
<div class="rule" id="rule-05-2" data-rule="05.2">
  <h3 class="rule-h"><span class="rid"><span class="rid-w">Rule</span> <span class="rid-n">05.2</span></span> <span class="rt">Text sits only on pairs that pass.</span></h3>
  <div class="rule-body">
    <p class="rule-text">the rule</p>
    <div class="tokens"><p class="label">Tokens</p><ul class="tok-list">chips</ul></div>
    <div class="why"><p class="label">Why it works</p><p class="basis">Basis WCAG 2.2 SC 1.4.3</p><p>...</p></div>
  </div>
  <div class="hinge" aria-hidden="true">hairline, ampersand B, hairline</div>
  <figure class="plate plate--correct">Correct application</figure>
  <figure class="plate plate--failure">Failure case</figure>
  <figure class="plate plate--corrective">Corrective example (only when the rule has one)</figure>
  <div class="rule-foot">
    <div class="foot-block foot-specs"><p class="label">Specifications</p><dl class="spec-list">label, value, token</dl> Files</div>
    <div class="foot-block foot-related"><p class="label">Related chapters</p>links</div>
    <div class="foot-block foot-builders"><p class="label">For builders</p>note</div>
  </div>
</div>
```

The hinge divider is the shell's: a hairline broken by ampersand B (`work/build/assets/identity/ampersand/20261028_Amp-B-24px-Master.svg`, drawn at its true 24 px) in the surface's ink, `--oa-color-identity-hinge-divider` (D1-22, D1-26). It sits between each rule and its correct use, with the ampersand on the edge of the text column. Do not draw it in a specimen to separate blocks.

## 5. How a specimen fragment is framed (for makers)

Your file `work/build/guide/specimens/s-05-2-correct.html` is a fragment: markup and, if you need one, a `<style>` block. No `<html>`, `<head>` or `<body>`, and no `<h1>` to `<h6>` (styled text only). The shell puts it on a plate:

```html
<figure class="plate plate--correct" id="fig-s-05-2-correct">
  <div class="plate-head">
    <p class="plate-label"><span aria-hidden="true">✓</span>Correct application</p>
    <p class="plate-size">True size, 640 px wide</p>
  </div>
  <div class="plate-scroll" data-plate-scroll>                      the mat: a deeper Newsprint around the specimen
    <div class="plate-stage oa-surface-newsprint" data-specimen="s-05-2-correct" data-red="specimen"
         data-surface="newsprint" style="--w:640px" role="img" aria-label="(your manifest alt)">
      YOUR FRAGMENT
    </div>
  </div>
  <figcaption class="plate-cap"><span class="illus">Illustrative</span> your caption</figcaption>
</figure>
```

What the frame does for you, so the specimen does not have to:

- **True size.** The stage is exactly `width_px` wide. Set your own height. A specimen wider than the screen keeps its size: the mat scrolls sideways, becomes a named keyboard region, and shows a line saying so. Nothing is scaled.
- **Surface.** The stage takes the token surface class for your manifest's `surface` (`newsprint` by default, or `white`, `charcoal`, `prussian`). That class sets the background and the short role names, so inside the specimen `var(--oa-color-text-primary)`, `var(--oa-color-border-hairline)`, `var(--oa-color-focus-ring)` and the rest already point at that surface's values. Long names (`--oa-color-text-primary-on-newsprint`) work too.
- **Alt text.** The stage is `role="img"` named by your manifest's `alt`, so a screen reader hears one full description. If the specimen has controls a reader should use (a demo, a composer), set `"interactive": true`: the stage becomes a group, your controls stay reachable, and the alt is read as its description.
- **Illustrative.** `"illustrative": true` prints the Illustrative label at the start of the caption (H03), unless your caption already says it.
- **Red.** The stage carries `data-red="specimen"`, so red inside a specimen does not count toward the page's red (D2-102). Inside the specimen, still mark what the red is: `data-red="signature"` on a wordmark or lever, `data-red="working"` with `data-red-job="..."` on the one working red the specimen shows as its own view. The check allows one working-red job per specimen, and none on Prussian.
- **Styles stay inside.** Your `<style>` is wrapped in `@scope ([data-specimen="your-id"])`, so `.label { ... }` styles only your specimen and never the shell. The shell's own element styles are class-based, so a specimen inherits only the font (Inter, 17 px) and the surface's text color.
- **Ids stay unique.** Every `id` in your fragment becomes `your-id--name`, and the build rewrites `href="#name"`, `url(#name)`, `aria-labelledby`, `aria-describedby`, `for`, CSS `#name` selectors and `getElementById('name')` to match. In a `<script>`, find your elements from `document.currentScript.closest('[data-specimen]')`.
- **Assets by repository path.** `<img src="work/build/assets/...svg" alt="...">` is inlined into the page as a data URI, so the page stands alone. Add `data-inline` to an SVG `<img>` to place the master as inline SVG instead, so it takes `color` and the `--amp` and `--lever` properties: `<img data-inline src="work/build/assets/identity/wordmark/20261028_Wordmark-Display-Master.svg" alt="Oath & Action" width="480" data-red="signature">`. An empty `alt` hides it from assistive technology.

**Manifest fields.** `manifest-<maker>.json` maps each id to `{ chapter, rule, width_px, alt, illustrative, notes }` (brief), and the shell also reads:

| Field | Use |
|---|---|
| `surface` | `newsprint` (default), `white`, `charcoal` or `prussian` |
| `height_px` | adds the height to the plate's size line |
| `interactive` | `true` for a specimen with controls (above) |
| `check_exempt` | `["contrast"]`, `["red"]` or `["size"]`. Contrast and red exemptions are for labeled failure cases only, and so is `size` unless the caption says the plate shows a mark or a minimum size at true size. The rendered check skips that test inside the plate and lists every exemption in its results |
| `caption`, `label` | for the `s-proofs-*` set when `proofs.json` gives none |

**Colors.** Only `var(--oa-...)` from `work/build/tokens/tokens.css`. The build warns on any literal hex, `rgb()` or `hsl()` outside a `var()` fallback and outside path data.

**The proofs appendix** (identity designer). Every specimen whose id starts `s-proofs-` goes into the appendix after chapter 08, in manifest order. For groups and captions, write `work/build/guide/chapters/proofs.json`:

```
{ "intro": ["..."], "groups": [ { "label": "Masthead", "text": ["..."],
    "items": [ { "specimen": "s-proofs-masthead-today", "label": "Today's width", "caption": "..." },
               { "specimen": "s-proofs-masthead-condensed", "label": "Condensed, for Gate 2", "caption": "..." } ] } ] }
```

Each group label is an h3. Two plates in a group sit side by side when both fit at true size, and wrap when they do not.

## 6. Checks (for makers)

`guide_check.js` is the rendered check for guide pages. `dataviz_check.js` stays as it is, for charts.

```
node work/build/scripts/phase-2/guide_check.js work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html
```

It opens the page at 1440, 1024, 390 and 360 px (`--quick` for 1440 and 390) and fails on:

- Structure: exactly one h1; no skipped heading level; no heading inside a specimen; every h3 in a chapter is a rule h3 or one of the three closers; every rule h3 starts with "Rule NN.n", its NN is its chapter's number, and its rule block carries `id="rule-NN-n"`.
- Anchors: every id unique; every same-page link lands on an id; every Related chapters link lands on a chapter; each V5 alias the page needs (`#grid`) sits inside its new chapter.
- Specimens: every plate stage has an alt (an `aria-label` of at least 15 characters), every `<img>` has `alt`, every inline `<svg>` is named or hidden.
- Text: none under 13 px, and every text pair at 4.5 to 1 (3 to 1 for large text), computed from rendered colors; exempt plates are skipped and listed.
- Rule 05.3: every Pillar Red mark sits under a `data-red`; at most one working-red job in the page outside specimens and one inside each specimen; no red on Prussian.
- Writing: the locked lines character for character wherever a fragment of one appears; no em dash outside an element marked `data-allow-emdash` (W21's specimen).
- Page: no sideways scroll outside a scrolling frame; axe-core with the WCAG 2.2 AA tags; a visible focus ring on the first 60 Tab stops at 1440; no outside requests other than Google Fonts; no script errors.

It writes `<page>-Guide-Check-Results.json` beside the page and full-page captures to `captures/` beside it.

**axe-core.** Do not run `npm install --no-save axe-core@4.10.2` in `work/build` as the brief has it. `work/build` has no `package.json`, and that command removes every package installed earlier the same way, including `style-dictionary` 5.8.0, which the token build needs. I tested this in a scratch folder: a second `--no-save` install removed the first package. Either install both together:

```
cd work/build && npm install --no-save axe-core@4.10.2 style-dictionary@5.8.0
```

or install axe-core outside the repository and point the check at it:

```
npm install --prefix "${TMPDIR:-/tmp}/oa-axe" axe-core@4.10.2
AXE_PATH="${TMPDIR:-/tmp}/oa-axe/node_modules/axe-core/axe.min.js" node work/build/scripts/phase-2/guide_check.js <page>
```

`guide_check.js` finds axe-core at `AXE_PATH`, then `work/build/node_modules/axe-core`, then `${TMPDIR:-/tmp}/oa-axe/node_modules/axe-core`.

## 7. The shell, in brief

- **Ground and type.** Newsprint everywhere, Charcoal text, Deep Stone for secondary text. Inter Tight for headings, Inter for reading, from `tokens.css`'s type styles (`--oa-type-section` for chapter titles, `--oa-type-h3` for rules, `--oa-type-intro` for the instruction line and the rule, `--oa-type-label` for labels). The cover sets the tagline in `--oa-type-title` as display text under the h1. Lora Italic is left to the chapters' quoted lines.
- **Navigation, as the Gate 1 wireframes draw it.** A sticky masthead with the wordmark (24 px master, 16 px on phones), "Brand Guide Edition 06", and the part links. A chapter rail on the left from 1024 px, with the current chapter on a White band with a 4 px Charcoal bar. "In this chapter" in a right column from 1280 px, above the first rule below that, with the current rule underlined. Location line over every h2, "Return to ..." after a cross-reference, focus moved to the heading a link lands on. On phones, the wordmark, the current chapter's name and a Menu button that opens a modal dialog with one navigation block.
- **Landmarks.** One banner (masthead), one navigation block for parts and one for chapters, main, one contentinfo (the colophon). The phone menu holds a single navigation block. Chapters are sections with headings and no region names.
- **Part opener.** A Charcoal panel, the part's one dark beat (Rule 05.1), with each chapter and its instruction line. The pillar mark that marks each part waits for board B (DR-88).
- **Anchors.** Chapter anchors are words (`#color`). V5's `#grid` sits at the top of `#signal-grid`. Rules are `#rule-05-2`; closers are `#color-specs`, `#color-related`, `#color-builders`.
- **Tokens.** `tokens.css` is inlined into the page. If it is missing, the build writes a provisional block from the Phase 1 schema draft and says so on the page.

## 8. Engineer's report

To be completed at hand-back: routine calls as proposed decision lines, open questions, Tested, Not tested, change log.
