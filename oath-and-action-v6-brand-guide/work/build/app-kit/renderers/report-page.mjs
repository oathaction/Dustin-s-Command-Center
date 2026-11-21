// Report page renderer (DR-297, chat 10): one page of a research brief on US Letter with its bleed, drawn at 96 px to the
// inch, so the report reader shows it at 816 by 1056 px inside the trim and the PDF prints the same drawing at 8.5 by 11 in.
// Positions are in points from the trim's top left, as work/handoffs/phase-4/20261121_Kit-Sample-Specs.md, section 3, sets
// them; the trim and bleed come from the platform row (print.letter). Sizes are provisional print sizes: chapter 25 sets
// the point scale.
import { esc, mark, platform, type_css } from '../lib.mjs';

export const type = 'report-page';
const LOCK24 = 'work/build/assets/identity/lockmark/20261109_Lockmark-24px-Master-Outline.svg';
const PX = 96;              // px to the inch
const PT = PX / 72;         // px to the point

export function render(spec) {
  const row = platform(spec.platform);
  const bleed = (row.bleed || 0) * 72;                      // pt
  const TW = row.width * 72, TH = row.height * 72;          // the trim, pt (612 by 792)
  const W = Math.round((TW + 2 * bleed) * PT), H = Math.round((TH + 2 * bleed) * PT);   // the sheet, px (840 by 1080)
  const L = 54, R = 558, MAIN = 332, RAIL = 441, RAILW = 117, FOOT = 738;              // pt from the trim's top left
  const at = (x, y) => `left:${bleed + x}pt;top:${bleed + y}pt`;
  const ill = `<span class="rp-ill">${esc(spec.illustrative)}</span>`;
  const css = `
.rp{position:relative;width:${W}px;height:${H}px;overflow:hidden;background:var(--oa-color-surface-newsprint);color:var(--oa-color-text-primary-on-newsprint);font-kerning:normal;font-variant-ligatures:common-ligatures}
.rp p,.rp h1,.rp h2{margin:0}
.rp>*{position:absolute}
.rp-ill{display:inline-block;margin-left:6pt;padding:2px 6px;border:1px solid var(--oa-color-border-strong-on-newsprint);${type_css('label', { size: '10pt', lh: '1.2' })};vertical-align:baseline;color:var(--oa-color-text-primary-on-newsprint)}
.rp-head{${at(L, 36)};width:${R - L}pt;height:18pt;display:flex;align-items:center}
.rp-head svg{display:block;width:18pt;height:18pt;flex:none;color:var(--oa-color-text-primary-on-newsprint);--link:var(--oa-color-palette-stone);--lever:var(--oa-color-identity-signature-on-newsprint)}
.rp-head .lab{margin-left:9pt;${type_css('label', { size: '10pt', lh: '1.2' })}}
.rp-head .rp-ill{margin-left:9pt}
.rp-head .fo{margin-left:auto;font-family:var(--oa-type-caption-font-family);font-weight:400;font-size:10pt;line-height:1.2;font-variant-numeric:tabular-nums}
.rp-rule{${at(L, 66)};width:${R - L}pt;height:0;border-top:0.75pt solid var(--oa-color-border-hairline-on-newsprint)}
.rp-main{${at(L, 114)};width:${MAIN}pt}
.rp-h1{font-family:var(--oa-type-section-font-family);font-weight:800;font-size:36pt;line-height:1.03;letter-spacing:-0.025em;text-wrap:balance}
.rp-h1 .ln{display:block}
.rp-intro{margin-top:18pt !important;${type_css('intro', { size: '14pt', lh: '1.5' })}}
.rp-sec:first-of-type{margin-top:30pt}
.rp-sec+.rp-sec{margin-top:24pt}
.rp-sec h2{font-family:var(--oa-type-h4-font-family);font-weight:var(--oa-type-h4-font-weight);font-size:15pt;line-height:1.15;letter-spacing:-0.005em}
.rp-sec p{margin-top:6pt !important;${type_css('body', { size: '11pt', lh: '1.6' })}}
.rp-rail{${at(RAIL, 114)};width:${RAILW}pt}
.rp-f+.rp-f{margin-top:24pt}
.rp-f{border-top:1.5pt solid var(--oa-color-border-strong-on-newsprint);padding-top:12pt}
.rp-f .n{${type_css('figure', { size: '48pt', lh: '1' })}}
.rp-f .w{margin-top:6pt !important;${type_css('caption', { size: '10pt', lh: '1.5' })};color:var(--oa-color-text-primary-on-newsprint)}
.rp-f .rp-ill{margin:6pt 0 0}
.rp-foot{left:${bleed + L}pt;bottom:${bleed + (TH - FOOT)}pt;width:${R - L}pt;border-top:0.75pt solid var(--oa-color-border-hairline-on-newsprint);padding-top:9pt;display:flex;gap:${RAIL - L - MAIN}pt;${type_css('caption', { size: '10pt', lh: '1.5' })};color:var(--oa-color-text-secondary-on-newsprint)}
.rp-foot .s{width:${MAIN}pt}
.rp-foot .rp-ill{color:var(--oa-color-text-secondary-on-newsprint)}
.rp-foot .se{margin-left:auto;width:${RAILW}pt}
`;
  const html = `<div class="rp" data-oa-application="${esc(spec.id)}" lang="en">`
    + `<div class="rp-head">${mark(LOCK24, { red: 'signature' })}<span class="lab">${esc(spec.section_label)}</span>${ill}<span class="fo">${esc(spec.folio)}</span></div>`
    + `<div class="rp-rule" aria-hidden="true"></div>`
    + `<div class="rp-main"><h1 class="rp-h1"><span class="ln">${esc(spec.headline[0])}</span> <span class="ln">${esc(spec.headline[1])}</span></h1>`
    + `<p class="rp-intro">${esc(spec.intro)}</p>`
    + spec.sections.map(([h, p]) => `<div class="rp-sec"><h2>${esc(h)}</h2><p>${esc(p)}</p></div>`).join('')
    + `</div>`
    + `<div class="rp-rail">${spec.figures.map(([n, w]) => `<div class="rp-f"><p class="n">${esc(n)}</p><p class="w">${esc(w)}</p>${ill}</div>`).join('')}</div>`
    + `<div class="rp-foot"><p class="s">${esc(spec.sources)}${ill}</p><p class="se">${esc(spec.series[0])}<br>${esc(spec.series[1])}</p></div>`
    + `</div>`;
  // the overlay, in the sheet's px: bleed (hatched outside the trim), trim, safe line, margins and the 12-column grid
  const p = (v) => +(v * PT).toFixed(2), b = p(bleed);
  const trim = [b, b, p(TW), p(TH)];
  const inset = (r, d) => [r[0] + p(d), r[1] + p(d), r[2] - 2 * p(d), r[3] - 2 * p(d)];
  const safe = inset(trim, 18), marg = inset(trim, 54);
  const cols = Array.from({ length: 12 }, (_, i) => [b + p(54 + 43 * i), p(31)]);
  // each name sits in an empty band: the bleed's and the trim's between the trim and the safe line, the safe line's and the
  // margins' between the safe line and the margins, all along the foot, clear of every word on the page
  const layers = [
    { x: trim[0], y: trim[1], w: trim[2], h: trim[3], kind: 'hatch', label: 'Bleed, 0.125 in, hatched', lx: marg[0], ly: safe[1] + safe[3] + 1, ls: 13, sw: 1 },
    { x: trim[0], y: trim[1], w: trim[2], h: trim[3], kind: 'solid', label: 'Trim, 8.5 by 11 in', lx: marg[0] + 300, ly: safe[1] + safe[3] + 1, ls: 13, sw: 1 },
    { x: safe[0], y: safe[1], w: safe[2], h: safe[3], label: 'Safe line, 0.25 in', lx: marg[0], ly: marg[1] + marg[3] + 13, ls: 13, sw: 1 },
    { x: marg[0], y: marg[1], w: marg[2], h: marg[3], label: 'Margins, 0.75 in, and 12 columns', lx: marg[0] + 220, ly: marg[1] + marg[3] + 13, ls: 13, sw: 1 },
    { x: marg[0], y: marg[1], w: marg[2], h: marg[3], kind: 'cols', cols },
  ];
  return {
    id: spec.id, type, w: W, h: H, unit: 'px', css, html, layers, alt: spec.alt, title: spec.title,
    live: [safe[0], safe[1], safe[2], safe[3]], floor_px: null,
    print: { width_in: row.width + 2 * (row.bleed || 0), height_in: row.height + 2 * (row.bleed || 0), bleed_pt: bleed, trim_pt: [TW, TH] },
    exports: [
      { kind: 'pdf', name: spec.export_name, platform: spec.platform, theme: 'light' },
      { kind: 'png', name: spec.export_name + '-Proof-96ppi', platform: null, theme: 'light', viewport: [W, H], proof: true },
    ],
    plate: { head: spec.plate_head, line: spec.plate_line },
  };
}
