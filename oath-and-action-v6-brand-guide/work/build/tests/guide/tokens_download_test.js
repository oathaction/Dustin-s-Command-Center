// The tokens.css download on a built guide page, in Chromium (round 3 fix pass, November 10, 2026; DR-192, D2-964).
//
// Usage: node work/build/tests/guide/tokens_download_test.js <page.html> [--results out.json]
//
// The published page sits in a host whose save call refuses a .css name, so where window.claude reaches the host's
// downloads capability the button saves a zip holding tokens.css; with no host it stays the plain .css link. Each case
// stubs window.claude before the page's own script runs (window.claude carries only use(), as the contract says), clicks
// a chapter's button and the colophon's link as a reader would, and reads what happened: the host's save calls, the
// browser's downloads and the words on every button. A zip handed to the host is opened here and its one file compared
// with work/build/tokens/tokens.css byte for byte. Exit code 1 when any case fails.
const fs = require('fs');
const path = require('path');
const zlib = require('zlib');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '../../../..');
const TOKENS = fs.readFileSync(path.join(ROOT, 'work/build/tokens/tokens.css'));
const CSS_NAME = '20261106_Oath-And-Action-Tokens.css';
const ZIP_NAME = '20261106_Oath-And-Action-Tokens.zip';
const CSS_WORDS = 'Download tokens.css';
const ZIP_WORDS = 'Download tokens.css in a zip file';

// The stub host. mode: 'none' (no window.claude), 'null' (use resolves null), 'never' (use never answers), 'throw'
// (use throws), 'reject' (use rejects), or a save outcome: 'saved', 'declined', 'rate_limited', 'unavailable',
// 'rejected_extension', 'save-throws' (save throws before it returns a promise).
function stub(mode) {
  window.__saves = [];
  window.__rejections = [];
  window.addEventListener('unhandledrejection', (e) => window.__rejections.push(String(e.reason && (e.reason.code || e.reason.message || e.reason))));
  if (mode === 'none') return;
  const b64 = (u8) => { let s = ''; for (let i = 0; i < u8.length; i++) s += String.fromCharCode(u8[i]); return btoa(s); };
  const save = (req) => {
    if (mode === 'save-throws') throw new TypeError('bad request');
    const d = req.data;
    const bytes = d instanceof Uint8Array ? d : d instanceof ArrayBuffer ? new Uint8Array(d) : ArrayBuffer.isView(d) ? new Uint8Array(d.buffer, d.byteOffset, d.byteLength) : null;
    window.__saves.push({ filename: req.filename, kind: Object.prototype.toString.call(d), bytes: bytes ? b64(bytes) : null, keys: Object.keys(req) });
    if (mode === 'saved') return Promise.resolve({ status: 'saved' });
    return Promise.reject({ code: mode, message: 'stub: ' + mode });
  };
  const ns = Object.freeze({ save });
  const use = (name) => {
    if (mode === 'throw') throw new Error('stub: use throws');
    if (mode === 'reject') return Promise.reject(new Error('stub: use rejects'));
    if (mode === 'never') return new Promise(() => {});
    if (mode === 'null' || name !== 'downloads') return Promise.resolve(null);
    return new Promise((res) => setTimeout(() => res(ns), 30));
  };
  Object.defineProperty(window, 'claude', { value: Object.freeze({ use }), configurable: false });
}

// One local file entry from a zip: its name and its inflated bytes, with the CRC checked.
function unzipOne(buf) {
  if (buf.readUInt32LE(0) !== 0x04034b50) throw new Error('no local file header');
  const method = buf.readUInt16LE(8), crc = buf.readUInt32LE(14), size = buf.readUInt32LE(18), raw = buf.readUInt32LE(22);
  const n = buf.readUInt16LE(26), x = buf.readUInt16LE(28);
  const name = buf.slice(30, 30 + n).toString('utf8');
  const data = buf.slice(30 + n + x, 30 + n + x + size);
  const out = method === 8 ? zlib.inflateRawSync(data) : method === 0 ? data : null;
  if (!out) throw new Error('compression method ' + method);
  if (out.length !== raw) throw new Error('size ' + out.length + ' where the header says ' + raw);
  if ((zlib.crc32(out) >>> 0) !== crc) throw new Error('CRC does not match');
  const entries = buf.readUInt16LE(buf.length - 22 + 10);   // end of central directory, no comment
  return { name, bytes: out, entries };
}

async function run(browser, file, mode, opts = {}) {
  const ctx = await browser.newContext({ acceptDownloads: true, viewport: { width: opts.width || 1440, height: 900 } });
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', (e) => errors.push(String(e.message || e)));
  const downloads = [];
  page.on('download', async (d) => { const p = await d.path(); downloads.push({ name: d.suggestedFilename(), bytes: p ? fs.readFileSync(p) : null }); });
  await page.addInitScript(stub, mode);
  await page.goto('file://' + file, { waitUntil: 'load' });
  await page.waitForTimeout(opts.wait || 300);
  const words = () => page.evaluate(() => [...document.querySelectorAll('a[data-oa-download="tokens-download"], #tokens-download')].map((a) => a.textContent));
  const before = await words();
  const clicks = opts.clicks || ['chapter'];
  for (const which of clicks) {
    const sel = which === 'chapter' ? 'a[data-oa-download]' : '#tokens-download';
    const loc = page.locator(sel).first();
    await loc.scrollIntoViewIfNeeded();
    await loc.click();
    await page.waitForTimeout(400);
  }
  const after = await words();
  const saves = await page.evaluate(() => window.__saves);
  const rejections = await page.evaluate(() => window.__rejections);
  const where = await page.evaluate(() => location.hash);
  await ctx.close();
  return { mode, before, after, saves, downloads, errors, rejections, where };
}

const all = (xs, w) => xs.length > 0 && xs.every((x) => x === w);

(async () => {
  const arg = process.argv.slice(2).find((x, i, a) => !x.startsWith('--') && a[i - 1] !== '--results');
  const file = arg ? path.resolve(arg) : '';
  if (!file || !fs.existsSync(file)) { console.error('usage: node tokens_download_test.js <page.html> [--results out.json]'); process.exit(2); }
  const browser = await chromium.launch();
  const cases = [];
  const check = (name, r, tests) => {
    const failed = Object.entries(tests).filter(([, ok]) => !ok).map(([k]) => k);
    if (r.errors.length) failed.push('page errors: ' + r.errors.join(' | '));
    if (r.rejections.length) failed.push('unhandled rejections: ' + r.rejections.join(' | '));
    cases.push({ name, pass: !failed.length, failed, words_before: r.before[0], words_after: r.after[0], buttons: r.before.length, saves: r.saves.map((s) => ({ filename: s.filename, kind: s.kind, bytes: s.bytes ? Buffer.from(s.bytes, 'base64').length : null })), downloads: r.downloads.map((d) => ({ name: d.name, bytes: d.bytes ? d.bytes.length : null })) });
  };
  const cssOk = (d) => d && d.name === CSS_NAME && d.bytes && Buffer.compare(d.bytes, TOKENS) === 0;
  const zipOk = (s) => {
    if (!s || s.filename !== ZIP_NAME || !s.bytes) return false;
    try { const z = unzipOne(Buffer.from(s.bytes, 'base64')); return z.name === 'tokens.css' && z.entries === 1 && Buffer.compare(z.bytes, TOKENS) === 0; } catch (e) { return false; }
  };

  let r = await run(browser, file, 'saved', { clicks: ['chapter', 'colophon'] });
  check('host saves: a chapter button and the colophon link each hand the zip to the host', r, {
    'every button says it gives a zip': all(r.after, ZIP_WORDS), 'the plain words before the host answers': all(r.before, CSS_WORDS) || all(r.before, ZIP_WORDS),
    'two saves, one per click': r.saves.length === 2, 'each save is the zip, holding tokens.css alone, byte for byte': r.saves.every(zipOk),
    'the save carries filename and data only': r.saves.every((s) => s.keys.join() === 'filename,data'), 'no browser download': r.downloads.length === 0, 'the page did not jump to the colophon': r.where === '' });
  r = await run(browser, file, 'declined');
  check('host: the reader declines, and nothing more happens', r, { 'one save offered': r.saves.length === 1 && zipOk(r.saves[0]), 'no browser download': r.downloads.length === 0, 'the buttons still offer the zip': all(r.after, ZIP_WORDS) });
  r = await run(browser, file, 'rate_limited');
  check('host: a prompt is already open (rate_limited), and nothing more happens', r, { 'one save offered': r.saves.length === 1, 'no browser download': r.downloads.length === 0, 'the buttons still offer the zip': all(r.after, ZIP_WORDS) });
  for (const code of ['unavailable', 'rejected_extension', 'capability_removed', 'save-throws']) {
    r = await run(browser, file, code);
    check(`host: save fails with ${code}, so the plain link takes over`, r, { 'the buttons go back to the plain words': all(r.after, CSS_WORDS), 'the plain tokens.css downloads, byte for byte': r.downloads.length === 1 && cssOk(r.downloads[0]) });
  }
  for (const mode of ['null', 'none', 'reject', 'throw']) {
    r = await run(browser, file, mode, { clicks: ['chapter', 'colophon'] });
    const label = { null: 'use("downloads") resolves null', none: 'no window.claude at all', reject: 'use() rejects', throw: 'use() throws' }[mode];
    check(`no host save (${label}): the plain link`, r, { 'every button says tokens.css': all(r.after, CSS_WORDS) && all(r.before, CSS_WORDS), 'no host save': r.saves.length === 0, 'two downloads of tokens.css, byte for byte': r.downloads.length === 2 && r.downloads.every(cssOk) });
  }
  r = await run(browser, file, 'never', { wait: 300 });
  check('the host never answers: the plain link works meanwhile', r, { 'the plain words': all(r.after, CSS_WORDS), 'no host save': r.saves.length === 0, 'tokens.css downloads': r.downloads.length === 1 && cssOk(r.downloads[0]) });
  r = await run(browser, file, 'saved', { width: 390 });
  check('host saves at 390 px', r, { 'the zip words': all(r.after, ZIP_WORDS), 'one zip save': r.saves.length === 1 && zipOk(r.saves[0]), 'no browser download': r.downloads.length === 0 });
  await browser.close();

  const pass = cases.every((c) => c.pass);
  const out = { checked: new Date().toISOString(), page: path.relative(ROOT, file), tokens_css_bytes: TOKENS.length, pass, cases };
  const ri = process.argv.indexOf('--results');
  const outPath = ri > 0 ? path.resolve(process.argv[ri + 1]) : path.join(path.dirname(file), path.basename(file, '.html') + '-Download-Test-Results.json');
  fs.writeFileSync(outPath, JSON.stringify(out, null, 1));
  console.log(`${pass ? 'PASS' : 'FAIL'} tokens download: ${cases.filter((c) => c.pass).length} of ${cases.length} cases`);
  for (const c of cases) console.log(`  ${c.pass ? 'pass' : 'FAIL'}  ${c.name}${c.failed.length ? ': ' + c.failed.join('; ') : ''}`);
  console.log('  results: ' + outPath);
  process.exit(pass ? 0 : 1);
})().catch((e) => { console.error(e); process.exit(1); });
