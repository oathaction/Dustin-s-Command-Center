#!/usr/bin/env node
// Cross-check tokens.json and tokens.css with Style Dictionary, an independent DTCG reader (T-11).
//
//   cd work/build && npm install --no-save style-dictionary     (once; node_modules stays out of git)
//   node work/build/tests/tokens/sd_crosscheck.mjs [--json PATH] [--css PATH]
//
// Style Dictionary parses tokens.json as DTCG, resolves every alias with its own resolver, names each
// token with its own kebab-case transform and writes each value with its own CSS transforms. This script
// then checks, token by token, that Style Dictionary's name is a custom property in tokens.css and that
// its value equals the value tokens.css resolves to. Exit 1 on any disagreement; exit 2 when Style
// Dictionary is not installed.

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '..', '..', '..', '..');
const args = process.argv.slice(2);
const opt = (f, d) => (args.includes(f) ? args[args.indexOf(f) + 1] : d);
const JSON_PATH = path.resolve(opt('--json', path.join(ROOT, 'work/build/tokens/tokens.json')));
const CSS_PATH = path.resolve(opt('--css', path.join(ROOT, 'work/build/tokens/tokens.css')));
const SD_DIR = path.join(ROOT, 'work/build/node_modules/style-dictionary');

if (!fs.existsSync(path.join(SD_DIR, 'package.json'))) {
  console.log('sd-crosscheck: Style Dictionary is not installed in work/build/node_modules; skipped.');
  process.exit(2);
}
const sdVersion = JSON.parse(fs.readFileSync(path.join(SD_DIR, 'package.json'), 'utf8')).version;
const { default: StyleDictionary } = await import(pathToFileURL(path.join(SD_DIR, 'lib/StyleDictionary.js')).href);

// --- read tokens.css :root and resolve var() chains (this script's own reader)
const cssText = fs.readFileSync(CSS_PATH, 'utf8').replace(/\/\*[\s\S]*?\*\//g, '');
const rootBody = cssText.match(/:root\s*\{([\s\S]*?)\n\}/)[1];
const props = new Map();
for (const part of rootBody.split(';')) {
  const i = part.indexOf(':');
  if (i < 0) continue;
  props.set(part.slice(0, i).trim(), part.slice(i + 1).trim().replace(/\s+/g, ' '));
}
function resolveVar(v, seen = []) {
  return v.replace(/var\((--[\w-]+)\)/g, (_, n) => {
    if (seen.includes(n) || !props.has(n)) throw new Error(`cannot resolve ${n}`);
    return resolveVar(props.get(n), [...seen, n]);
  });
}

// --- Style Dictionary's reading
const sd = new StyleDictionary({
  source: [JSON_PATH],
  usesDtcg: true,
  log: { verbosity: 'silent', warnings: 'disabled' },
  platforms: { css: { transformGroup: 'css' } },
});
await sd.hasInitialized;
const dict = await sd.exportPlatform('css');
const sdTokens = [];
(function walk(n) {
  for (const v of Object.values(n)) {
    if (v && typeof v === 'object') {
      if ('$value' in v && Array.isArray(v.path)) sdTokens.push(v); else walk(v);
    }
  }
})(dict);

// --- compare
const num = (s) => Number.parseFloat(s);
const unq = (s) => String(s).replace(/["']/g, '').replace(/\s*,\s*/g, ', ').trim().toLowerCase();
const parseClampMax = (s) => { const m = /clamp\([^,]+,[^,]+,\s*([\d.]+)rem\s*\)/.exec(s); return m ? `${m[1]}rem` : s; };
function same(type, sdValue, ours, token) {
  switch (type) {
    case 'color': return String(sdValue).toLowerCase() === ours.toLowerCase();
    case 'dimension': {
      const a = /^(-?[\d.]+)([a-z%]*)$/.exec(String(sdValue)); const b = /^(-?[\d.]+)([a-z%]*)$/.exec(ours);
      return a && b && a[2] === b[2] && Math.abs(num(a[1]) - num(b[1])) < 1e-6;
    }
    case 'duration': {
      const toMs = (s) => (String(s).endsWith('ms') ? num(s) : num(s) * 1000);
      return Math.abs(toMs(sdValue) - toMs(ours)) < 1e-6;
    }
    case 'number':
      return ours.endsWith('%') ? Math.abs(num(ours) / 100 - Number(sdValue)) < 1e-9 : Math.abs(num(ours) - Number(sdValue)) < 1e-9;
    case 'fontWeight': return Number(sdValue) === num(ours);
    case 'fontFamily': return unq(sdValue) === unq(ours);
    case 'cubicBezier': return String(sdValue).replace(/\s+/g, '') === ours.replace(/\s+/g, '');
    case 'typography': {
      // Style Dictionary writes "weight size/line-height family"; tokens.css adds the style and writes the
      // fluid size as clamp(), whose maximum is the DTCG fontSize.
      const m = /^(\d+) ([\d.]+rem)\/([\d.]+) (.+)$/.exec(String(sdValue));
      const o = /^(normal|italic) (\d+) (\S+(?:\([^)]*\))?)\/([\d.]+) (.+)$/.exec(ours);
      if (!m || !o) return false;
      return m[1] === o[2] && num(m[2]) === num(parseClampMax(o[3])) && num(m[3]) === num(o[4]) && unq(m[4]) === unq(o[5]);
    }
    default: return false;
  }
}

const mismatches = [];
const seenNames = new Set();
const byType = {};
for (const t of sdTokens) {
  const name = `--${t.name}`;
  seenNames.add(name);
  byType[t.$type] = (byType[t.$type] || 0) + 1;
  if (!props.has(name)) { mismatches.push(`${t.path.join('.')}: Style Dictionary names it ${name}, which tokens.css lacks`); continue; }
  let ours;
  try { ours = resolveVar(props.get(name)); } catch (err) { mismatches.push(`${t.path.join('.')}: ${err.message}`); continue; }
  if (!same(t.$type, t.$value, ours, t)) mismatches.push(`${t.path.join('.')}: Style Dictionary gives ${JSON.stringify(t.$value)}, tokens.css resolves to ${ours}`);
}
const typeParts = /-(font-family|font-style|font-weight|font-size|line-height|letter-spacing|text-transform|font-variant-numeric)$/;
const oursOnly = [...props.keys()].filter((n) => !seenNames.has(n));
const unexplained = oursOnly.filter((n) => !(typeParts.test(n) && seenNames.has(n.replace(typeParts, ''))));
for (const n of unexplained) mismatches.push(`${n}: in tokens.css but not among Style Dictionary's tokens`);

console.log(`sd-crosscheck: Style Dictionary ${sdVersion} read ${sdTokens.length} tokens (${Object.entries(byType).map(([k, v]) => `${v} ${k}`).join(', ')}); `
  + `${sdTokens.length - mismatches.length} agree with tokens.css; ${oursOnly.length - unexplained.length} typography part properties are tokens.css's own; ${mismatches.length} disagreements`);
for (const m of mismatches.slice(0, 40)) console.log('  DISAGREE', m);
process.exit(mismatches.length ? 1 : 0);
