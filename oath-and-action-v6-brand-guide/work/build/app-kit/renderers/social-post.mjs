// Social post renderer (DR-297, chat 10): a one-figure Explainer card on Newsprint with a Charcoal foot band that holds the
// source line and Rule 08.2's 96 px sign-off. Layout from work/handoffs/phase-4/20261121_Kit-Sample-Specs.md, section 1;
// sizes from the platform row the content file names (instagram.portrait for the studio sample: 1080 by 1350 px).
// render(spec) returns the application at true size as static markup with its CSS, its overlay layers and its exports.
import { esc, mark, platform, safe_boxes, type_css } from '../lib.mjs';

export const type = 'social-post';
const AMP_DISPLAY = 'work/build/assets/identity/ampersand/20261028_Amp-B-Display-Master.svg';
const LOCK48 = 'work/build/assets/identity/lockmark/20261109_Lockmark-48px-Master-Outline.svg';
const M = 64;          // the margin on every side (--oa-space-800, S95's card_margin)
const SIGN = 96;       // Rule 08.2's sign-off: the 48 px master at exactly twice its size (DR-211)
const GAP = 32;        // between the source line and the sign-off (--oa-space-400)
const FLOOR = 36;      // every word at 36 px or more (Rule 14.141; R4-4)

export function render(spec) {
  const row = platform(spec.platform);
  const W = row.width, H = row.height;
  const cap = 0.7275 * 110;                         // ampersand B's cap height at the headline's 110 px
  const bw = +(93.29 * cap / 100).toFixed(2), bh = +(102.69 * cap / 100).toFixed(2);
  const B = mark(AMP_DISPLAY, { cls: 'sp-b', width: bw, height: bh, label: 'and', red: 'working',
    attrs: `data-red-job="${esc(spec.hinge_job)}"` });
  // the sign-off: the 48 px master's own paints set to tokens for a dark ground (Rule 08.2's dark card: the links take the
  // nodes' color), as the chart kit's social card paints it, on whole pixels
  const sign = mark(LOCK48, { cls: 'sp-sign', width: SIGN, height: SIGN, red: 'signature',
    attrs: 'data-oa-sign-off="lockmark-48-at-96" shape-rendering="crispEdges"' });
  const css = `
.sp{position:relative;width:${W}px;height:${H}px;box-sizing:border-box;overflow:hidden;background:var(--oa-color-surface-newsprint);color:var(--oa-color-text-primary-on-newsprint);font-kerning:normal;font-variant-ligatures:common-ligatures}
.sp p{margin:0}
.sp-top{position:absolute;left:${M}px;top:${M}px;width:${W - 2 * M}px}
.sp-k{font-family:var(--oa-type-h3-font-family);font-style:normal;font-weight:800;font-size:${FLOOR}px;line-height:1.08;letter-spacing:-0.01em;color:var(--oa-color-text-primary-on-newsprint)}
.sp-k .s{color:var(--oa-color-text-secondary-on-newsprint)}
.sp-hl{margin-top:40px !important;${type_css('title', { size: '110px' })};color:var(--oa-color-text-primary-on-newsprint)}
.sp-hl .ln{display:block;white-space:nowrap}
.sp-b{display:inline-block;vertical-align:-1.08px;color:var(--oa-color-palette-pillar-red)}
.sp-fig{margin-top:80px !important;${type_css('figure', { size: '104px' })};color:var(--oa-color-text-primary-on-newsprint)}
.sp-what{margin-top:16px !important;font-family:var(--oa-type-body-font-family);font-weight:600;font-size:${FLOOR}px;line-height:47px;color:var(--oa-color-text-primary-on-newsprint)}
.sp-ctx{margin-top:8px !important;font-family:var(--oa-type-body-font-family);font-weight:400;font-size:${FLOOR}px;line-height:47px;color:var(--oa-color-text-primary-on-newsprint)}
.sp-band{position:absolute;left:0;right:0;bottom:0;box-sizing:border-box;padding:${M}px ${M}px ${M}px ${M}px;background:var(--oa-color-surface-charcoal);color-scheme:dark}
.sp-src{width:${W - 2 * M - SIGN - GAP}px;font-family:var(--oa-type-body-font-family);font-weight:400;font-size:${FLOOR}px;line-height:47px;color:var(--oa-color-text-secondary-on-charcoal)}
.sp-sign{position:absolute;left:${W - M - SIGN}px;top:${H - M - SIGN}px;color:var(--oa-color-text-primary-on-charcoal);--link:var(--oa-color-text-primary-on-charcoal);--lever:var(--oa-color-identity-signature-on-charcoal)}
`;
  const html = `<div class="sp" data-oa-application="${esc(spec.id)}">`
    + `<div class="sp-top">`
    + `<p class="sp-k">${esc(spec.kicker[0])}<span class="s">${esc(spec.kicker[1])}</span></p>`
    + `<p class="sp-hl"><span class="ln">${esc(spec.headline[0])}</span><span class="ln">${B}&nbsp;${esc(spec.headline[1]).replace(/ /g, '&nbsp;')}</span></p>`
    + `<p class="sp-fig">${esc(spec.figure)}</p>`
    + `<p class="sp-what">${esc(spec.counts)}</p>`
    + `<p class="sp-ctx">${esc(spec.context)}</p>`
    + `</div>`
    + `<div class="sp-band"><p class="sp-src">${esc(spec.source)}</p></div>`
    + sign
    + `</div>`;
  // the overlay's layers: the margin, and the grid's centered crop from the platform row's safe area
  const box = safe_boxes(row, W, H).safe;
  const layers = [{ x: M, y: M, w: W - 2 * M, h: H - 2 * M, label: 'Margin, 64 px', lx: M + 8, ly: M + 8 }];
  if (box) layers.push({ x: box[0], y: box[1], w: box[2], h: box[3], kind: 'shade', label: 'Profile grid crop, 3:4', lx: box[0] + 8, ly: H / 2 });
  return {
    id: spec.id, type, w: W, h: H, unit: 'px', css, html, layers, alt: spec.alt, alt_short: spec.alt_short,
    // what the export checks read: the live box no word or mark may leave, and the floor every word keeps
    live: [M, M, W - 2 * M, H - 2 * M], floor_px: FLOOR, panel: '.sp-band',
    sign_off: { x: W - M - SIGN, y: H - M - SIGN, size: SIGN },
    exports: [{ kind: 'png', name: spec.export_name, platform: spec.platform, theme: 'light', viewport: [W, H] }],
    plate: { head: spec.plate_head, line: spec.plate_line, feed_px: 390 },
  };
}
