# Civic Line tracing guide

For the tracing agents. You trace your assigned Civic Line icons into vector sources, one file per icon, and build each one until its overlay looks right. The studio engineer built the pipeline and traced two pilots, CL-021 Connect and CL-001 Voting. Their sources in `src/` are working examples.

Paths below are relative to `work/build/`. Run every command from `work/build/scripts/civic-line/` with `python3 -I`.

## What you may touch

- Write only `assets/civic-line/src/<ID>.svg` and `src/<ID>.json` for your own IDs. The build writes that icon's exports and QA files for you.
- Leave the reference crops, masks, inventory, scale file and scripts alone, and leave other tracers' IDs alone.
- Leave `build_all.py` and `verify_set.py` to the main session. They write shared files.

## Fixed numbers

- Line weight W = 5.5 source px for every stroke. The build applies it; you never write a width.
- Scale s = 0.487395 viewBox units per source px, one value for the set. Strokes export at 2.6807 units.
- The build maps each icon's ink-box centre to (64, 64). You draw in crop pixels and never think about the 128 grid.

## The loop

1. `python3 -I new_source.py <ID> --tracer <your-name>`. This writes both source skeletons with the right viewBox and data-id. The SVG comment carries the catalogue's Construction and Red text.
2. Look at `assets/civic-line/qa/ref-zoom/<ID>.png`: black sheet left, red sheet right, 4x, with a grid every 10 crop px. Count heads, seats, pins, rules, dots and arrowheads here.
3. Measure. Boxes are crop px `x0,y0,x1,y1`:
   - `python3 -I fit_ref.py <ID> line 20,66,140,76` fits a straight stroke centreline and gives its end points and angle.
   - `python3 -I fit_ref.py <ID> circle 5,5,80,115` fits a circle centre and radius to one arc.
   - `python3 -I fit_ref.py <ID> extent 80,0,140,60 --red` finds where red starts and stops.
   - `python3 -I fit_ref.py <ID> width ...` reads a local stroke width.
   Put one stroke in a `line` box and one arc in a `circle` box, away from junctions. End points are centreline ends; a round cap adds 2.75 px beyond them.
4. Draw in `src/<ID>.svg`.
5. `python3 -I build_icon.py <ID> --tracer <your-name>`. It prints the metrics and the files to view.
6. View `qa/overlays/<ID>.png`, then `qa/sizes/<ID>.png`. For detail, run `python3 -I zoom_qa.py <ID> diff x0,y0,x1,y1`. The panels are `reference`, `trace`, `overlay`, `diff`, `black` and `red`. Every panel comes out at 4 x `--scale` crop px (12x by default): the overlay panels are already 4x, and the raw `black` and `red` crops get the extra factor of 4. The tool saves to the session scratchpad's `zoom/` folder and prints the path; open it from there. Keep other scratch files there too, never in `scripts/`.
7. Correct, log the correction, build again. Repeat until the overlay and the metrics look right. Then mark the icon reviewed (see Status).

The overlay has four panels. The first is the black reference, the second your red-black trace on the same background. The third shows reference ink in light grey with your edges in blue, and the red masks outlined: reference in red, yours in green. The fourth shows edge differences over 0.5 px, orange where only the reference has an edge and blue where only yours does. `qa/blink/<ID>.gif` alternates reference and trace.

## Coordinates

The viewBox is `0 0 <crop width> <crop height>`. Pixel column i covers x from i to i + 1, so the ref-zoom grid lines sit on pixel edges and a pixel centre sits at i + 0.5. `fit_ref.py`, the inventory and the build all use this convention. The red crop is registered to the black crop at offset (0, 0) for all 122 icons, so the same coordinates serve both.

## Format

```xml
<svg xmlns="http://www.w3.org/2000/svg" data-id="CL-001" viewBox="0 0 159 132">
  <g data-role="base">
    <rect id="front" x="10.38" y="71.26" width="137.62" height="49.75"/>
    <polyline id="lid-left" points="10.38,71.26 37.75,40.9 69.9,40.9"/>
    <polyline id="lid-right" points="118.6,40.9 120.63,40.9 148,71.26"/>
    <line id="ballot-left" x1="56.5" y1="56" x2="96.13" y2="11.37"/>
    <line id="ballot-right-low" x1="99.12" y1="50.05" x2="93.84" y2="56"/>
    <line id="slot" x1="50.25" y1="56" x2="107.63" y2="56"/>
  </g>
  <g data-role="accent">
    <polyline id="ballot-top-right" class="butt" points="94.18,13.57 96.13,11.37 118.74,27.95 99.12,50.05"/>
  </g>
</svg>
```

Rules the build enforces:

- The root carries `xmlns`, `data-id` and the crop viewBox. Only `<defs>`, `<title>`, `<desc>` and `<g data-role>` may sit at the top level. Comments are fine.
- Groups carry `data-role="base"` or `data-role="accent"`. Use as many as the layering needs, in drawing order: later groups paint over earlier ones. Groups do not nest. Base exports in Charcoal in both editions. Accent exports in Pillar Red in red-black and Charcoal in black.
- Elements: `path` (absolute or relative commands, arcs included), `line`, `polyline`, `polygon`, `circle`, `ellipse`, `rect` (with `rx`). No text, images, `use`, transforms, colours or style attributes.
- An element is a stroke by default: width W, round caps, round joins, no fill. Its `class` changes that:

| class | result | use it for |
|---|---|---|
| (none) | stroke W, round caps and joins | almost everything |
| `fill` | filled, no stroke | solid dots, coin tops, doors, filled cells |
| `fill-stroke` | filled and stroked in one colour | filled shapes whose outer corners are rounded like the strokes |
| `miter` | square joins | architectural corners, page corners and parcel edges the sheet shows square |
| `butt` | flat caps | ends the sheet shows flat, and colour splits (below) |

  `miter` and `butt` combine with each other and with `fill-stroke`. They do not combine with `fill`.
- `data-w="<px>"` overrides the width for one element. It needs an `id`, and the corrections log needs an entry naming that id. Use it only where W would change the drawing, such as shutting a gap the sheet keeps open.
- `fill-rule="evenodd"` is allowed on a `fill` or `fill-stroke` path or polygon.

## Layering and colour splits

Check the red sheet at each crossing to see which colour lies on top, and order the groups to match. In CL-021 the black outer arcs cover both crossings, so the accent group comes first and base second.

Where one stroke changes colour along its length, end both pieces at the same point. Give the piece on top `butt` caps so the split is a square cut. Read the split position with `fit_ref.py extent ... --red`. In CL-001 this lifted the red IoU from 0.842 to 0.880. A round cap at a split pushes red 2.75 px past the change.

## Negative space

Cutouts are real holes in the asset: R-35's X, the person in CL-057, the numeral 1 in R-02, R-12's keyhole and R-10's bar. Never paint a background-coloured shape over a line; cut the line instead. Two ways:

- A compound path with two subpaths and `class="fill" fill-rule="evenodd"`: the outer shape, then the hole.
- A mask. Shapes inside `<mask>` are cuts by default; `data-mask="keep"` paints one back. The build sets the mask region to the whole canvas.

```xml
<!-- Illustrative coordinates, not a trace. -->
<defs>
  <mask id="x-cut">
    <line x1="126" y1="77" x2="146" y2="97"/>
    <line x1="146" y1="77" x2="126" y2="97"/>
  </mask>
</defs>
<g data-role="accent">
  <circle class="fill" cx="136" cy="87" r="22" mask="url(#x-cut)"/>
</g>
```

The black edition keeps the same hole. The pipeline test confirms alpha 0 at the cut in both PNG editions.

## Clean-up rules (DR-03)

Dustin: "i want my logos to look exactly like these, but cleaner, more polished" and "clean them up as needed."

- Draw every stroke at W. Several icons measure away from it: CL-069 to CL-072 run 12 to 14 percent heavier, R-50 14 percent lighter, and R-03 is all filled dots. Draw them at W anyway and log it.
- Use a true circle, a straight line, a right angle, equal repeats or a symmetric pair where the drawing plainly means one. Fit first, then decide.
- Keep every feature, count, gap, open contour end and red placement as drawn. Count in the enlarged view; the image settles any doubt in the catalogue text.
- Keep the drawn quirks the brief names: the shield in Paid Leave, the chair in Safe Seats, the open lock in Filibuster Reform, the family in Child Tax Credit, the robot face in Workplace AI.
- Draw geometry from the black sheet and place red from the red sheet. Across the set the two sheets' stroke widths agree to 0.02 px (median), but they differ by sub-pixel shifts. Eight icons fall below 0.90 sheet-to-sheet IoU: CL-037, CL-047, R-04, R-10, R-12, R-16, R-19 and R-21. In those the red sheet's strokes also run about 0.3 px thinner. A difference map of each shows edge fringes only, with no feature missing from either sheet.
- Move geometry only as far as the clean-up needs. Any change that moves an edge by more than 1 px gets a log entry with the measured value and the new one.

## Corrections log

`src/<ID>.json` holds the log:

```json
{
  "id": "CL-021",
  "tracer": "oa-engineer (pilot)",
  "corrections": [
    {"what": "Made both rings true circles with one radius, 49.64 px",
     "why": "DR-03. Circle fits give 49.53 and 49.76 px; the catalogue calls for two equal circles."},
    {"element": "heavy-rule", "what": "data-w 7", "why": "The sheet's rule is twice the weight of its neighbours."}
  ],
  "notes": "What you kept on purpose, and any judgement between the two sheets."
}
```

Each entry needs `what` and `why`. Add `element` when the entry covers a `data-w`. The build copies the log into the status file.

## Metric targets

These targets guide the visual review; they are not pass marks. The two supplied sheets agree with each other at a median IoU of 0.945 (range 0.870 to 0.985), so no trace should be expected to beat that.

| Metric | Target | Pilots |
|---|---|---|
| Best offset (±3 px search) | (0, 0) | (0, 0) and (0, 0) |
| Edge mean | 0.25 px or less where drawn as is; up to about 0.45 px where a logged correction moves edges | CL-001 0.19, CL-021 0.41 |
| Edge p95 | 1.0 px or less | CL-001 0.71, CL-021 1.12 |
| Edge max | 2 px or less, unless a logged correction explains it | CL-001 1.77, CL-021 1.90 |
| Silhouette IoU | 0.92 or more where drawn as is; 0.85 or more with circle or symmetry corrections | CL-001 0.933, CL-021 0.858 |
| Red IoU | 0.85 or more for stroked accents; small dots and short marks score lower, so read their outlines | CL-001 0.880, CL-021 0.834 |
| Ink area ratio, trace over reference | about 0.95 to 1.05; sheet 03 near 0.92 and sheet 05 near 1.05, since W differs from their drawn weight | CL-001 0.986, CL-021 0.943 |
| Bake check IoU at 4x (the main number), pair identity, inside 0 to 128 | 0.999 or more, true, true (automatic) | 1.0000 and 1.0000; true; true |

The bake check renders the baked export back at crop scale and compares it with your crop-space drawing. Read the 4x number. It leaves out pixels within 2 levels of the threshold, because an edge that lands exactly on a half pixel renders at coverage one half and can round either way in two renders of the same geometry. The raw 4x and 1x numbers are still printed, and the 1x one flips at half pixels, so do not nudge geometry to move it. `qa/metrics/<ID>.json` also records the largest pixel difference between the two 4x renders. Across the set it reaches 58 levels of 255 at most, in a handful of isolated pixels on curves; a real shift shows along a whole edge and pulls the 4x IoU down. Since October 29 the exporter writes 4 decimals and fits each arc's radius to keep its centre, so half circles whose ends sit a diameter apart bake cleanly; there is no need to split them.

CL-021's higher numbers come from its logged correction: the sheet's left ring is about 1 px wider than tall, and the trace draws a true circle. A non-zero offset means your drawing has shifted. A ratio far outside the range means a missing part, an extra part or a wrong width. Every number passing does not prove a match: look at corners, crossings, end gaps and the small features the catalogue names.

## Status

The first build sets the state to `traced` and every build counts an iteration. After your visual review:

- `python3 -I build_icon.py <ID> --state reviewed --note "overlay checked; crossings and gaps match"`
- After a reviewer's comments and your fixes: `--state fixed --note "..."`

The status file is `qa/status/<ID>.json`. The main session compiles `qa/20261029_Civic-Line-Completion-Ledger.md` from those files.

## When the build refuses

The build names every problem with its location and exits without writing that icon. The usual causes are a wrong viewBox, a colour or transform attribute, an element outside the list, or a `data-w` missing its log entry.
