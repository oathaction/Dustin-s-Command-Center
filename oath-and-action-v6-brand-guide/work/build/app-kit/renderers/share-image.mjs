// Share preview renderer (chat 11, contract C6): the website's link-preview card, the Open Graph image, at the size of the
// specifications table's row (website.share_preview, 1200 by 630 px). Layout from the page specs' section 8
// (work/handoffs/phase-4/20261121_Web-Page-Specs.md): the identity proofs' link-preview card (s-proofs-social) on Newsprint
// with a Charcoal foot band, the card's one dark panel. The kicker at the H3 style's 32 px, its lead in the text's ink and its
// tail in the secondary ink; the headline at the title style's 110 px, line height 0.95, where {B} would set ampersand B as
// its "and" in the card's one working red, with Rule 05.3's keyline inside it on Newsprint (DR-330); in the band, the wordmark's display master 44 px tall at the left, centered on the
// sign-off, and Rule 08.2's sign-off at the right, the 48 px master drawn at exactly twice its size (96 px), on whole pixels,
// in the dark card's paints (the links take the nodes' color).
//
// Content keys: id, type "share-image", platform (default website.share_preview), band (the foot band's height, default
// 200), export_name, plate_head, plate_line; words (kicker [lead, tail], headline [lines], alt) from the chapter generator's
// key for this id (DD-3), or from the content file itself.
import { esc, mark, platform, type_css } from '../lib.mjs';
import { words } from './web-site.mjs';
import { keyline } from './hinge-keyline.mjs';

export const type = 'share-image';
const AMP_DISPLAY = 'work/build/assets/identity/ampersand/20261028_Amp-B-Display-Master.svg';
const WORDMARK = 'work/build/assets/identity/wordmark/20261028_Wordmark-Display-Master.svg';
const LOCK48 = 'work/build/assets/identity/lockmark/20261109_Lockmark-48px-Master-Outline.svg';
const M = 72;           // the margin on every side
const SIGN = 96;        // Rule 08.2: the 48 px master at exactly twice its size
const KICK = 32;        // the H3 style at 32 px
const HL = 110;         // the title style at 110 px
const WM_H = 44;        // the wordmark's display master, 44 px tall

export function render(spec) {
  const w = spec.kicker ? spec : words()[spec.id];
  const row = platform(spec.platform || 'website.share_preview');
  const W = row.width, H = row.height, BAND = spec.band || 200;
  const sign_x = W - M - SIGN, sign_y = H - M - SIGN;
  const wm_w = +(398.57 * WM_H / 44).toFixed(2), wm_y = Math.round(sign_y + SIGN / 2 - WM_H / 2);
  const cap = 0.7275 * HL;
  const bw = +(93.29 * cap / 100).toFixed(2), bh = +(102.69 * cap / 100).toFixed(2);
  // chat 13b (DR-330): the card is Newsprint, so a hinge headline's B takes Rule 05.3's keyline
  const B = keyline(mark(AMP_DISPLAY, { cls: 'sh-b', width: bw, height: bh, label: 'and', red: 'working', attrs: `data-red-job="${esc(spec.hinge_job || 'the one point the headline names')}"` }), 'sh-b-keyline');
  const wm = mark(WORDMARK, { cls: 'sh-wm', width: wm_w, height: WM_H, label: 'Oath & Action', red: 'signature' });
  const sign = mark(LOCK48, { cls: 'sh-sign', width: SIGN, height: SIGN, red: 'signature', attrs: 'data-oa-sign-off="lockmark-48-at-96" shape-rendering="crispEdges"' });
  const line = (s) => `<span class="ln">${s.split('{B}').map((x) => esc(x).replace(/ /g, '&nbsp;')).join(B)}</span>`;
  const css = `
.sh{position:relative;width:${W}px;height:${H}px;box-sizing:border-box;overflow:hidden;background:var(--oa-color-surface-newsprint);color:var(--oa-color-text-primary-on-newsprint);font-kerning:normal;font-variant-ligatures:common-ligatures}
.sh p{margin:0}
.sh-k{position:absolute;left:${M}px;top:${M}px;${type_css('h3', { size: `${KICK}px` })};color:var(--oa-color-text-primary-on-newsprint);white-space:nowrap}
.sh-k .t{color:var(--oa-color-text-secondary-on-newsprint)}
.sh-hl{position:absolute;left:${M}px;top:131px;width:${W - 2 * M}px;${type_css('title', { size: `${HL}px`, lh: '0.95' })};color:var(--oa-color-text-primary-on-newsprint)}
.sh-hl .ln{display:block;white-space:nowrap}
.sh-b{display:inline-block;vertical-align:-1.08px;color:var(--oa-color-palette-pillar-red)}
.sh-band{position:absolute;left:0;top:${H - BAND}px;width:${W}px;height:${BAND}px}
.sh-wm{position:absolute;left:${M}px;top:${wm_y}px;color:var(--oa-color-text-primary-on-charcoal);--amp:var(--oa-color-identity-signature-on-charcoal);--lever:var(--oa-color-identity-signature-on-charcoal);--link:var(--oa-color-text-primary-on-charcoal);--line:var(--oa-color-text-primary-on-charcoal)}
.sh-sign{position:absolute;left:${sign_x}px;top:${sign_y}px;color:var(--oa-color-text-primary-on-charcoal);--lever:var(--oa-color-identity-signature-on-charcoal);--link:var(--oa-color-text-primary-on-charcoal);--line:var(--oa-color-text-primary-on-charcoal)}
`;
  const html = `<div class="sh" data-oa-application="${esc(spec.id)}">`
    + `<p class="sh-k">${esc(w.kicker[0])}${w.kicker[1] ? `<span class="t"> · ${esc(String(w.kicker[1]).replace(/^\s*·\s*/, ''))}</span>` : ''}</p>`
    + `<p class="sh-hl">${w.headline.map(line).join('')}</p>`
    + `<div class="sh-band oa-surface-charcoal"></div>`
    + wm + sign + `</div>`;
  const layers = [{ x: M, y: M, w: W - 2 * M, h: H - 2 * M, label: 'Margin, 72 px', lx: M, ly: 24 }];
  return {
    id: spec.id, type, w: W, h: H, unit: 'px', css, html, layers, alt: w.alt, alt_short: w.alt,
    live: [M, M, W - 2 * M, H - 2 * M], floor_px: KICK, panel: '.sh-band',
    sign_off: { x: sign_x, y: sign_y, size: SIGN, ground: 'charcoal' },
    exports: [{ kind: 'png', name: spec.export_name, platform: row.id, theme: 'light', viewport: [W, H] }],
    plate: { head: spec.plate_head, line: spec.plate_line, feed_px: 500 },
    meta: { 'og:image:width': String(W), 'og:image:height': String(H), 'og:image:alt': w.alt },
  };
}
