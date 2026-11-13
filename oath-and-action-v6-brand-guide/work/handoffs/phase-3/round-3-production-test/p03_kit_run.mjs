// Production test 1 (simulated designer, round 3). The kit's command reads data only from work/build/data and has no
// option for another folder, so this runs the kit's own exported run_spec with data_dir pointed at a scratch folder that
// links every frozen file plus the designer's derived file. It prints the faults, writes the CSV the kit would write, the
// SVG drawings, and the plate's bytes measured the way guide_build.py's load-table method builds it.
// usage: node p03_kit_run.mjs SPEC.json DATA_DIR OUT_DIR
import fs from 'fs';
import path from 'path';
import { run_spec, island_table, GUIDE_NOTE_FAULTS } from '/home/user/Dustin-s-Command-Center/oath-and-action-v6-brand-guide/work/build/chart-kit/oa-chart.mjs';
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const C = require('/home/user/Dustin-s-Command-Center/oath-and-action-v6-brand-guide/work/build/chart-kit/checks.js');
const K = globalThis.OAChart;
const [specPath, dataDir, outDir] = process.argv.slice(2);
const spec = JSON.parse(fs.readFileSync(specPath, 'utf8'));
fs.mkdirSync(outDir, { recursive: true });
const res = run_spec(spec, { grounds: ['newsprint', 'charcoal'], widths: [1440, 390], data_dir: dataDir, sweep: true, spec_path: specPath });
const out = { faults: res.faults, rows: res.rows ? res.rows.length : 0, drawings: res.drawings.map(d => ({ ground: d.ground, page: d.page, width: d.width, height: d.height, bytes: d.bytes })) };
for (const d of res.drawings) fs.writeFileSync(path.join(outDir, `${spec.id}-${d.ground}-${d.page}.svg`), d.svg);
if (res.rows && res.datasets && res.datasets.length) {
  const cols = Object.keys(res.datasets[0].meta.columns);
  fs.writeFileSync(path.join(outDir, `${spec.id}.csv`), C.to_csv(res.rows, cols));
  out.csv_rows = res.rows.length; out.csv_cols = cols;
  const columns = res.datasets[0].meta.columns;
  // the plate's figure as guide_build.py places an entry (method load-table: words, lean table, compressed island)
  const r390 = run_spec(spec, { grounds: ['newsprint'], widths: [1440, 390], data_dir: dataDir, no_narrow: true, spec_path: specPath });
  let html = K.figure(spec, r390.rows, { id: 'oac-' + spec.id.toLowerCase(), lean_table: true, types: columns, guide: true });
  const isl = island_table(spec, r390.rows, columns, null);
  html = html.slice(0, html.lastIndexOf('</figure>')) + isl + '</figure>';
  fs.writeFileSync(path.join(outDir, `${spec.id}-figure.html`), html);
  out.figure_bytes = Buffer.byteLength(html);
  out.island_bytes = Buffer.byteLength(isl);
}
console.log(JSON.stringify(out, null, 1));
