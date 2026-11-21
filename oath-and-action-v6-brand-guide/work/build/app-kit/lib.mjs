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
import crypto from 'crypto';
import { fileURLToPath } from 'url';

export const KIT = path.dirname(fileURLToPath(import.meta.url));
export const ROOT = path.resolve(KIT, '../../..');
export const TOKENS_CSS = path.join(ROOT, 'work/build/tokens/tokens.css');
export const FONT_MANIFEST = path.join(ROOT, 'work/build/assets/fonts/20261111_Font-Manifest.json');
export const CODE = path.join(ROOT, 'work/build/guide/code');
export const SPECS_TABLE = path.join(ROOT, 'work/research/20261121_Platform-Specifications.json');
export const EXPORTS = path.join(ROOT, 'work/build/exports/phase-4');
export const PLATES = path.join(KIT, 'plates');   // chat 11, contract C4: the plates the guide build places

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
  touch(SPECS_TABLE);
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
.oa-app-plate{display:grid;gap:8px;max-width:100%;margin:0 0 32px}
.oa-app-head{margin:0;font:var(--oa-type-label-font-style) var(--oa-type-label-font-weight) 0.8125rem/1.3 var(--oa-type-label-font-family);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;color:var(--oa-color-text-primary)}
.oa-app-size{margin:0;font:var(--oa-type-caption-font-style) var(--oa-type-caption-font-weight) 0.875rem/1.4 var(--oa-type-caption-font-family);color:var(--oa-color-text-secondary)}
.oa-app-switch{display:inline-flex;align-items:center;gap:8px;min-height:44px;font:var(--oa-type-ui-font-style) var(--oa-type-ui-font-weight) var(--oa-type-ui-font-size)/1.3 var(--oa-type-ui-font-family);color:var(--oa-color-text-primary)}
.oa-app-switch input{width:20px;height:20px;margin:0}
.oa-app-switch input:focus-visible{outline:var(--oa-border-width-focus-ring) solid var(--oa-color-focus-ring);outline-offset:2px}
.oa-app-row{display:flex;flex-wrap:wrap;gap:16px;align-items:flex-start}
.oa-app-frame{border:1px solid var(--oa-color-border-strong);max-width:100%;flex:1 1 320px}
.oa-app-frame.oa-app-feed{flex:0 0 auto;width:min(390px,100%)}
.oa-app-frame svg.oa-app-scale{display:block;width:100%;height:auto}
.oa-app-safe{display:none}
.oa-app-plate:has(.oa-app-switch input:checked) .oa-app-safe{display:inline}
.oa-app-safe .shade{fill:var(--oa-color-text-primary);fill-opacity:.32}
.oa-app-safe .hatch{fill:url(#oa-app-hatch)}
.oa-app-safe .edge{fill:none;stroke:var(--oa-color-text-primary);stroke-dasharray:12 8}
.oa-app-safe .solid{fill:none;stroke:var(--oa-color-text-primary)}
.oa-app-safe .col{fill:var(--oa-color-text-primary);fill-opacity:.08}
.oa-app-safe .chip{fill:var(--oa-color-surface)}
.oa-app-safe text{font-family:var(--oa-type-label-font-family);font-weight:600;letter-spacing:.06em;text-transform:uppercase;fill:var(--oa-color-text-primary)}
`;

// The overlay, in the application's own units (px), from named layers, each drawn as a 2 px dashed edge (scaled with the
// drawing) with its name on a chip in the label style:
//   { x, y, w, h, label, kind: 'edge' (dashed, default) | 'solid' | 'shade' (dims what lies outside the box) | 'hatch'
//     (hatches what lies outside the box) | 'cols' (cols: [[x, w], ...] columns of the box), sw (stroke width, default 2),
//     ls (label size, default 26), lx, ly (label place) }
export function overlay(w, h, layers = []) {
  if (!layers.length) return '';
  const p = [];
  for (const L of layers) {
    const sw = L.sw || 2, ls = L.ls || 26;
    const out = `M0 0H${w}V${h}H0Z M${L.x} ${L.y}V${L.y + L.h}H${L.x + L.w}V${L.y}Z`;
    if (L.kind === 'shade') p.push(`<path class="shade" fill-rule="evenodd" d="${out}"/>`);
    if (L.kind === 'hatch') p.push(`<path class="hatch" fill-rule="evenodd" d="${out}"/>`);
    if (L.kind === 'cols') for (const [cx, cw] of L.cols) p.push(`<rect class="col" x="${cx}" y="${L.y}" width="${cw}" height="${L.h}"/>`);
    // chat 11: a circle (a maskable icon's safe circle): cx, cy, r
    if (L.kind === 'circle') p.push(`<circle class="edge" cx="${L.cx}" cy="${L.cy}" r="${L.r}" stroke-width="${sw}" stroke-dasharray="${6 * sw} ${4 * sw}"/>`);
    if (L.kind !== 'cols' && L.kind !== 'circle') p.push(`<rect class="${L.kind === 'solid' ? 'solid' : 'edge'}" x="${L.x}" y="${L.y}" width="${L.w}" height="${L.h}" stroke-width="${sw}"${L.kind === 'solid' ? '' : ` stroke-dasharray="${6 * sw} ${4 * sw}"`}/>`);
    if (L.label) {
      const tx = L.lx ?? L.x + 8, ty = L.ly ?? L.y + 8, tw = Math.round(L.label.length * ls * 0.68 + ls * 0.8);
      p.push(`<rect class="chip" x="${tx}" y="${ty}" width="${tw}" height="${Math.round(ls * 1.6)}"/><text x="${tx + ls * 0.4}" y="${ty + ls * 1.12}" font-size="${ls}">${esc(L.label)}</text>`);
    }
  }
  const hatch = layers.some((L) => L.kind === 'hatch') ? '<defs><pattern id="oa-app-hatch" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="3" height="8" style="fill:var(--oa-color-text-primary);fill-opacity:.45"/></pattern></defs>' : '';
  return `<g class="oa-app-safe" aria-hidden="true">${hatch}${p.join('')}</g>`;
}

// One frame: the application's markup at true size (w by h px) inside an SVG whose viewBox scales it to the frame's width,
// with the overlay over it in the same coordinates. The markup sits in foreignObject, so its words stay live text.
// page: { id, key, type } makes it a page frame (chat 11, contract C4): a picture of a working page, named by its alt, whose
// markup (headings, links, the switch) is inert and hidden from the accessibility tree, so the guide's outline and Tab order
// never meet it; data-oa-picture keeps its words under the guide check's 13 px floor and contrast test.
export function frame({ w, h, html, alt, layers = [], cls = '', art_attrs = '', page = null }) {
  const pf = page ? ` data-oa-page-frame="${esc(page.id)} ${esc(page.key)}" data-oa-app-type="${esc(page.type)}" data-w="${w}" data-h="${h}"` : '';
  const hide = page ? ' inert aria-hidden="true" data-oa-picture' : '';
  return `<div class="oa-app-frame${cls ? ' ' + cls : ''}"${pf}><svg class="oa-app-scale" viewBox="0 0 ${w} ${h}" role="img" aria-label="${esc(alt)}">`
    + `<foreignObject x="0" y="0" width="${w}" height="${h}"><div xmlns="http://www.w3.org/1999/xhtml" class="oa-app-art"${hide} style="width:${w}px;height:${h}px"${art_attrs}>${html}</div></foreignObject>`
    + overlay(w, h, layers) + `</svg></div>`;
}

// Chat 11 (contract C4): every file the kit reads while it draws an application, so the guide build can tell when a plate is
// older than its inputs. track() starts a record; the kit's modules all read through fs.readFileSync, the chart kit's too.
const READS = { on: null };
const _read = fs.readFileSync;
fs.readFileSync = function (p, ...rest) {
  if (READS.on && (typeof p === 'string' || p instanceof URL)) {
    const abs = path.resolve(p instanceof URL ? fileURLToPath(p) : p);
    if (abs.startsWith(ROOT + path.sep)) READS.on.add(path.relative(ROOT, abs));
  }
  return _read.call(fs, p, ...rest);
};
export function track() { READS.on = new Set(); return READS.on; }
// a file a cached value came from, counted as read by the application being drawn now
export function touch(abs_or_rel) {
  if (!READS.on) return;
  const abs = path.isAbsolute(abs_or_rel) ? abs_or_rel : path.join(ROOT, abs_or_rel);
  if (abs.startsWith(ROOT + path.sep)) READS.on.add(path.relative(ROOT, abs));
}
export function untrack() { const s = READS.on; READS.on = null; return s; }
export function sha256(rel) { return crypto.createHash('sha256').update(_read.call(fs, path.join(ROOT, rel))).digest('hex'); }

// The plate: a head line, the switch (a native checkbox; :has() shows every overlay in the plate, so it works by keyboard
// with scripts off), the frames in a row, and the line under them. css goes in once for the plate.
export function plate({ id, head, line = null, css = '', frames = [], switch_words = 'Show the safe areas' }) {
  const has_overlay = frames.some((f) => f.includes('class="oa-app-safe"'));
  return `<div class="oa-app-plate" data-oa-app="${esc(id)}">`
    + (css ? `<style>${css}</style>` : '')
    + `<p class="oa-app-head">${esc(head)}</p>`
    + (has_overlay ? `<label class="oa-app-switch"><input type="checkbox" name="${esc(id)}-safe">${esc(switch_words)}</label>` : '')
    + `<div class="oa-app-row">${frames.join('')}</div>`
    + (line ? `<p class="oa-app-size">${esc(line)}</p>` : '')
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

// A type style by its token (oa.type.<name>), as the guide's own specimens set one: face, weight, size, line height,
// tracking, case and figures. Pass size to set a size the token does not hold (an artboard or a printed page, where the
// spec names the rule that allows it); lh likewise.
export function type_css(name, { size = null, lh = null, weight = null } = {}) {
  const v = (k) => `var(--oa-type-${name}-${k})`;
  return `font-family:${v('font-family')};font-style:${v('font-style')};font-weight:${weight || v('font-weight')};`
    + `font-size:${size || v('font-size')};line-height:${lh || v('line-height')};letter-spacing:${v('letter-spacing')};`
    + `text-transform:${v('text-transform')};font-variant-numeric:${v('font-variant-numeric')}`;
}

// An identity master inlined from its file, so currentColor and its paint variables (--amp, --link, --lever) take tokens.
// opts: cls, width, height (px), label (role="img" with that name; else aria-hidden), style, red ("signature" or "working")
export function mark(rel, { cls = '', width = null, height = null, label = null, style = '', red = null, attrs = '' } = {}) {
  let s = fs.readFileSync(path.join(ROOT, rel), 'utf8').replace(/<\?xml[^>]*>/, '').replace(/<!--[\s\S]*?-->/g, '');
  s = s.replace(/<title>[\s\S]*?<\/title>|<desc>[\s\S]*?<\/desc>/g, '').trim();
  const a = [label ? `role="img" aria-label="${esc(label)}"` : 'aria-hidden="true"', 'focusable="false"', `data-oa-master="${path.basename(rel, '.svg')}"`];
  if (cls) a.push(`class="${cls}"`);
  if (width != null) a.push(`width="${width}"`);
  if (height != null) a.push(`height="${height}"`);
  if (style) a.push(`style="${style}"`);
  if (red) a.push(`data-red="${red}"`);
  if (attrs) a.push(attrs);
  return s.replace(/<svg\b/, '<svg ' + a.join(' ')).replace(/\s*\n\s*/g, ' ');
}

// The fluid tokens (sizes that follow the window, in vw) restated in cqi, so an application drawn in a frame takes the size
// its own width gives it: inside the frame, 1cqi is one percent of the application's width, as 1vw is of its own window.
// Read from tokens.css at build, so the values stay the tokens' own.
export function fluid_cqi() {
  const out = [];
  const seen = new Set();
  for (const m of tokens_css().matchAll(/(--oa-[a-z0-9-]+)\s*:\s*([^;]*\dvw\b[^;]*);/g)) {
    if (seen.has(m[1])) continue;
    seen.add(m[1]);
    out.push(`${m[1]}:${m[2].replace(/(\d)vw\b/g, '$1cqi')}`);
  }
  return out.join(';');
}

// Every var(--oa-...) a piece of CSS or markup names that tokens.css (or the chart kit's style) does not define
let DEFINED = null;
export function missing_tokens(text, extra = '') {
  if (!DEFINED) DEFINED = new Set([...tokens_css().matchAll(/(--oa-[a-z0-9-]+)\s*:/g)].map((m) => m[1]));
  const local = new Set([...String(extra + text).matchAll(/(--oa-[a-z0-9-]+)\s*:/g)].map((m) => m[1]));
  return [...new Set([...String(text).matchAll(/var\((--oa-[a-z0-9-]+)/g)].map((m) => m[1]))].filter((n) => !DEFINED.has(n) && !local.has(n));
}

// Chat 11 (contract C6): a token's value on the light page, read from tokens.css with every var() resolved, for a file that
// reads no stylesheet (a favicon): token_value('--oa-color-identity-signature-on-white') -> '#E63946'
let TOKVALS = null;
export function token_value(name) {
  if (!TOKVALS) {
    TOKVALS = new Map();
    for (const m of tokens_css().matchAll(/(--oa-[a-z0-9-]+)\s*:\s*([^;]+);/g)) if (!TOKVALS.has(m[1])) TOKVALS.set(m[1], m[2].trim());
  }
  touch(TOKENS_CSS);
  let v = TOKVALS.get(name);
  if (v == null) throw new Error(`tokens.css has no ${name}`);
  for (let i = 0; i < 12 && /var\(/.test(v); i++) v = v.replace(/var\((--oa-[a-z0-9-]+)\)/g, (m, n) => TOKVALS.get(n) ?? m);
  return v;
}

// Chat 11 (step 4, bytes): a guide frame draws each identity master by <use> of one symbol the page carries once, as chat
// 10's C1 carries each photograph once. symbolize(html) finds every inlined master (lib.mark()'s data-oa-master, and chapter
// 18's two wordmark masters by their class), moves its drawing into a <symbol> with the master's viewBox, and leaves the
// <svg> with its own attributes around a <use>. currentColor and the masters' paint variables (--amp, --link, --lever)
// reach a <use> instance by inheritance, so the drawing paints as before; the kit proves each frame's pixels unchanged.
export function symbolize(html) {
  const symbols = {};
  let out = '', i = 0;
  const open = /<svg\b[^>]*?(?:\sdata-oa-master="([^"]+)"|\sclass="oa-masthead-wm oa-masthead-wm--(24|16)")[^>]*>/g;
  let m;
  while ((m = open.exec(html))) {
    const start = m.index;
    // the element's end: count nested <svg> openings and closings
    const re = /<svg\b|<\/svg>/g;
    re.lastIndex = start + 1;
    let depth = 1, mm, end = -1;
    while ((mm = re.exec(html))) { depth += mm[0] === '<svg' ? 1 : -1; if (!depth) { end = mm.index; break; } }
    if (end < 0) break;
    const tag = m[0];
    const inner = html.slice(start + tag.length, end);
    const name = m[1] || `chapter-18-wordmark-${m[2]}px`;
    const id = 'oa-app-id-' + name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
    const vb = (tag.match(/\sviewBox="([^"]+)"/) || [])[1];
    if (!vb) { open.lastIndex = start + 1; continue; }
    const sym = `<symbol id="${id}" viewBox="${vb}">${inner}</symbol>`;
    if (symbols[id] && symbols[id] !== sym) throw new Error(`two drawings named ${id}`);
    symbols[id] = sym;
    // the instance takes the viewBox's own rectangle, since a master's viewBox need not start at 0 (L3's starts at y -12)
    const [vx, vy, vw, vh] = vb.trim().split(/[\s,]+/);
    out += html.slice(i, start) + tag + `<use href="#${id}" x="${vx}" y="${vy}" width="${vw}" height="${vh}"/></svg>`;
    i = end + '</svg>'.length;
    open.lastIndex = i;
  }
  return { html: out + html.slice(i), symbols };
}
export const identity_sprite = (symbols) => `<svg data-oa-app-kit="identity" aria-hidden="true" focusable="false" width="0" height="0" style="position:absolute;width:0;height:0;overflow:hidden">${Object.values(symbols).join('')}</svg>`;
