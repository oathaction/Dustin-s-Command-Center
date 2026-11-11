// A small, safe minifier for the chart kit's own scripts (weight pass, November 11, 2026). No outside tool: it reads the
// code token by token (strings, template literals, regular expressions and comments kept apart), drops every comment, and
// removes white space, keeping one line break wherever the source had one and the line break could matter to JavaScript's
// automatic semicolons. It renames nothing, so the minified kit runs the same code as the source. The weight pass proves it
// by drawing every spec with the source and with the minified bundle and comparing the results byte for byte
// (tools/kit_snapshot.mjs).
//
//   import { minify } from './minify.mjs';   minify(sourceText) -> text
//   node work/build/chart-kit/tools/minify.mjs FILE...   prints each file's bytes before and after
const ID = /[A-Za-z0-9_$\u0080-￿]/;
const OPS = '+-*/%<>=&|!^~?.';
// After these tokens a "/" starts a regular expression; after anything else it divides
const REGEX_AFTER = new Set(['', '(', ',', '=', ':', '[', '!', '&', '|', '?', '{', '}', ';', '+', '-', '*', '%', '<', '>', '~', '^',
  '&&', '||', '==', '===', '!=', '!==', '<=', '>=', '=>', '+=', '-=', '*=', '/=', 'return', 'typeof', 'case', 'do', 'else', 'in', 'of', 'new',
  'delete', 'void', 'throw', 'instanceof']);
// A line break after these tokens can never end a statement by itself, so it can go
const NO_ASI_AFTER = new Set(['{', '(', '[', ',', ';', ':', '=', '?', '&&', '||', '+', '-', '*', '%', '<', '>', '!', '==', '===', '!=', '!==',
  '<=', '>=', '+=', '-=', '*=', '/=', '=>', '.', '&', '|', '^', '~']);
// A line break before these tokens can go: the token cannot begin a statement on its own
const NO_ASI_BEFORE = new Set([')', ']', '}', ',', ';', ':', '?', '.', '&&', '||', '==', '===', '!=', '!==', '=', '+=', '-=', '*=', '/=']);

function tokens(src) {
  const out = [];   // [kind, text, wsBefore: 0 none, 1 space, 2 newline]
  let i = 0, ws = 0, last = '';
  const n = src.length;
  while (i < n) {
    const c = src[i];
    if (c === ' ' || c === '\t' || c === '\r') { ws = Math.max(ws, 1); i++; continue; }
    if (c === '\n') { ws = 2; i++; continue; }
    if (c === '/' && src[i + 1] === '/') { while (i < n && src[i] !== '\n') i++; ws = Math.max(ws, 1); continue; }
    if (c === '/' && src[i + 1] === '*') {
      const e = src.indexOf('*/', i + 2);
      if (e < 0) throw new Error('minify: an unclosed comment');
      if (src.slice(i, e).includes('\n')) ws = 2; else ws = Math.max(ws, 1);
      i = e + 2;
      continue;
    }
    let j = i, kind;
    if (c === '"' || c === "'") {
      j++;
      while (j < n && src[j] !== c) { if (src[j] === '\\') j++; if (src[j] === '\n') throw new Error('minify: a string runs past its line'); j++; }
      j++; kind = 'str';
    } else if (c === '`') {
      j++;
      while (j < n && src[j] !== '`') { if (src[j] === '\\') j++; j++; }
      j++; kind = 'str';
    } else if (c === '/' && REGEX_AFTER.has(last)) {
      j++;
      let cls = false;
      while (j < n) {
        const d = src[j];
        if (d === '\\') { j += 2; continue; }
        if (d === '\n') throw new Error('minify: a regular expression runs past its line');
        if (cls) { if (d === ']') cls = false; } else if (d === '[') cls = true; else if (d === '/') break;
        j++;
      }
      j++;
      while (j < n && /[a-z]/.test(src[j])) j++;
      kind = 're';
    } else if (ID.test(c)) {
      while (j < n && ID.test(src[j])) j++;
      // a number with a decimal point or exponent stays one token
      if (/[0-9]/.test(c)) { while (j < n && /[0-9.eE]/.test(src[j]) || (j < n && /[+-]/.test(src[j]) && /[eE]/.test(src[j - 1]))) j++; }
      kind = 'id';
    } else {
      // the longest operator that matches
      const three = src.slice(i, i + 4);
      const ops = ['>>>=', '===', '!==', '**=', '<<=', '>>=', '>>>', '...', '&&', '||', '==', '!=', '<=', '>=', '+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=',
        '=>', '++', '--', '<<', '>>', '**', '??', '?.'];
      const op = ops.find(o => three.startsWith(o));
      j = i + (op ? op.length : 1);
      kind = 'op';
    }
    const text = src.slice(i, j);
    out.push([kind, text, ws]);
    last = kind === 'str' || kind === 're' ? 'x' : (kind === 'id' && !REGEX_AFTER.has(text) ? 'x' : text);
    if (kind === 'op' && (text === ')' || text === ']')) last = ')';
    ws = 0;
    i = j;
  }
  return out;
}

export function minify(src) {
  const t = tokens(src);
  let out = '', prev = null;
  for (const [kind, text, ws] of t) {
    if (prev) {
      const a = prev[1], b = text;
      const glue = (ID.test(a[a.length - 1]) && ID.test(b[0])) || (OPS.includes(a[a.length - 1]) && OPS.includes(b[0]))
        || (prev[0] === 're' && ID.test(b[0])) || (a[a.length - 1] === '/' && b[0] === '/');
      if (ws === 2 && !(NO_ASI_AFTER.has(a) || NO_ASI_BEFORE.has(b))) out += '\n';
      else if (ws && glue) out += ' ';
      else if (!ws && glue) out += ' ';
    }
    out += text;
    prev = [kind, text];
  }
  return out + '\n';
}

import { fileURLToPath } from 'url';
import fs from 'fs';
if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  for (const f of process.argv.slice(2)) {
    const s = fs.readFileSync(f, 'utf8'), m = minify(s);
    console.log(`${f}: ${s.length} -> ${m.length}`);
  }
}
