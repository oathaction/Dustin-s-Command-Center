// Draw every spec with a given copy of the kit and write what it draws, so two copies can be compared byte for byte
// (weight pass, November 11, 2026). A drawing that is the same string renders the same pixels.
//
//   node work/build/chart-kit/tools/kit_snapshot.mjs --out A.json                  the kit's source files
//   node work/build/chart-kit/tools/kit_snapshot.mjs --bundle FILE --out B.json    one script holding the whole kit
//   node work/build/chart-kit/tools/kit_snapshot.mjs --compare A.json B.json       exit 1 when any drawing differs
//   options: --specs DIR (more spec folders, repeatable)
//
// For each spec in work/build/chart-kit/specs/, fixtures/specs/, the chapter 13 plates' .chart.json and any --specs folder,
// it draws at 328, 358, 600, 720 and 1024 px on Newsprint and Charcoal, and writes the figure's HTML (lean table and
// island as the guide places it) beside each drawing's SVG.
import fs from 'fs';
import path from 'path';
import vm from 'vm';
import { createRequire } from 'module';
import { fileURLToPath } from 'url';

const require = createRequire(import.meta.url);
const KIT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const ROOT = path.resolve(KIT, '../../..');
const args = process.argv.slice(2);
const opt = (k) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : null; };

if (args[0] === '--compare') {
  const a = JSON.parse(fs.readFileSync(args[1], 'utf8')), b = JSON.parse(fs.readFileSync(args[2], 'utf8'));
  const keys = new Set([...Object.keys(a), ...Object.keys(b)]);
  let diff = 0;
  for (const k of keys) if (a[k] !== b[k]) { diff++; if (diff <= 10) console.log('DIFFERS ' + k); }
  console.log(`${diff ? 'FAIL' : 'PASS'} ${keys.size} drawings and figures compared, ${diff} differ`);
  process.exit(diff ? 1 : 0);
}

const main = await import(path.join(KIT, 'oa-chart.mjs'));
const C = require(path.join(KIT, 'checks.js'));
const Kmain = globalThis.OAChart;
// the copy under test, in a fresh context
const ctx = vm.createContext({ console });
const code = opt('--bundle') ? [fs.readFileSync(opt('--bundle'), 'utf8')]
  : ['metrics.js', 'kit.js', 'kit-build.js', 'parts.js', 'geo.js'].map((f) => fs.readFileSync(path.join(KIT, f), 'utf8'))
    .concat(fs.readdirSync(path.join(KIT, 'forms')).filter((f) => f.endsWith('.js')).sort().map((f) => fs.readFileSync(path.join(KIT, 'forms', f), 'utf8')));
code.forEach((c) => vm.runInContext(c, ctx));
const K = ctx.OAChart;
K.words = Kmain.words;
K.id_types = Kmain.id_types;

// --only DIR draws one frozen folder of specs alone, so two copies of the kit meet the same specs while makers edit theirs
const dirs = opt('--only') ? [] : [path.join(KIT, 'specs'), path.join(KIT, 'fixtures/specs')];
if (opt('--only')) dirs.push(path.resolve(opt('--only')));
args.forEach((a, i) => { if (a === '--specs') dirs.push(path.resolve(args[i + 1])); });
const files = dirs.flatMap((d) => fs.existsSync(d) ? fs.readdirSync(d).filter((f) => f.endsWith('.json')).map((f) => path.join(d, f)) : [])
  .concat(opt('--only') ? [] : fs.readdirSync(path.join(ROOT, 'work/build/guide/specimens')).filter((f) => f.endsWith('.chart.json')).map((f) => path.join(ROOT, 'work/build/guide/specimens', f)));
const out = {};
for (const f of files.sort()) {
  const spec = JSON.parse(fs.readFileSync(f, 'utf8'));
  let chk;
  try { chk = C.check_spec(Kmain, spec, {}); } catch (e) { continue; }
  if (!chk.rows || !chk.rows.length || !K.forms[spec.form]) continue;
  const rows = JSON.parse(JSON.stringify(chk.rows));
  const extra = JSON.parse(JSON.stringify(main.extra_rows(chk)));
  const cols = chk.datasets.length ? chk.datasets[0].meta.columns : (spec.data || {}).columns || {};
  const tag = path.relative(ROOT, f);
  for (const g of ['newsprint', 'charcoal']) for (const w of [328, 358, 600, 720, 1024]) {
    try {
      const d = K.draw(spec, rows, { width: w, ground: g, tokens: main.TOK[g], extra });
      out[`${tag}|${g}|${w}`] = d.svg;
    } catch (e) { out[`${tag}|${g}|${w}`] = 'ERROR ' + e.message; }
  }
  out[`${tag}|figure`] = K.figure(spec, rows, { id: 'x', lean_table: true, types: cols, guide: true });
}
fs.writeFileSync(opt('--out'), JSON.stringify(out));
console.log(`${Object.keys(out).length} drawings and figures from ${files.length} specs -> ${opt('--out')}`);
