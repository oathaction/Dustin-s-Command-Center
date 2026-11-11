#!/usr/bin/env node
// Build the Oath & Action token files from the one source.
//
//   node work/build/scripts/phase-2/tokens_build.mjs            build, validate, write
//   node work/build/scripts/phase-2/tokens_build.mjs --check    build in memory and fail if the files on disk differ
//
// Options: --out-dir <dir> (default work/build/tokens), --source <file> (default the source below; used to
// prove the validation gate with a broken copy), --no-validate (skip the rule test), --quiet.
//
// Reads   work/build/tokens/src/oa-tokens.src.mjs
// Writes  work/build/tokens/tokens.json  (DTCG Format Module 2025.10, aliases kept as {path} references)
//         work/build/tokens/tokens.css   (custom properties --oa-..., surface classes, the light and dark themes,
//                                         reduced motion)
//
// Before writing, the build writes both files to a temporary folder and runs the rule test
// (work/build/tests/tokens/test_token_rules.py) on them. A failure stops the build and leaves the
// files on disk as they were (Token Architecture section 7, step 2).
//
// Zero dependencies. The color math (WCAG 2.x contrast, OKLab per Ottosson as in CSS Color 4) is written
// here on its own; the tests carry their own copy in Python, so the two check each other.

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath, pathToFileURL } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '..', '..', '..', '..');
const RULE_TEST = path.join(ROOT, 'work/build/tests/tokens/test_token_rules.py');

const args = process.argv.slice(2);
const flag = (f) => args.includes(f);
const opt = (f, d) => (args.includes(f) ? args[args.indexOf(f) + 1] : d);
const SOURCE = path.resolve(opt('--source', path.join(ROOT, 'work/build/tokens/src/oa-tokens.src.mjs')));
const OUT_DIR = path.resolve(opt('--out-dir', path.join(ROOT, 'work/build/tokens')));
const CHECK = flag('--check');
const VALIDATE = !flag('--no-validate');
const QUIET = flag('--quiet');
const log = (...m) => { if (!QUIET) console.log(...m); };

const src = await import(pathToFileURL(SOURCE).href);
const NS = src.meta.namespace;

// ------------------------------------------------------------------------------------------ color math
const hexToRgb = (h) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16) / 255);
const lin = (c) => (c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4);
const delin = (c) => (c <= 0.0031308 ? 12.92 * c : 1.055 * c ** (1 / 2.4) - 0.055);
const luminance = (h) => { const [r, g, b] = hexToRgb(h).map(lin); return 0.2126 * r + 0.7152 * g + 0.0722 * b; };
function contrast(a, b) {
  const [x, y] = [luminance(a), luminance(b)].sort((p, q) => q - p);
  return (x + 0.05) / (y + 0.05);
}
function toOklab(h) {
  const [r, g, b] = hexToRgb(h).map(lin);
  const l = Math.cbrt(0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b);
  const m = Math.cbrt(0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b);
  const s = Math.cbrt(0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b);
  return [
    0.2104542553 * l + 0.793617785 * m - 0.0040720468 * s,
    1.9779984951 * l - 2.428592205 * m + 0.4505937099 * s,
    0.0259040371 * l + 0.7827717662 * m - 0.808675766 * s,
  ];
}
function fromOklab([L, a, b]) {
  const l = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3;
  const m = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3;
  const s = (L - 0.0894841775 * a - 1.291485548 * b) ** 3;
  const rgb = [
    4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
    -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
    -0.0041960863 * l - 0.7034186147 * m + 1.707614701 * s,
  ];
  return '#' + rgb.map((c) => Math.round(Math.min(1, Math.max(0, delin(Math.min(1, Math.max(0, c))))) * 255)
    .toString(16).padStart(2, '0').toUpperCase()).join('');
}
const mixOklab = (a, b, t) => { const p = toOklab(a); const q = toOklab(b); return fromOklab(p.map((x, i) => x + (q[i] - x) * t)); };

// ------------------------------------------------------------------------------------------ formatting
const fmt = (n) => { const s = Number(Number(n).toFixed(6)).toString(); return s === '-0' ? '0' : s; };
const r2 = (n) => Math.round(n * 100) / 100;
const cssName = (p) => '--' + p.split('.').map((seg) => seg.replace(/([a-z0-9])([A-Z])/g, '$1-$2').toLowerCase()).join('-');
const GENERIC = new Set(['serif', 'sans-serif', 'monospace', 'cursive', 'fantasy', 'system-ui', 'ui-serif', 'ui-sans-serif', 'ui-monospace']);
const cssFamily = (list) => (Array.isArray(list) ? list : [list]).map((f) => (GENERIC.has(f) ? f : `"${f}"`)).join(', ');
const isAlias = (v) => typeof v === 'string' && /^\{[^{}]+\}$/.test(v);
const aliasPath = (v) => v.slice(1, -1);
const SURFACE_OF = { onNewsprint: 'newsprint', onWhite: 'white', onCharcoal: 'charcoal', onPrussian: 'prussian' };
const THRESH = { text: 4.5, largeText: 3, graphic: 3, focus: 3 };
const NAME_BAD = /[{}.]|^\$/;

// ------------------------------------------------------------------------------------------ build the tree
const PALETTE = Object.fromEntries(Object.entries(src.tree.oa.color.palette).map(([k, t]) => [k, t.$value.hex]));
const tokens = new Map();      // path -> DTCG token object (as written)
const order = [];              // token paths in tree order
const errors = [];

function colorValue(hexv) {
  return { colorSpace: 'srgb', components: hexToRgb(hexv).map((c) => Number(c.toFixed(4))), alpha: 1, hex: hexv };
}

function materialize(node, p) {
  const v = node.$value;
  if (isAlias(v)) return v;
  if (v && typeof v === 'object' && v.$kind) {
    switch (v.$kind) {
      case 'ref': return `{${v.path}}`;
      case 'hex': return colorValue(v.hex.toUpperCase());
      case 'mix': {
        if (!(v.base in PALETTE) || !(v.toward in PALETTE)) errors.push(`${p}: a mix must start from and move toward palette colors`);
        node.ext.derivation = {
          method: 'color-mix', space: 'oklab', base: `{oa.color.palette.${v.base}}`, toward: `{oa.color.palette.${v.toward}}`, amount: v.amount,
          css: `color-mix(in oklab, ${PALETTE[v.base]}, ${PALETTE[v.toward]} ${fmt(v.amount * 100)}%)`,
        };
        return colorValue(mixOklab(PALETTE[v.base], PALETTE[v.toward], v.amount));
      }
      case 'dim': return { value: v.value, unit: v.unit };
      case 'remFromPx': return { value: v.px / 16, unit: 'rem' };
      case 'duration': return { value: v.value, unit: v.unit };
      case 'type': {
        const { minPx, maxPx, trackingEm } = v;
        const maxRem = maxPx / 16;
        const minRem = minPx / 16;
        let css = `${fmt(maxRem)}rem`;
        if (minPx !== maxPx) {
          const { minViewportPx: v0, maxViewportPx: v1 } = src.meta.fluidRange;
          const slope = (maxPx - minPx) / (v1 - v0);
          const icpt = minPx - slope * v0;
          css = `clamp(${fmt(minRem)}rem, ${(icpt / 16).toFixed(4)}rem + ${(slope * 100).toFixed(4)}vw, ${fmt(maxRem)}rem)`;
        }
        const { tier, ...rest } = node.ext;
        node.ext = { tier: tier || 'semantic', minFontSize: { value: minRem, unit: 'rem' }, cssFontSize: css, trackingEm, ...rest };
        return {
          fontFamily: `{${v.family}}`, fontSize: { value: maxRem, unit: 'rem' }, fontWeight: `{${v.weight}}`,
          letterSpacing: { value: Number((trackingEm * maxRem).toFixed(5)), unit: 'rem' }, lineHeight: v.lineHeight,
        };
      }
      default: errors.push(`${p}: unknown recipe ${v.$kind}`);
    }
  }
  return v;   // numbers, arrays (fontFamily, cubicBezier), plain values
}

function walk(node, p, outGroup) {
  for (const [k, child] of Object.entries(node)) {
    if (k.startsWith('$')) { outGroup[k] = child; continue; }
    const cp = p ? `${p}.${k}` : k;
    if (NAME_BAD.test(k)) errors.push(`${cp}: name segment "${k}" breaks the DTCG naming rules`);
    if (child && typeof child === 'object' && '$value' in child) {
      const ext = { ...(child.ext || {}) };
      const holder = { $value: child.$value, ext };
      const value = materialize(holder, cp);
      const t = { $type: child.$type, $value: value, $description: child.$description };
      // DTCG 2025.10's $deprecated: a renamed token's old name, kept as an alias for one release (Rule 26.8)
      if (child.$deprecated !== undefined) {
        if (!isAlias(value) || !(typeof child.$deprecated === 'string' && child.$deprecated.trim())) errors.push(`${cp}: a deprecated token is an alias of its new name and says why in $deprecated`);
        t.$deprecated = child.$deprecated;
      }
      tokens.set(cp, { token: t, ext: holder.ext });
      order.push(cp);
      outGroup[k] = t;
    } else if (child && typeof child === 'object') {
      outGroup[k] = {};
      walk(child, cp, outGroup[k]);
    }
  }
}
const out = {};
walk(src.tree, '', out);

// ------------------------------------------------------------------------------------------ resolve and measure
function resolve(p, seen = []) {
  if (seen.includes(p)) { errors.push(`alias cycle: ${[...seen, p].join(' > ')}`); return null; }
  const e = tokens.get(p);
  if (!e) { errors.push(`${seen[seen.length - 1] || '?'} points to missing ${p}`); return null; }
  const v = e.token.$value;
  return isAlias(v) ? resolve(aliasPath(v), [...seen, p]) : { path: p, value: v };
}
const resolveRef = (ref, from) => {
  if (!isAlias(ref)) { errors.push(`${from}: "${ref}" is not a {path} reference`); return null; }
  return resolve(aliasPath(ref), [from]);
};
const hexOf = (ref, from) => { const r = resolveRef(ref, from); return r && r.value && r.value.hex; };

for (const p of order) {
  const { token, ext } = tokens.get(p);
  const r = resolve(p);
  if (!r) continue;
  // alias targets must carry the same type
  if (isAlias(token.$value)) {
    const target = tokens.get(aliasPath(token.$value));
    if (target && target.token.$type !== token.$type) errors.push(`${p}: ${token.$type} token aliases a ${target.token.$type} token`);
  }
  for (const key of ['ground', 'keyline', 'requiresType', 'fallback', 'minSize', 'edge']) if (ext[key]) resolveRef(ext[key], p);
  for (const key of ['groundsAlso', 'textOnIt']) for (const ref of ext[key] || []) resolveRef(ref, p);
  if (token.$type !== 'color') continue;
  const hexv = r.value.hex;
  const last = p.split('.').pop();
  const surface = ext.surface || SURFACE_OF[last];
  if (ext.tier === 'semantic' && surface) {
    const ground = ext.ground ? hexOf(ext.ground, p) : PALETTE[surface];
    if (ext.kind === 'background') {
      ext.contrast = { onSurface: r2(contrast(hexv, PALETTE[surface])) };
      ext.textOnIt = (ext.textOnIt || []);
      ext.textContrast = Object.fromEntries(ext.textOnIt.map((ref) => [aliasPath(ref), r2(contrast(hexOf(ref, p), hexv))]));
      ext.threshold = 4.5;
      // a ground with an edge (the field ground, stage C): the edge holds 3:1 on the surface and on the ground
      if (ext.edge) ext.edgeContrast = { onSurface: r2(contrast(hexOf(ext.edge, p), PALETTE[surface])), onGround: r2(contrast(hexOf(ext.edge, p), hexv)) };
    } else if (ground && hexv) {
      ext.contrast = r2(contrast(hexv, ground));
      ext.threshold = THRESH[ext.kind] ?? null;
      if (ext.groundsAlso) ext.contrastAlso = Object.fromEntries(ext.groundsAlso.map((ref) => [aliasPath(ref), r2(contrast(hexv, hexOf(ref, p)))]));
      if (ext.keyline) ext.keylineContrast = r2(contrast(hexOf(ext.keyline, p), PALETTE[surface]));
    }
  }
  if (ext.tier === 'primitive' && ext.surfaces) {
    if (ext.kind === 'background') {
      ext.textContrast = Object.fromEntries((ext.textOnIt || []).map((ref) => [aliasPath(ref), r2(contrast(hexOf(ref, p), hexv))]));
    } else {
      ext.contrast = Object.fromEntries(ext.surfaces.map((s) => [s, r2(contrast(hexv, PALETTE[s]))]));
    }
  }
}
// opacity composites
for (const p of order) {
  const { ext, token } = tokens.get(p);
  if (!ext.composite) continue;
  const ink = hexOf(ext.composite.ink, p);
  const ground = hexOf(ext.composite.ground, p);
  const a = token.$value;
  const mixed = '#' + hexToRgb(ink).map((c, i) => Math.round((c * a + hexToRgb(ground)[i] * (1 - a)) * 255).toString(16).padStart(2, '0').toUpperCase()).join('');
  ext.composite = { ...ext.composite, hex: mixed, contrastWithGround: r2(contrast(mixed, ground)) };
}
// CSS names must be unique
const seenNames = new Map();
for (const p of order) {
  const n = cssName(p);
  if (seenNames.has(n)) errors.push(`${p}: CSS name ${n} collides with ${seenNames.get(n)}`);
  seenNames.set(n, p);
}
if (errors.length) {
  console.error(`tokens_build: ${errors.length} error(s) in the source`);
  for (const e of errors) console.error('  ' + e);
  process.exit(1);
}

// attach $extensions in a fixed key order
for (const p of order) {
  const { token, ext } = tokens.get(p);
  const clean = Object.fromEntries(Object.entries(ext).filter(([, v]) => v !== undefined));
  if (Object.keys(clean).length) token.$extensions = { [NS]: clean };
}

const json = {
  $description: `${src.meta.title}. Version ${src.meta.version} (${src.meta.status}): ${src.meta.statusNote} Generated from ${src.meta.source} by ${src.meta.generator}; do not edit by hand.`,
  $extensions: {
    [NS]: {
      ...src.meta,
      tokenSetVersion: src.meta.version,
      needs: src.needs,
      held: src.held,
      redRuleId: src.redRule.id,
      redRule: src.redRule.text,
      redRuleSource: src.redRule.source,
      redRulePrecedence: src.redRule.precedence,
      chartRules: src.chartRules,
    },
  },
  ...out,
};

// ------------------------------------------------------------------------------------------ CSS
const decls = [];   // [name, value, comment?]
function cssLiteral(p, t, ext) {
  const v = t.$value;
  switch (t.$type) {
    case 'color': return v.hex;
    case 'dimension': return `${fmt(v.value)}${v.unit}`;
    case 'duration': return `${fmt(v.value)}${v.unit}`;
    case 'number': return ext.css ?? fmt(v);
    case 'fontWeight': return fmt(v);
    case 'fontFamily': return cssFamily(v);
    case 'cubicBezier': return `cubic-bezier(${v.map(fmt).join(', ')})`;
    default: throw new Error(`${p}: no CSS rule for type ${t.$type}`);
  }
}
const TYPE_PARTS = ['font-family', 'font-style', 'font-weight', 'font-size', 'line-height', 'letter-spacing', 'text-transform', 'font-variant-numeric'];
const valueFor = (v, lit) => (isAlias(v) ? `var(${cssName(aliasPath(v))})` : lit());
let lastGroup = '';
for (const p of order) {
  const { token: t, ext } = tokens.get(p);
  const n = cssName(p);
  const segs = p.split('.');
  const group = segs.slice(0, Math.min(3, segs.length - 1)).join('.');
  if (group !== lastGroup) { decls.push([null, null, group]); lastGroup = group; }
  if (t.$type === 'typography') {
    if (isAlias(t.$value)) {
      const tn = cssName(aliasPath(t.$value));
      for (const part of TYPE_PARTS) decls.push([`${n}-${part}`, `var(${tn}-${part})`]);
      decls.push([n, `var(${tn})`]);
    } else {
      const v = t.$value;
      decls.push([`${n}-font-family`, valueFor(v.fontFamily, () => cssFamily(v.fontFamily))]);
      decls.push([`${n}-font-style`, ext.fontStyle || 'normal']);
      decls.push([`${n}-font-weight`, valueFor(v.fontWeight, () => fmt(v.fontWeight))]);
      decls.push([`${n}-font-size`, ext.cssFontSize]);
      decls.push([`${n}-line-height`, fmt(v.lineHeight)]);
      decls.push([`${n}-letter-spacing`, `${fmt(ext.trackingEm)}em`]);
      decls.push([`${n}-text-transform`, ext.textTransform === 'uppercase' ? 'uppercase' : 'none']);
      decls.push([`${n}-font-variant-numeric`, ext.numeric || 'normal']);
      decls.push([n, `var(${n}-font-style) var(${n}-font-weight) var(${n}-font-size)/var(${n}-line-height) var(${n}-font-family)`]);
    }
    continue;
  }
  const dep = t.$deprecated !== undefined && ext.deprecated
    ? `deprecated, renamed ${cssName(aliasPath(ext.deprecated.replacedBy))}, leaves with ${ext.deprecated.removedIn}` : null;
  decls.push([n, valueFor(t.$value, () => cssLiteral(p, t, ext)), null, dep]);
}

// surface classes: short names point at one surface's tokens; a role with no token on a surface is set
// to initial there, so a value from an outer surface can never leak in (red never reaches Prussian).
const bases = [];
for (const p of order) {
  const segs = p.split('.');
  const last = segs.pop();
  if (!(last in SURFACE_OF)) continue;
  const b = segs.join('.');
  if (!bases.includes(b)) bases.push(b);
}
const SCHEME = { newsprint: 'light', white: 'light', charcoal: 'dark', prussian: 'dark' };
const KEY = { newsprint: 'onNewsprint', white: 'onWhite', charcoal: 'onCharcoal', prussian: 'onPrussian' };
// DR-204 (stage C): the short name for the ground itself, so a menu, a dialog or a masthead can paint the surface or
// theme it sits on. It is CSS only, like every short name, and may not collide with a token's own name.
const THEME = src.meta.theme || null;
const SHORT_SURFACE = THEME ? THEME.shortSurface : null;
for (const n of [...bases.map(cssName), ...(SHORT_SURFACE ? [SHORT_SURFACE] : [])]) {
  if (seenNames.has(n)) { console.error(`tokens_build: the short name ${n} collides with the token ${seenNames.get(n)}`); process.exit(1); }
}
// Every declaration a surface (a class or a theme) makes: its ground, its ink, its color scheme, the ground's short
// name, and each short name pointed at this surface's token, or initial where the surface has none.
const surfaceLines = (s, indent) => [
  `background-color: var(${cssName(`oa.color.surface.${s}`)});`,
  `color: var(${cssName(`oa.color.text.primary.${KEY[s]}`)});`,
  `color-scheme: ${SCHEME[s]};`,
  ...(SHORT_SURFACE ? [`${SHORT_SURFACE}: var(${cssName(`oa.color.surface.${s}`)});`] : []),
  ...bases.map((b) => `${cssName(b)}: ${tokens.has(`${b}.${KEY[s]}`) ? `var(${cssName(`${b}.${KEY[s]}`)})` : 'initial'};`),
].map((l) => indent + l);
const surfaceBlocks = src.meta.surfaces.map((s) => {
  const lines = surfaceLines(s, '  ');
  const note = {
    newsprint: 'Newsprint: the default reading surface and the page color for charts and the atlas (DR-53).',
    white: 'White: the bright surface. Chart roles are initial here: charts sit on Newsprint or Charcoal.',
    charcoal: 'Charcoal: the dark ground. Interface roles and chart roles take their Charcoal values (DR-50).',
    prussian: 'Prussian: the depth surface. Every red role is initial here, because red never sits on Prussian (Rule 05.3).',
  }[s];
  return `/* ${note} */\n.oa-surface-${s} {\n${lines.join('\n')}\n}`;
});

// The themes (DR-204, D2-1133). With no attribute the root follows the device; data-oa-theme on the root wins over
// the device; on any other element it sets that element and what it holds. The blocks come after the surface classes,
// so on one element the attribute wins; on the root the theme's selectors outrank a class.
let themeCss = '';
if (THEME) {
  const A = THEME.attribute;
  for (const k of ['light', 'dark']) {
    if (!THEME[k] || !src.meta.surfaces.includes(THEME[k].surface)) { console.error(`tokens_build: the ${k} theme names no known surface`); process.exit(1); }
  }
  const L = THEME.light.surface, Dk = THEME.dark.surface;
  themeCss = `
/* Themes (DR-204): one dark mode for every screen product, drawn from Night Edition on Charcoal (DR-36).
 * With no ${A} attribute, or ${A}="device", the root follows the device: light, or dark under
 * ${THEME.followsDevice}. ${A}="light" or ${A}="dark" on the root wins over the device; the reader's
 * Theme choice (Light, Dark, Match my device) writes it there. On any other element it sets that element and
 * everything inside it. A surface class keeps its own surface in either
 * theme, so a product that follows the theme puts no surface class on its body. A page that must stay light,
 * such as the brand guide, sets ${A}="light" on its root. */

/* Light (${L[0].toUpperCase() + L.slice(1)}): the default, and wherever ${A}="light" stands. */
:root:not([${A}="dark"]),
[${A}="light"] {
${surfaceLines(L, '  ').join('\n')}
}

/* Dark (${Dk[0].toUpperCase() + Dk.slice(1)}): when the device asks for dark and the root does not force light. */
@media ${THEME.followsDevice} {
  :root:not([${A}="light"]) {
${surfaceLines(Dk, '    ').join('\n')}
  }
}

/* Dark (${Dk[0].toUpperCase() + Dk.slice(1)}): wherever ${A}="dark" stands, whatever the device asks. */
[${A}="dark"] {
${surfaceLines(Dk, '  ').join('\n')}
}
`;
}

const durations = order.filter((p) => tokens.get(p).token.$type === 'duration');
const reduced = durations.map((p) => {
  const rv = tokens.get(p).ext.reducedMotionValue;
  return `    ${cssName(p)}: ${fmt(rv.value)}${rv.unit};`;
}).join('\n');

const queries = order.filter((p) => p.startsWith('oa.layout.breakpoint.')).map((p) => {
  const q = tokens.get(p).ext.mediaQuery;
  return ` *   ${p.split('.').pop().padEnd(11)} ${q || '(base layout, no query)'}`;
}).join('\n');

const rootLines = decls.map(([n, v, g, note]) => (n === null ? `\n  /* ${g} */` : `  ${n}: ${v};${note ? ` /* ${note} */` : ''}`)).join('\n');
const css = `/* ${src.meta.title}
 * Version ${src.meta.version} (${src.meta.status}). ${src.meta.statusNote}
 * DTCG Format Module ${src.meta.formatVersion}. Generated from ${src.meta.source}
 * by ${src.meta.generator}. Do not edit by hand: the token tests fail when this
 * file and tokens.json disagree.
 *
 * Naming: ${src.meta.cssNaming}.
 * Surface classes (.oa-surface-newsprint and the rest) point the short names, such as
 * --oa-color-text-secondary, at that surface's tokens.${THEME ? `
 * Themes: the root follows the device, light on Newsprint or dark on Charcoal (DR-204), and
 * ${THEME.attribute}="light" or "dark" on the root wins over the device. See the theme blocks below.` : ''}${src.meta.changeNotes ? `
 * Change in ${src.meta.changeNotes[0].version}: ${src.meta.changeNotes[0].change}` : ''}
 *
 * Media queries cannot read custom properties. Write breakpoints in em, which follows text size:
${queries}
 */

:root {${rootLines}
}

${surfaceBlocks.join('\n\n')}
${themeCss}
/* Reduced motion: every duration resolves to 0 ms and the final state shows at once. */
@media (prefers-reduced-motion: reduce) {
  :root {
${reduced}
  }
}
`;
const jsonText = JSON.stringify(json, null, 2) + '\n';

// ------------------------------------------------------------------------------------------ check, validate, write
const files = { 'tokens.json': jsonText, 'tokens.css': css };
if (CHECK) {
  const stale = Object.entries(files).filter(([f, text]) => {
    const fp = path.join(OUT_DIR, f);
    return !fs.existsSync(fp) || fs.readFileSync(fp, 'utf8') !== text;
  }).map(([f]) => f);
  if (stale.length) {
    console.error(`tokens_build --check: ${stale.join(' and ')} in ${path.relative(ROOT, OUT_DIR) || OUT_DIR} differ from what the source builds. Run the build.`);
    process.exit(1);
  }
  log(`tokens_build --check: tokens.json and tokens.css match the source (${order.length} tokens).`);
  process.exit(0);
}
if (VALIDATE) {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'oa-tokens-'));
  for (const [f, text] of Object.entries(files)) fs.writeFileSync(path.join(tmp, f), text);
  const res = spawnSync('python3', ['-I', RULE_TEST, '--json', path.join(tmp, 'tokens.json'), '--css', path.join(tmp, 'tokens.css'), '--quiet'], { encoding: 'utf8' });
  fs.rmSync(tmp, { recursive: true, force: true });
  if (res.error) { console.error(`tokens_build: could not run the rule test (${res.error.message}). Use --no-validate only for tests.`); process.exit(1); }
  if (res.status !== 0) {
    console.error('tokens_build: the rule test failed, so nothing was written.');
    process.stderr.write(res.stdout + res.stderr);
    process.exit(1);
  }
  log('tokens_build: rule test passed on the new build.');
}
fs.mkdirSync(OUT_DIR, { recursive: true });
for (const [f, text] of Object.entries(files)) fs.writeFileSync(path.join(OUT_DIR, f), text);
log(`tokens_build: wrote ${order.length} tokens to ${path.relative(ROOT, path.join(OUT_DIR, 'tokens.json'))} and ${path.relative(ROOT, path.join(OUT_DIR, 'tokens.css'))} (version ${src.meta.version}).`);
