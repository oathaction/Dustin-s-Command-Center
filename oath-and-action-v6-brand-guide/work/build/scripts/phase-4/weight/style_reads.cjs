// The check before 3a (DR-331; chat 12b left it open): does any script on the page read a plate's own <style>? 3a drops a plate's
// block where an earlier one carries the same rules, so a script that read the block itself (its text, its sheet, a clone or a
// serialization of something holding it) would read something else afterwards. Two halves, in one Chromium with scripts on:
//
//   1. While the page loads and its scripts run, every read of a style element's sheet, of document.styleSheets, and every
//      textContent, innerText, innerHTML or outerHTML read, cloneNode and XMLSerializer call whose node is a plate's style or
//      holds one, is recorded (an init script wraps those getters before any page script runs).
//   2. After load, each element the page's scripts read on a click or a keystroke (found by reading the scripts: table rows and
//      cells, list items, pre and code, the copy buttons' sources, the status words, the chart kit's art and source line, the
//      tracker's news, headings) is checked for a plate style inside it.
//
//   node style_reads.cjs PAGE.html [OUT.json]
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const SITES = ['tbody tr', 'tr', 'td', 'th', 'li', 'pre', 'code', 'template', 'h3', '.rg-head', '[data-oa-say]', '.oa-copy-value', '.oa-copy-vh',
  '.oa-diagram-name', '.oa-diagram-panel-text', '.oa-stepper-line', '.oa-toggle-label', '.oa-tracker-news > li', '.oac-source', '[data-oa-art]',
  'svg', 'a[data-oa-file]', '[data-oa-panel]', 'script', '[data-pages]', '[data-rows]', '[data-steps]', 'button', 'label', 'summary'];

(async () => {
  const [file, out] = process.argv.slice(2);
  const stamp = () => new Date().toISOString().slice(11, 19) + ' UTC';
  const rec = { page: file, started: stamp() };
  const browser = await chromium.launch();
  try {
    const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
    await ctx.addInitScript(() => {
      const hits = [];
      let calls = 0;
      window.__oaStyleReads = { hits, calls: () => calls };
      const tc = Object.getOwnPropertyDescriptor(Node.prototype, 'textContent');
      const qsa = Element.prototype.querySelectorAll;
      const plate = (n) => n && n.nodeType === 1 && n.localName === 'style' && /^\s*@scope \(\[data-specimen=/.test(tc.get.call(n) || '');
      const holds = (n) => {
        if (!n) return false;
        if (n.nodeType === 9) n = n.documentElement;
        if (!n || (n.nodeType !== 1 && n.nodeType !== 11)) return false;
        if (plate(n)) return true;
        for (const s of qsa.call(n, 'style')) if (plate(s)) return true;
        return false;
      };
      const note = (api, n) => {
        calls++;
        if (hits.length < 200) hits.push({ api, node: n.nodeType === 1 ? n.localName + (n.id ? '#' + n.id : '') + (n.className && typeof n.className === 'string' ? '.' + n.className.trim().split(/\s+/).join('.') : '') : String(n.nodeName) });
      };
      const wrapGet = (proto, prop, api) => {
        const d = Object.getOwnPropertyDescriptor(proto, prop);
        if (!d || !d.get) return;
        Object.defineProperty(proto, prop, { ...d, get() { const v = d.get.call(this); try { if (this && this.nodeType !== 3 && holds(this)) note(api, this); } catch (e) { /* the check never breaks the page */ } return v; } });
      };
      wrapGet(Node.prototype, 'textContent', 'textContent');
      wrapGet(HTMLElement.prototype, 'innerText', 'innerText');
      wrapGet(Element.prototype, 'innerHTML', 'innerHTML');
      wrapGet(Element.prototype, 'outerHTML', 'outerHTML');
      const sheet = Object.getOwnPropertyDescriptor(HTMLStyleElement.prototype, 'sheet');
      Object.defineProperty(HTMLStyleElement.prototype, 'sheet', { ...sheet, get() { try { if (plate(this)) note('sheet', this); } catch (e) { /* */ } return sheet.get.call(this); } });
      const ss = Object.getOwnPropertyDescriptor(Document.prototype, 'styleSheets');
      Object.defineProperty(Document.prototype, 'styleSheets', { ...ss, get() { note('document.styleSheets', this); return ss.get.call(this); } });
      const clone = Node.prototype.cloneNode;
      Node.prototype.cloneNode = function (deep) { try { if (this.nodeType !== 3 && (deep ? holds(this) : plate(this))) note('cloneNode', this); } catch (e) { /* */ } return clone.call(this, deep); };
      const ser = XMLSerializer.prototype.serializeToString;
      XMLSerializer.prototype.serializeToString = function (n) { try { if (holds(n)) note('XMLSerializer', n); } catch (e) { /* */ } return ser.call(this, n); };
    });
    const page = await ctx.newPage();
    const errors = [];
    page.on('pageerror', (e) => errors.push(String(e).slice(0, 200)));
    await page.goto('file://' + path.resolve(file), { waitUntil: 'load', timeout: 300000 });
    await page.waitForTimeout(4000);
    // scroll the page through once, so scripts that wait for a plate to come into view run too
    await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 4000) { window.scrollTo(0, y); await new Promise((r) => requestAnimationFrame(r)); } window.scrollTo(0, 0); });
    await page.waitForTimeout(2000);
    rec.at_load = await page.evaluate(() => ({ reads: window.__oaStyleReads.hits, count: window.__oaStyleReads.calls() }));
    rec.sites = await page.evaluate((sites) => {
      const plate = (n) => n.localName === 'style' && /^\s*@scope \(\[data-specimen=/.test(n.textContent);
      const holds = (n) => plate(n) || [...n.querySelectorAll('style')].some(plate);
      const out = {};
      for (const s of sites) {
        const els = [...document.querySelectorAll(s)];
        out[s] = { elements: els.length, holding_a_plate_style: els.filter(holds).length };
      }
      const targets = [...document.querySelectorAll('[data-copy-from]')].map((b) => document.getElementById(b.getAttribute('data-copy-from'))).filter(Boolean);
      out['[data-copy-from] sources'] = { elements: targets.length, holding_a_plate_style: targets.filter(holds).length };
      out['plate styles on the page'] = { elements: [...document.querySelectorAll('style')].filter(plate).length, holding_a_plate_style: null };
      return out;
    }, SITES);
    rec.page_errors = errors;
    await ctx.close();
  } finally {
    await browser.close();
  }
  rec.ended = stamp();
  rec.reads_found = rec.at_load.count + Object.entries(rec.sites).filter(([k]) => k !== 'plate styles on the page').reduce((a, [, v]) => a + v.holding_a_plate_style, 0);
  console.log(JSON.stringify(rec, null, 1));
  if (out) fs.writeFileSync(out, JSON.stringify(rec, null, 1));
})().catch((e) => { console.error(e); process.exit(2); });
