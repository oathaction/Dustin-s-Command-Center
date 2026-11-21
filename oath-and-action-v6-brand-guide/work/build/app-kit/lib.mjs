// The application kit's shared parts (DR-297, chat 10): what every renderer and the command share.
//
// A renderer (renderers/<type>.mjs) turns a content file (specs/<id>.json) into static markup at the application's true
// size, with the guide's own tokens and fonts. This module gives it:
//   tokens_css()          work/build/tokens/tokens.css, the one source of every color, size and space
//   font_css()            the guide's embedded fonts as @font-face data URLs, from the font manifest (for export pages)
//   component_css(name)   chapter 18's own CSS for a component (work/build/guide/code/c-18-<name>.css), reused, never copied
//   platform(id)          a row of the research lead's specifications table (work/research/20261121_Platform-Specifications.json)
//   safe_boxes(row, w, h) the row's safe area as boxes in the application's own pixels
//   plate(...)            the guide's plate for an application: the drawing at true size in a frame that scales it to the
//                         column (an SVG viewBox around the markup), with a safe-area overlay a reader switches on by
//                         keyboard with scripts off (a checkbox and CSS)
//   export_page(...)      a standalone page that holds the drawing at true size, for the PNG and PDF exports
// No part of this module runs on the guide's page: the kit draws at build time into static markup (G3-07).
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

export const KIT = path.dirname(fileURLToPath(import.meta.url));
export const ROOT = path.resolve(KIT, '../../..');
export const TOKENS_CSS = path.join(ROOT, 'work/build/tokens/tokens.css');
export const FONT_MANIFEST = path.join(ROOT, 'work/build/assets/fonts/20261111_Font-Manifest.json');
export const CODE = path.join(ROOT, 'work/build/guide/code');
export const SPECS_TABLE = path.join(ROOT, 'work/research/20261121_Platform-Specifications.json');
export const EXPORTS = path.join(ROOT, 'work/build/exports/phase-4');

export const esc = (s) => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

export function tokens_css() { return fs.readFileSync(TOKENS_CSS, 'utf8'); }

export function font_css() {
  const man = JSON.parse(fs.readFileSync(FONT_MANIFEST, 'utf8'));
  return man.files.map((f) => {
    const w = (f.weights || [400]);
    const weight = w.length > 1 ? `${Math.min(...w)} ${Math.max(...w)}` : String(w[0]);
    const data = fs.readFileSync(path.join(path.dirname(FONT_MANIFEST), f.file)).toString('base64');
    return `@font-face{font-family:"${f.family}";font-style:${f.style || 'normal'};font-weight:${weight};font-display:block;`
      + `src:url(data:font/woff2;base64,${data}) format("woff2");unicode-range:${f.unicode_range}}`;
  }).join('\n');
}

export function component_css(name) {
  const p = path.join(CODE, `c-18-${name}.css`);
  if (!fs.existsSync(p)) throw new Error(`chapter 18 has no component ${name} (${path.relative(ROOT, p)})`);
  return fs.readFileSync(p, 'utf8');
}

let TABLE = null;
export function platform(id) {
  if (!TABLE) TABLE = JSON.parse(fs.readFileSync(SPECS_TABLE, 'utf8'));
  const r = TABLE.rows.find((x) => x.id === id);
  if (!r) throw new Error(`the specifications table has no row ${id} (${path.relative(ROOT, SPECS_TABLE)})`);
  return r;
}

// The row's safe area as boxes, in the application's pixels: { safe: [x, y, w, h] or null, circle: [cx, cy, r] or null }.
// Insets are in the row's unit; a box is centered; a circle's radius is a percent of the shorter side.
export function safe_boxes(row, w, h, px_per_unit = 1) {
  const s = row && row.safe_area;
  if (!s) return { safe: null, circle: null };
  if (s.type === 'box') {
    const bw = s.width * px_per_unit, bh = s.height * px_per_unit;
    return { safe: [(w - bw) / 2, (h - bh) / 2, bw, bh], circle: null };
  }
  if (s.type === 'insets') {
    const t = s.top * px_per_unit, r = s.right * px_per_unit, b = s.bottom * px_per_unit, l = s.left * px_per_unit;
    return { safe: [l, t, w - l - r, h - t - b], circle: null };
  }
  if (s.type === 'circle') return { safe: null, circle: [w / 2, h / 2, Math.min(w, h) * s.radius_pct / 100] };
  return { safe: null, circle: null };
}

export function title_case(s) {
  return String(s).replace(/[^A-Za-z0-9 ]+/g, ' ').trim().split(/\s+/).map((x) => x[0].toUpperCase() + x.slice(1)).join('-');
}
export function today() {
  const d = new Date();
  return `${d.getUTCFullYear()}${String(d.getUTCMonth() + 1).padStart(2, '0')}${String(d.getUTCDate()).padStart(2, '0')}`;
}

// The plate's own style, scoped by class: the frame, the scaled drawing, the switch and the overlay. Colors only by token.
export const PLATE_CSS = `
.oa-app-plate{display:grid;gap:8px;max-width:100%}
.oa-app-switch{display:flex;align-items:center;gap:8px;min-height:44px;font:var(--oa-type-label-font-style) var(--oa-type-label-font-weight) 0.875rem/1.3 var(--oa-type-label-font-family);color:var(--oa-color-text-primary)}
.oa-app-switch input{width:20px;height:20px;margin:0;accent-color:var(--oa-color-action-primary-background, var(--oa-color-text-primary))}
.oa-app-switch input:focus-visible{outline:2px solid var(--oa-color-focus-ring, var(--oa-color-text-primary));outline-offset:2px}
.oa-app-frame{border:1px solid var(--oa-color-border-strong);background:var(--oa-color-surface-white);max-width:100%}
.oa-app-frame svg.oa-app-scale{display:block;width:100%;height:auto}
.oa-app-safe{display:none}
.oa-app-plate:has(.oa-app-switch input:checked) .oa-app-safe{display:inline}
.oa-app-safe .zone{fill:var(--oa-color-signature-red, currentColor);fill-opacity:.28}
.oa-app-safe .line{fill:none;stroke:var(--oa-color-signature-red, currentColor);stroke-width:4;stroke-dasharray:16 10}
.oa-app-safe text{font:600 28px/1 var(--oa-type-label-font-family);fill:var(--oa-color-text-primary);paint-order:stroke;stroke:var(--oa-color-surface-white);stroke-width:6px}
.oa-app-size{margin:0;font:var(--oa-type-caption-font-style) var(--oa-type-caption-font-weight) 0.875rem/1.4 var(--oa-type-caption-font-family);color:var(--oa-color-text-secondary)}
`;

// The overlay: everything outside the safe box shaded, the box's edge dashed, each named zone (a platform's button or
// crop zone) shaded and named. zones: [{ x, y, w, h, label }]
export function overlay(w, h, boxes, zones = []) {
  const parts = [];
  if (boxes.safe) {
    const [x, y, bw, bh] = boxes.safe;
    parts.push(`<path class="zone" fill-rule="evenodd" d="M0 0H${w}V${h}H0Z M${x} ${y}V${y + bh}H${x + bw}V${y}Z"/>`);
    parts.push(`<rect class="line" x="${x}" y="${y}" width="${bw}" height="${bh}"/>`);
  }
  if (boxes.circle) {
    const [cx, cy, r] = boxes.circle;
    parts.push(`<path class="zone" fill-rule="evenodd" d="M0 0H${w}V${h}H0Z M${cx - r} ${cy}a${r} ${r} 0 1 0 ${2 * r} 0a${r} ${r} 0 1 0 ${-2 * r} 0Z"/>`);
    parts.push(`<circle class="line" cx="${cx}" cy="${cy}" r="${r}"/>`);
  }
  for (const z of zones) {
    parts.push(`<rect class="zone" x="${z.x}" y="${z.y}" width="${z.w}" height="${z.h}"/>`);
    if (z.label) parts.push(`<text x="${z.x + 12}" y="${z.y + 36}">${esc(z.label)}</text>`);
  }
  return parts.length ? `<g class="oa-app-safe" aria-hidden="true">${parts.join('')}</g>` : '';
}

// The plate: the application's markup at true size (w by h px) inside an SVG whose viewBox scales it to the frame's width,
// the overlay drawn in the same coordinates over it, and the switch above. id must be unique on a page.
export function plate({ id, w, h, html, css = '', alt, boxes = { safe: null, circle: null }, zones = [], size_line = null, switch_words = 'Show the safe area' }) {
  const ov = overlay(w, h, boxes, zones);
  const sw = ov ? `<label class="oa-app-switch"><input type="checkbox" name="${esc(id)}-safe">${esc(switch_words)}</label>` : '';
  return `<div class="oa-app-plate" data-oa-app="${esc(id)}">`
    + (css ? `<style>${css}</style>` : '')
    + sw
    + `<div class="oa-app-frame"><svg class="oa-app-scale" viewBox="0 0 ${w} ${h}" role="img" aria-label="${esc(alt)}">`
    + `<foreignObject x="0" y="0" width="${w}" height="${h}"><div xmlns="http://www.w3.org/1999/xhtml" class="oa-app-art" style="width:${w}px;height:${h}px">${html}</div></foreignObject>`
    + ov + `</svg></div>`
    + (size_line ? `<p class="oa-app-size">${esc(size_line)}</p>` : '')
    + `</div>`;
}

// A standalone page holding the drawing at true size at the top left, for captures and PDFs. theme: light or dark (the
// guide's data-oa-theme contract). page: { width_in, height_in } prints at that size with no margin.
export function export_page({ title, w, h, html, css = '', theme = 'light', page = null, fonts = true }) {
  const at_page = page ? `@page{size:${page.width_in}in ${page.height_in}in;margin:0}` : '';
  return `<!doctype html>
<html lang="en" data-oa-theme="${theme}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(title)}</title>
<style>${fonts ? font_css() : ''}</style>
<style>${tokens_css()}</style>
<style>${at_page}html,body{margin:0;padding:0}body{background:var(--oa-color-surface-page, var(--oa-color-surface-newsprint))}
.oa-app-art{position:relative;overflow:hidden${w ? `;width:${w}px` : ''}${h ? `;height:${h}px` : ''}}
${css}</style>
</head>
<body><div class="oa-app-art">${html}</div></body>
</html>
`;
}
