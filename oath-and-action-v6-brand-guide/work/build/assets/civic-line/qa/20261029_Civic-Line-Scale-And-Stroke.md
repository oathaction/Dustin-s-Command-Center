# Civic Line scale and line weight

Measured on October 29, 2026 from the 122 black-sheet reference crops. Numbers come from `20261029_Civic-Line-Scale-And-Stroke.json` beside this note.

## Line weight

W = **5.5 source px**. That is the median of the 122 per-icon median stroke widths (5.551 px), rounded to the nearest quarter pixel. In the 128-unit export it becomes **2.6807 units**.

The per-icon medians run from 4.75 to 9.42 px. The middle half sits between 5.35 and 5.75 px, and the standard deviation is 0.45 px.

Each width is read the way the brief asks: twice the distance-transform value at medial-axis points of the ink mask. The mask is taken at 8x (bilinear upsample, a 3 px Gaussian at 8x, then the midpoint threshold), because a 1x mask rounds every width to whole pixels. On 45 synthetic antialiased rings and bars of known width the 8x reading is off by +0.01 px on average and 0.16 px at worst. The 1x reading is off by up to 1.5 px.

Per-sheet medians: sheet 01 5.62 px, sheet 02 5.75 px, sheet 03 6.00 px, sheet 04 5.50 px, sheet 05 5.25 px.

Icons whose own median differs from W by more than 12 percent: CL-069 (6.18 px, +12.5%), CL-070 (6.18 px, +12.5%), CL-071 (6.25 px, +13.6%), CL-072 (6.25 px, +13.6%), R-03 (9.42 px, +71.3%), R-50 (4.75 px, -13.6%). R-03 is drawn entirely as filled seat dots, so its reading is the dot diameter; it has no stroke to measure.

## Scale

s = **0.487395 units per source px**, one value for the whole set. The largest pictogram, R-44, spans 238 source px including stroke, so it fills 116 units and keeps 6 units of clear space on its long side. Every other icon keeps its size relative to it, as on the sheets.

The ten largest extents:

| ID | Extent (px) | Width | Height | Units |
|---|---:|---:|---:|---:|
| R-44 | 238 | 238 | 80 | 116.0 |
| R-47 | 234 | 234 | 97 | 114.05 |
| R-42 | 232 | 232 | 118 | 113.08 |
| R-13 | 227 | 227 | 117 | 110.64 |
| R-46 | 224 | 224 | 112 | 109.18 |
| R-49 | 223 | 223 | 91 | 108.69 |
| R-39 | 221 | 221 | 93 | 107.71 |
| R-36 | 218 | 218 | 111 | 106.25 |
| R-30 | 216 | 216 | 89 | 105.28 |
| R-06 | 215 | 215 | 88 | 104.79 |

The largest extent is within 15 percent of the next one, so no single icon sets the scale on its own.

## What this means at small sizes

The brief's starting estimate was 3 to 4 units of stroke in the 128-unit box. The measured weight at one shared scale comes to 2.68 units, because the widest reform pictograms set the scale and the set keeps their relative sizes. Rendered at 24 px the stroke is 0.50 px wide, at 32 px 0.67 px and at 64 px 1.34 px. The size strips in `sizes/` show the effect. Use below 32 px would need its own optical-size masters; that is a decision for Dustin, outside this tracing pass.

## Placement

Each icon's ink-box centre in its crop maps to (64, 64): X = s * (x - cx) + 64 and Y = s * (y - cy) + 64. The inventory stores cx, cy and the matrix per icon.
