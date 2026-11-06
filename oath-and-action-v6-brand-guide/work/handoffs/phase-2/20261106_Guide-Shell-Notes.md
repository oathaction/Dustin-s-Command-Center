# Guide shell notes, stage board A

Oath & Action Edition 06, Phase 2, November 6, 2026. Written by the guide engineer for the editor, the identity designer and the systems designer, under `work/handoffs/phase-2/20261106_Stage-A-Brief.md`. This is a living file: the sections marked "for makers" stay stable; the engineer's report sits at the end.

## 0. New interfaces for the fix pass (for makers)

Published first in the fix pass, under `work/handoffs/phase-2/20261106_Stage-A-Fix-Pass-Brief.md` ("New interfaces"). Write against these now. The build reads every key below; until a key's rendering lands in the shell, the build accepts it and ignores it, so nothing you write will break the page.

### Manifest keys (`manifest-<maker>.json`)

| Key | Write it when | What the shell does |
|---|---|---|
| `"readable": true` | The specimen is a static table or list whose words a reader needs (minimums, palettes, term tables, checklists) | The stage becomes a group named "Correct application, Rule 03.4, specimen" (the plate label, the rule, then "specimen"; an extra without a label takes the first words of its alt). The table or list keeps its structure for assistive technology. Your alt becomes the group's description, read once. Nothing claims interaction (D2-255) |
| `"interactive": true` | Only for a specimen with controls a reader uses (the composer, a demo with buttons) | The same group, named "..., interactive specimen" |
| neither | Everything else: a picture of a piece | The stage is an image named by your alt, as now |
| `"scale": 0.25` | A drawing shown smaller than the thing it shows | The size line reads "One quarter size" in place of "True size". Also 0.5 "Half size", 0.2 "One fifth size", 0.1 "One tenth size"; any other value prints its percent. Text in the drawing passes the type-scale check at its drawn size or at its size divided by the scale |
| `"check_exempt": [..., "scale"]` | Type off the D2-254 sizes on purpose: a labeled failure, a historical record (our fifth edition as it was) or a print piece set in points | The type-scale check skips the plate and lists the exemption. Put the reason in `notes`; the build warns when `notes` is empty, or when a plate that is not a failure gives no print or historical reason |
| `"fit_switch": true` | A wide comparison frame (the masthead and social card pairs) | A "True size / Fit to window" switch in the plate head, true size by default. Fit to window scales the whole stage down to the frame's width and the size line says by how much |
| `"width_px"` | Every specimen of a thing with a width (C-S6) | The stage is that wide and the size line prints it. Leave it out only for page text the shell should flow |

**Room at true size.** A plate's stage has 770 px at 1440 (columns 3 to 10, less the mat), 606 px at 1024 and 608 px at 768. On phones the mat keeps 16 px each side (C-S7), so a stage has the screen width less 32 px: 358 px at 390 and 328 px at 360. A fluid SVG whose labels sit near 13 px drops under the floor there; give it a `width_px` or larger labels. From 1440 the appendix spans the whole page with a 24 px mat, so a proof stage has 1,264 px at true size; wider ones scroll, and `fit_switch` offers the fit.

**Type sizes inside a specimen (D2-254), checked by `guide_check.js` as `typeScale`.** Up to 600 px wide: title 56, section 44, figure 48, H3 26, H4 20, quote 24, intro 19, ask 19, body 17, body small 15, UI 15, caption 14, label 13, data label 13. From 1,200 px wide: title 110, section 80, figure 104, H3 32, H4 24, quote 32, intro 22, and the rest unchanged. Between 601 and 1,199 px, either set. A specimen with no `width_px` flows with the page, so it may also use each style's fluid size at the width being checked (`font: var(--oa-type-h3)` and the rest). The chart system's own sizes (28 and 22 px titles, 15 px labels, 116 and 88 px big numbers) also pass. Any other size needs `"scale"` in `check_exempt`.

**Never inside a specimen (AX-S8):** `<nav>`, `<article>`, `<header>`, `<footer>`, `<main>`, `<aside>`, a named `<section>` or `<form>`, or a landmark role. Draw them with `div`. Checked as `specimenLandmarks`.

**Illustrative (DR-97, C-S8).** One form only: `<span class="illus">Illustrative</span>`. The shell styles it everywhere, specimens included, and it never stretches inside a flex or grid parent. Do not restyle it in your `<style>`. One label at the head of a piece in which everything is invented; a label beside each item only where real and invented items mix.

### Chapter key `groups` (chapter JSON)

```
"groups": [
  { "before_rule": "02.1", "number": 1, "title": "Sound like a person talking",
    "line": "Write the sentence you would say across a kitchen table, with the actor up front." },
  { "before_rule": "02.5", "number": 2, "title": "Put the point first and stop", "line": "..." }
]
```

Each group opens before the rule `before_rule` names and runs to the next group. Rules keep their IDs and stay h3. The shell prints two things:

1. A rule-group block before the group's first rule, outside any mat: a hairline, the number and title in the H4 style, and the line in the intro style. It is page text, not a heading, so the heading rule holds (map section 5).

```html
<div class="rule-group" id="group-02-1" data-group="1">
  <p class="rg-head"><span class="rg-n">1</span> <span class="rg-t">Sound like a person talking</span></p>
  <p class="rg-line">Write the sentence you would say across a kitchen table, with the actor up front.</p>
</div>
```

2. A rule index right after the chapter's intro, as page text: each group's number and title (a link to its block), then its rules as links.

```html
<div class="rule-index">
  <p class="label" id="voice-index-t">Rules in this chapter, by group</p>
  <ol class="ri-groups" aria-labelledby="voice-index-t">
    <li><a class="ri-g" href="#group-02-1"><span class="rg-n">1</span> Sound like a person talking</a>
      <ul class="ri-rules"><li><a href="#rule-02-1"><span class="toc-rid">02.1</span> Write it the way you would say it.</a></li> ...</ul></li>
  </ol>
</div>
```

In a chapter with groups, the "In this chapter" list lists rules under their group titles. A group anchor takes focus when a link lands on it. The build warns when `before_rule` names no rule in the chapter, when the first group does not start at the first rule, or when numbers skip. Chapter 02's old index and group-opener specimens (`s-02-index`, `s-02-group-1` to `s-02-group-5`) are no longer needed once `groups` is in the file.

### Strings the shell now writes

- "Coming later" wherever a chapter is not in this page (was "later stage").
- Every Files list ends: "Download buttons arrive with the asset package. Until then, ask the editor for any file listed here." (D2-252)
- The appendix is "Wordmark width proofs". The shell writes no decision code, "Phase", "Gate", "stage board" or "the studio" anywhere (D2-253); `guide_check.js` now fails those words and codes in every reader string, alt text included, as `codes`. Keep codes in manifests (`notes`) and in your handoff notes.
- An accessible name that holds an entity such as `&amp;` fails as `nameEntities`. Write `alt="Oath &amp; Action"` or `alt="Oath & Action"`; the build now decodes entities once in both cases. In chapter JSON, `&amp;` and `&minus;` print as `&` and `&minus;` once, and anything inside `<code>` prints as written, tags included.

### Preview

As before: `python3 -I work/build/scripts/phase-2/guide_build.py`, then open `work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html`. Then `node work/build/scripts/phase-2/guide_check.js work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html --quick` for the rendered checks at 1440 and 390 px. The new checks report each failure with its specimen id.

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
| `rules[].files` | repository paths, shown as code that breaks only at a slash. A path that does not exist is a warning. The chapter's Specifications closer ends "Download buttons arrive with the asset package. Until then, ask the editor for any file listed here." (D2-252) |
| `rules[].related` | chapter numbers, shown as links under "Related chapters" inside the rule. A chapter not in this page shows its number and name with "Coming later", never a dead link |
| `extras[]` | `{ "after_rule": "05.3", "specimen": "...", "caption": "...", "label": "optional label" }`. Leave `after_rule` out to place the extra above the first rule |
| `sources[]` | a numbered "Sources" list at the end of the chapter, before the closers |
| `groups[]` (optional) | rule groups, with a group block before each group's first rule and a rule index after the intro (section 0) |
| `related_chapters[]` (optional) | `{ "chapter": "06", "reason": "Which sizes count as large text." }` for the chapter's own "Related chapters" closer. Without it the shell uses the map's section 10 list with short reasons, plus any chapter a rule cites |

**Inline text.** Every string is escaped, then these inline tags are kept: `<em> <strong> <code> <abbr title> <q> <cite> <sup> <sub> <br> <span class="..."> <a href="#..."> <a href="https://...">`. Anything else shows as text. The shell links each "Rule 05.2" it finds to `#rule-05-2` when that rule is in the page, and each "chapter 06" to `#type`, so you rarely need an `<a>`. Use `<span class="illus">Illustrative</span>` for an inline Illustrative label.

## 4. The block markup the shell renders (for makers)

You never write this markup; it is here so you know what your fields become, and what the checks look for. A chapter:

```html
<section class="chapter" id="color" data-track="chapter" data-part="foundations" data-label="05 Color" data-chapter="05">
  <div class="ch-head">
    <p class="loc-line"><a href="#part-foundations">Foundations</a> · Chapter 05 of 28</p>
    <h2 class="ch-title" id="color-h"><span class="n">05</span> <span class="t">Color</span></h2>
    <p class="return" hidden></p>                                     "Return to ..." lands here after a cross-reference
    <p class="instr">Choose a surface first, then the text and graphic colors that pass on it.</p>
    <p class="intro">...</p>
    <div class="rule-index">...</div>                                  only in a chapter with "groups"
  </div>
  <div class="local-toc">In this chapter: every rule (under its group title, if any), then the three closers</div>
  <div class="ch-body">
    rule groups, rules and extras, then Sources, then three closers:
    <div class="closer" id="color-specs"><h3>Specifications</h3> every token the chapter names, with its value and links to the rules
      that use it ("Rule 05.1"); every file; the D2-252 line</div>
    <div class="closer" id="color-related"><h3>Related chapters</h3> two to five chapters, each with its reason</div>
    <div class="closer" id="color-builders"><h3>For builders</h3> a line on tokens.css; "Download tokens.css" and "Copy this chapter's
      CSS"; the CSS block: every custom property the chapter names with every property it depends on (type parts and their clamps
      included), then the four surface classes, as tokens.css holds them (RP-M3)</div>
  </div>
  <div class="chapnav">Previous, Next, Back to contents</div>
</section>
```

One rule, in the Master Brief section 7 order. The h3 starts with the Rule ID and the rule block owns the matching anchor (map section 4). Everything after the h3 is a visible label, not a heading (map section 5):

```html
<div class="rule" id="rule-05-2" data-rule="05.2">
  <h3 class="rule-h"><span class="rid"><span class="rid-w">Rule</span> <span class="rid-n">05.2</span></span> <span class="rt">Text sits only on pairs that pass.</span></h3>
  <p class="return" hidden></p>
  <div class="rule-body">
    <p class="rule-text">the rule</p>
    <div class="tokens"><p class="label">Tokens</p><ul class="tok-list">chips</ul></div>
    <div class="why"><p class="label">Why it works</p><p class="basis">Basis WCAG 2.2 SC 1.4.3</p><p>...</p></div>
  </div>
  <div class="hinge" aria-hidden="true"><span class="hinge-line"></span>ampersand B<span class="hinge-line"></span></div>
  <figure class="plate plate--correct">Correct application</figure>
  <figure class="plate plate--failure">Failure case</figure>
  <figure class="plate plate--corrective">Corrective example (only when the rule has one)</figure>
  <div class="rule-foot">
    <div class="foot-block foot-specs"><p class="label">Specifications</p><dl class="spec-list">label, value, token</dl> Files</div>
    <div class="foot-pair">
      <div class="foot-block foot-related"><p class="label">Related chapters</p>links</div>
      <div class="foot-block foot-builders"><p class="label">For builders</p>note</div>
    </div>
  </div>
</div>
```

From 48em the Rule ID hangs in its own column: the number sits on the title's first baseline at the H3 size, and the word "Rule" hangs above it in the rule's top space, so every title sits 24 px above its text whatever its length (C-M4). Under 48em "Rule 05.2" sits in the label style above the title.

The hinge divider is the shell's, drawn as DR-96 sets it: ampersand B's 24 px master (`work/build/assets/identity/ampersand/20261028_Amp-B-24px-Master.svg`) at 24 px, centered on a 1 px line as wide as the text block it divides, with 12 px of clear line on each side of B, all in the surface's ink, `--oa-color-identity-hinge-divider` (D1-22, D1-26). In the shell the line spans the rule's text column. Draw the same geometry when a specimen shows the divider; do not draw it in a specimen only to separate blocks.

## 5. How a specimen fragment is framed (for makers)

Your file `work/build/guide/specimens/s-05-2-correct.html` is a fragment: markup and, if you need one, a `<style>` block. No `<html>`, `<head>` or `<body>`, and no `<h1>` to `<h6>` (styled text only). The shell puts it on a plate:

```html
<figure class="plate plate--correct" id="fig-s-05-2-correct">
  <div class="plate-head">
    <p class="plate-label"><span aria-hidden="true">✓</span>Correct application</p>
    <p class="plate-size">True size, 640 px wide</p>                  or "One quarter size" with "scale": 0.25
    [the True size / Fit to window switch, with "fit_switch": true]
    <p class="plate-hint" hidden>Wider than this screen. Scroll the frame sideways to see all of it.</p>
  </div>
  <div class="plate-scroll" data-plate-scroll data-frame-name="Correct application, Rule 05.2">   the mat
    <div class="plate-stage oa-surface-newsprint" data-specimen="s-05-2-correct" data-red="specimen"
         style="--w:640px" data-width="640" data-surface="newsprint" role="img" aria-label="(your manifest alt)">
      YOUR FRAGMENT
    </div>
  </div>
  <figcaption class="plate-cap"><span class="illus">Illustrative</span> your caption</figcaption>
</figure>
```

What the frame does for you, so the specimen does not have to:

- **True size.** The stage is exactly `width_px` wide. Set your own height. A specimen wider than the screen keeps its size: the mat scrolls sideways, becomes a keyboard-scrollable group named for its plate ("Correct application, Rule 05.2, at true size"), and the plate head says it scrolls. Nothing is scaled, unless the manifest asks for `scale` or the reader picks Fit to window. A 1 px Stone keyline marks the stage's edge (AX-S13), and the stage keeps its colors when the system forces its own (AX-S6).
- **Surface.** The stage takes the token surface class for your manifest's `surface` (`newsprint` by default, or `white`, `charcoal`, `prussian`). That class sets the background and the short role names, so inside the specimen `var(--oa-color-text-primary)`, `var(--oa-color-border-hairline)`, `var(--oa-color-focus-ring)` and the rest already point at that surface's values. Long names (`--oa-color-text-primary-on-newsprint`) work too.
- **Alt text.** The stage is `role="img"` named by your manifest's `alt`, so a screen reader hears one full description. A static table or list sets `"readable": true`; a specimen with controls sets `"interactive": true`. Either way the stage becomes a group named for its plate and rule, its structure and controls stay reachable, and the alt is its description, held in a hidden paragraph that assistive technology hears only through the group (section 0).
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
| `readable`, `interactive` | a static table or list, or a specimen with controls (section 0) |
| `scale`, `fit_switch` | a drawing at reduced scale, or a wide comparison frame (section 0) |
| `check_exempt` | any of `"contrast"`, `"red"`, `"locked"` (a misquoted locked line shown as a failure), `"size"` and `"scale"`. Contrast, red and locked exemptions are for labeled failure cases only, and so is `size` unless the caption says the plate shows a mark or a minimum size at true size. `scale` is for a labeled failure, a historical record or a print piece, with the reason in `notes`. The rendered check skips that test inside the plate and lists every exemption in its results |
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
- Added in the fix pass: `specimenLandmarks` (no landmark or article element inside a stage), `nameEntities` (no accessible name holds an entity such as `&amp;`, and no visible text outside code shows `&amp;`), `typeScale` (every font size in a stage is one D2-254 allows, section 0) and `codes` (no D2-253 code or studio word in reader text, alt text or names). Each failure names its specimens or sections.

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

- **Ground and type.** Newsprint everywhere, Charcoal text, Deep Stone for secondary text. Inter Tight for headings, Inter for reading, from `tokens.css`'s type styles (`--oa-type-section` for chapter titles, `--oa-type-h3` for rules, `--oa-type-intro` for the instruction line and the rule, `--oa-type-label` for labels). The cover shows the display wordmark, the h1 "Brand Guide, Edition 06" (with "Oath & Action" in hidden text), the tagline in `--oa-type-title`, the pillars kept whole, and one line on what the guide is for. Lora Italic is left to the chapters' quoted lines.
- **The grid (C-S1).** The page sits on Rule 07.2's columns with the grid tokens' margins and gutters: 16 or 20 px margins on phones, 32 at 768, 40 at 1024 and 64 from 1440. From 1024 the rail takes columns 1 to 3 (1 to 2 from 1440). At 1440 the Rule ID sits in column 3, text in columns 4 to 8, plates in 3 to 10 and "In this chapter" in 11 and 12; at 1024 the ID takes columns 4 and 5 and text 6 to 12; at 768 the ID takes 1 and 2 and text 3 to 8.
- **Navigation, as the Gate 1 wireframes draw it.** A sticky masthead with the wordmark from its 24 px master (the 16 px master only under 360 px), "Brand Guide Edition 06" from 768 px, and the part links from 1024 px. Under 1024 px a second line under the bar names where the reader is in full, such as "04 The Ampersand and the hinge" (AX-S7), and a Menu button opens a modal dialog with one navigation block. A chapter rail on the left from 1024 px, with the current chapter on a White band with a 4 px Charcoal bar. "In this chapter" in a right column from 1440 px, its top rule level with the chapter head's, and above the first rule below that (a chapter with groups shows its rule index there instead). Location line over every h2. "Return to ..." appears right after the heading a cross-reference lands on, and focus moves to that heading, or to the target itself when it holds none.
- **Landmarks.** One banner (masthead), one navigation block for parts and one for chapters, main, one contentinfo (the colophon). The phone menu holds a single navigation block. Chapters are sections with headings and no region names.
- **Part opener.** A Charcoal panel, the part's one dark beat (Rule 05.1), with each chapter and its instruction line read from the chapter file. The pillar mark that marks each part comes with the pillar marks chapter; the page says nothing about it until then.
- **Appendix.** From 1440 px the appendix spans all twelve columns and slides over the rail, which the script hides once the appendix reaches it; its mat is 24 px, so a proof stage has 1,264 px at true size (C-M6, D2-251).
- **Anchors.** Chapter anchors are words (`#color`). V5's `#grid` sits at the top of `#signal-grid`. Rules are `#rule-05-2`; closers are `#color-specs`, `#color-related`, `#color-builders`.
- **Tokens.** `tokens.css` is inlined into the page. If it is missing, the build writes a provisional block from the Phase 1 schema draft and says so on the page.

## 8. Engineer's report

### What I built

- `guide_build.py`: reads every chapter JSON, specimen and manifest, validates them, and writes one page with `tokens.css` inlined, the identity masters inline and every specimen asset as a data URI. It builds with no chapter files (eight placeholders), some or all, and a malformed file becomes a placeholder with a warning. Warnings go to the console and to the build report beside the page.
- The shell (`work/build/guide/shell/guide-shell.css`, `guide-shell.js`): cover, contents, the Foundations part opener, chapters in the section 7 template, the hinge divider, plates, rule foot, chapter closers, chapter navigation, the proofs appendix, the colophon, the masthead, rail, local contents and phone menu.
- `guide_check.js`: the rendered check for guide pages, with a self-test that plants faults (section 6). The demo fixtures it builds from are in `work/build/guide/shell/fixtures/`.

### Routine calls, as proposed decision lines

- D2-xxx | Inside each rule, "Specifications", "Related chapters" and "For builders" are labels, as the Stage A brief lists them. Each chapter also ends with the map's three h3 closers, written as indexes: Specifications lists every token the chapter names with its value and the rules that use it, plus every file; Related chapters gives the map's section 10 list with a reason for each; For builders gives the chapter's custom properties as one CSS block with a Copy button | The brief puts the content per rule and the heading rule keeps three closers per chapter; indexes serve both without repeating prose
- D2-xxx | A link to a chapter the page does not hold yet shows its number and name with "later stage", as text | Every link on the page resolves, and the reader still sees where the topic lives
- D2-xxx | The contents lists all 28 chapters, with later ones as text under "Later stages". The rail, part links and phone menu list only what the page holds. "Where to start" waits for the Gate 2 preview build | Its three routes point at chapters 13, 26, 27 and 28, which are not built
- D2-xxx | The hinge divider is drawn whole in `--oa-color-identity-hinge-divider`, line and ampersand alike, with ampersand B's 24 px master at its true size. It sits after "Why it works" and before "Correct application", with the ampersand on the edge of the text column | One device in one ink (D1-22, D1-26); the rule and its reason are the commitment, the specimen what it produces
- D2-xxx | Each part opener is a Charcoal panel | The part's one dark beat (Rule 05.1); it marks the turn without the pillar mark, which waits for board B (DR-88)
- D2-xxx | Rules hang their ID in a left column from 768 px: "Rule" over "05.2" in the h3 style, the rule's title beside it | The Rule ID is how readers cite a rule, so it reads first and lines up down the page
- D2-xxx | Specimens sit at true size on a mat of `--oa-color-tint-stone-n90`, a deeper Newsprint, and never scale. A specimen wider than the screen scrolls inside its frame, which then becomes a named keyboard region with a line saying so | The creative director asked for generous true-size frames; the mat shows a Newsprint specimen's edge without adding White to the page. The tint is a chart token borrowed for the shell
- D2-xxx | A specimen's styles are wrapped in `@scope` to its stage, its ids are prefixed with its specimen id, and repository paths are inlined as data URIs | Four makers' fragments share one page without restyling the shell or each other, and the page stands alone apart from fonts
- D2-xxx | A labeled failure case may skip the contrast, red or locked-line test inside its own plate (`check_exempt` in the manifest), and a true-size mark may skip the 13 px floor. The stage is an image to assistive technology, named by its full alt, and every exemption is listed in the check's results | The Gate 1 board drew failures as images so the page passes its own checks; a failure has to be visible at true size to teach
- D2-xxx | The board loads Inter, Inter Tight and Lora from Google Fonts, as every Phase 2 board does (D2-49). The Gate 2 preview build embeds the OFL font files | Embedding belongs to the single-file build, with the license text
- D2-xxx | The masthead uses the wordmark's 24 px master from 768 px and its 16 px master on phones | Pixel-grid masters at the sizes they were drawn for
- D2-xxx | `guide_check.js` is a new script; `dataviz_check.js` is unchanged | The chart checks stay as they are (brief); guide pages need structure, anchor and exemption logic the chart pages do not
- D2-xxx | Makers install axe-core with `style-dictionary@5.8.0` in the same command, or outside the repository with `AXE_PATH` | With no `package.json` in `work/build`, a lone `npm install --no-save` removes packages installed the same way, including the token build's

### Open questions for Dustin

1. **Failure cases on the page.** A labeled failure case, such as Stone text on Newsprint at 13 px, fails WCAG 1.4.3 where it sits, by design. The shell presents each one as an image with a full description and a caption that names the failure, and the check skips only that plate. *Recommendation:* accept this for the guide, as the Gate 1 board proposed, and keep every correct application and all of the guide's own text passing.
2. **Wide proofs side by side.** At 1440 px the main column is about 1,080 px, so a 1200 by 630 social card at true size scrolls inside its frame, and two cannot sit side by side. *Recommendation:* keep true size and stack the two widths one above the other, as the shell does now. A "fit to this window" switch can come later if you want to compare whole cards at a glance.

### Tested

- `guide_build.py` with no chapter files (eight placeholders), with `--demo`, with a test set (one chapter, `proofs.json`, seven specimens including two 1200 px proofs, inline and data-URI assets), and with malformed files (bad JSON, `rules` as an object, a rule as a string, a bad Rule ID, a missing specimen). It finished every time and named each problem.
- Id prefixing, `@scope` wrapping, asset inlining, escaping of a `<script>` in a JSON string and auto-linking of "Rule 05.2", read back from the built test page.
- `guide_check.js` on the Stage A page as it stands (placeholders only) at 1440, 1024, 390 and 360 px: pass, 0 failures, axe-core 4.10.2.
- `guide_check.js --self-test`: the clean demo passes at 1440 and 390 px, and 25 of 25 planted faults are caught: a second h1, a skipped level, a heading in a specimen, a rule h3 without its ID, a Rule ID from another chapter, a rule anchor that does not match, a stray chapter h3, a duplicate id, a broken same-page link, a Related link that misses a chapter, the `#grid` alias removed, a specimen without alt, an `<img>` without alt, an unnamed SVG, a missing specimen file, 12 px text, low contrast, unmarked red, two working reds in the page, two in one specimen, red on Prussian, an em dash, a near miss of the tagline, pillars out of order, and a wide element outside a frame. Results: `work/boards/phase-2/stage-a/20261106_Guide-Check-Plant-Results.json`. The first run missed red on Prussian (the check read the red block's own fill as its ground); I fixed the check and it now catches it.
- `dataviz_check.js --board` on the demo build: its only failures are the demo's exempt failure plate (12 px gray text), as expected, since that script has no exemptions.
- Ad hoc, on the demo build: 320 px reflow and 200% text size at 1280 px with no page scroll (after fixing long chapter names in links); forced colors (after fixing the rail marker, which every item showed); print media (masthead, rail and menu hidden, a Letter PDF printed); the phone menu by keyboard (Enter opens it, focus lands on the current chapter, Tab never reaches the page behind it, Escape closes it and returns focus to Menu, a link closes it and moves focus to the chapter's h2); `#grid` lands on 08's h2.

### Not tested

- Real chapter content: no chapter or specimen file had landed when I wrote this.
- A screen reader by ear, and browsers other than Chromium. Firefox reads `@scope` only in recent versions; in an older browser a specimen's styles would leak into the page.
- Pages offline: fonts come from Google Fonts.
- Keyboard order past the first 60 Tab stops, touch devices, and a visual review of the printed PDF.

### Change log

Created:
- `work/build/scripts/phase-2/guide_build.py`
- `work/build/scripts/phase-2/guide_check.js`
- `work/build/guide/shell/guide-shell.css`, `work/build/guide/shell/guide-shell.js`
- `work/build/guide/shell/fixtures/demo-chapter.json` and `work/build/guide/shell/fixtures/specimens/` (`manifest-demo.json` and six `s-demo-*.html` fragments)
- `work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html`, `20261106_Stage-A-Chapters-Build-Report.json`, `20261106_Stage-A-Chapters-Guide-Check-Results.json`, `20261106_Guide-Check-Plant-Results.json`, and `captures/`
- `work/handoffs/phase-2/20261106_Guide-Shell-Notes.md` (this file)

Modified: none. Nothing in `work/build/tokens/`, `work/build/tests/tokens/`, `source/`, the ledgers or any existing board was touched.
