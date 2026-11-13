#!/usr/bin/env python3
"""Round 4 checks for the cartographer's maps (Phase 3, round 4; D3-1553, DR-261, the data lead's D4-1).

No layout table is derived this round; the script checks, by the chart kit's own draw in Node, what the round's notes and
the specs' notes_internal claim. It writes nothing.

Usage (from the project folder):
  python3 -I work/build/scripts/phase-3/cartographer_round4_derive.py [--check] [--kit DIR] [--specs DIR]

--check (the default and only mode) runs both checks and exits 1 on any fault:

  codes   D3-1553: at the guide's 326 px phone drawing (a 390 px window), S12, S16 and S78 each draw every state's and DC's
          code (51), so no "Not labeled" note prints; and at the 296 px drawing (a 360 px window) each names in its note
          every code it does not draw.
  radii   D4-1, condition 1: S16's code column (labels.column_phone, under 358 px) moves outlines, codes and leaders only.
          At every whole width from 300 to 357 px, S16 drawn as its spec stands and drawn with the column switched off
          (labels.column_under 1, which is today's layout) give every state the same circle radius to 0.01 px, the same
          shade class and the same size key words; and from 358 to 479 px the two drawings are the same SVG.

--kit names another chart kit folder (a scratch mirror) in place of work/build/chart-kit; --specs another specs folder.
The cartographer, November 13, 2026.
"""
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[4]
NODE = r"""
const [kitdir, specsdir] = process.argv.slice(1);
const path = await import('path'); const fs = await import('fs'); const { createRequire } = await import('module');
const M = await import(path.join(kitdir, 'oa-chart.mjs'));
const C = createRequire(path.join(kitdir, 'oa-chart.mjs'))(path.join(kitdir, 'checks.js'));
const K = globalThis.OAChart, G = globalThis.OAChartGeo;
const load = (id) => JSON.parse(fs.readFileSync(path.join(specsdir, id + '.json'), 'utf8'));
const draw = (spec, w) => { const chk = C.check_spec(K, spec, {}); return K.draw(spec, chk.rows, { width: w, ground: 'newsprint', tokens: M.TOK.newsprint, extra: M.extra_rows(chk) }); };
const codes = Object.keys(G.tiles);
const faults = [], log = [];
// codes
for (const id of ['s12', 's16', 's78']) {
  const spec = load(id);
  for (const w of [326, 296]) {
    const d = draw(spec, w), words = d.texts.map(t => t.words);
    const drawn = new Set(words.filter(t => codes.includes(t)));
    const missing = codes.filter(c => !drawn.has(c));
    const note = words.filter(t => /Not labeled|too small for state codes|names every/.test(t || '')).join(' ');
    const all = d.texts.map(t => t.words).join(' ');
    if (w === 326 && missing.length) faults.push(`codes: ${id.toUpperCase()} at 326 px leaves ${missing.join(', ')} uncoded`);
    if (w === 326 && /Not labeled/.test(all)) faults.push(`codes: ${id.toUpperCase()} at 326 px still prints a "Not labeled" note`);
    if (w === 296 && missing.length && !/too small for state codes/.test(all)) {
      const named = missing.filter(c => new RegExp('\\b' + c + '\\b').test(all.slice(all.indexOf('Not labeled'))));
      if (all.indexOf('Not labeled') < 0 || named.length !== missing.length) faults.push(`codes: ${id.toUpperCase()} at 296 px leaves ${missing.join(', ')} uncoded and its note does not name them all`);
    }
    log.push(`${id.toUpperCase()} at ${w} px: ${drawn.size} of ${codes.length} coded${missing.length ? ' (' + missing.join(', ') + ' in the note)' : ''}`);
  }
}
// radii
const s16 = load('s16');
const off = JSON.parse(JSON.stringify(s16)); off.labels = Object.assign({}, off.labels, { column_under: 1 });
let compared = 0, same_svg = 0;
const circles = (d) => { const m = {}; d.marks.filter(x => x.kind === 'circle' && x.data && G.centers[x.data.key]).forEach(x => { m[x.data.key] = { r: x.w / 2, fill: x.fill }; }); return m; };
const keywords = (d) => d.texts.filter(t => /million|Nation|^\d+$/.test(t.words || '')).map(t => t.words).join('|');
for (let w = 300; w <= 479; w++) {
  const a = draw(s16, w), b = draw(off, w);
  if (w >= 358) { if (a.svg !== b.svg) faults.push(`radii: S16 at ${w} px differs from the layout without the column`); else same_svg++; continue; }
  const ca = circles(a), cb = circles(b);
  for (const k of Object.keys(G.centers)) {
    if (!ca[k] || !cb[k]) { faults.push(`radii: S16 at ${w} px draws no circle for ${k}`); continue; }
    if (Math.abs(ca[k].r - cb[k].r) > 0.01) faults.push(`radii: S16 at ${w} px, ${k}: radius ${ca[k].r.toFixed(3)} against ${cb[k].r.toFixed(3)}`);
    if (ca[k].fill !== cb[k].fill) faults.push(`radii: S16 at ${w} px, ${k}: shade ${ca[k].fill} against ${cb[k].fill}`);
    compared++;
  }
  if (keywords(a) !== keywords(b)) faults.push(`radii: S16 at ${w} px, the key's words differ`);
}
log.push(`S16 radii and shades: ${compared} circles compared at 58 widths (300 to 357 px); 358 to 479 px: ${same_svg} of 122 drawings the same SVG`);
console.log(JSON.stringify({ faults, log }));
"""


def main(argv):
    kit = ROOT / "work/build/chart-kit"
    specs = None
    if "--kit" in argv:
        kit = pathlib.Path(argv[argv.index("--kit") + 1]).resolve()
    specs = pathlib.Path(argv[argv.index("--specs") + 1]).resolve() if "--specs" in argv else kit / "specs"
    r = subprocess.run(["node", "--input-type=module", "-e", NODE, str(kit), str(specs)],
                       capture_output=True, text=True, cwd=str(ROOT))
    if r.returncode != 0:
        print(r.stderr[-2000:])
        print("FAIL: the kit did not run")
        return 1
    out = json.loads(r.stdout.strip().splitlines()[-1])
    for line in out["log"]:
        print("  " + line)
    for f in out["faults"]:
        print("  - " + f)
    print(f"{'FAIL' if out['faults'] else 'PASS'}: cartographer round 4 checks, {len(out['faults'])} faults")
    return 1 if out["faults"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
