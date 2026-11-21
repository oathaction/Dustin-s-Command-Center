// Share preview renderer (chat 11, contract C6): the website's link-preview card, the Open Graph image, at the size of the
// specifications table's row (website.share_preview, 1200 by 630 px). Layout from the identity proofs' link-preview card
// (Rule 08.2's card, s-proofs-social): a 72 px margin; the kicker at the H3 style's 32 px, its lead in the text's ink and its
// tail in the secondary ink; the headline at the title style's 110 px, where {B} sets ampersand B from its display master as
// the "and", in the card's one working red; the wordmark's display master 44 px tall at the bottom left; and Rule 08.2's
// sign-off at the bottom right, the 48 px master drawn at exactly twice its size (96 px).
//
// Content keys: id, type "share-image", platform (default website.share_preview), ground ("newsprint" or "charcoal"),
// kicker [lead, tail], headline [line, ...] ({B} marks ampersand B), hinge_job (the working red's job), alt, alt_short,
// export_name, plate_head, plate_line.
import { esc, mark, platform, type_css } from '../lib.mjs';

export const type = 'share-image';
const AMP_DISPLAY = 'work/build/assets/identity/ampersand/20261028_Amp-B-Display-Master.svg';
const WORDMARK = 'work/build/assets/identity/wordmark/20261028_Wordmark-Display-Master.svg';
const LOCK48 = 'work/build/assets/identity/lockmark/20261109_Lockmark-48px-Master-Outline.svg';
const M = 72;           // the margin on every side (the proofs card's)
const SIGN = 96;        // Rule 08.2: the 48 px master at exactly twice its size
const KICK = 32;        // the H3 style at 32 px, large enough to read in a phone's feed
const HL = 110;         // the title style at 110 px
const WM_H = 44;        // the wordmark's display master, 44 px tall

export function render(spec) {
  const row = platform(spec.platform || 'website.share_preview');
  const W = row.width, H = row.height;
  const dark = spec.ground === 'charcoal';
  const on = dark ? 'charcoal' : 'newsprint';
  const cap = 0.7275 * HL;                          // ampersand B's cap height at the headline's size
  const bw = +(93.29 * cap / 100).toFixed(2), bh = +(102.69 * cap / 100).toFixed(2);
  const B = mark(AMP_DISPLAY, { cls: 'sh-b', width: bw, height: bh, label: 'and', red: 'working', attrs: `data-red-job="${esc(spec.hinge_job || 'the one point the headline names')}"` });
  const wm_w = +(398.57 * WM_H / 44).toFixed(2);
  const wm = mark(WORDMARK, { cls: 'sh-wm', width: wm_w, height: WM_H, label: 'Oath & Action', red: 'signature' });
  const sign = mark(LOCK48, { cls: 'sh-sign', width: SIGN, height: SIGN, red: 'signature', attrs: 'data-oa-sign-off="lockmark-48-at-96" shape-rendering="crispEdges"' });
  const line = (s) => `<span class="ln">${s.split('{B}').map((x) => esc(x).replace(/ /g, '&nbsp;')).join(B)}</span>`;
  const css = `
.sh{position:relative;width:${W}px;height:${H}px;box-sizing:border-box;overflow:hidden;background:var(--oa-color-surface-${on});color:var(--oa-color-text-primary-on-${on});font-kerning:normal;font-variant-ligatures:common-ligatures${dark ? ';color-scheme:dark' : ''}}
.sh p{margin:0}
.sh-top{position:absolute;left:${M}px;top:${M}px;width:${W - 2 * M}px}
.sh-k{${type_css('h3', { size: `${KICK}px` })};color:var(--oa-color-text-primary-on-${on})}
.sh-k .t{color:var(--oa-color-text-secondary-on-${on})}
.sh-hl{margin-top:24px !important;${type_css('title', { size: `${HL}px` })};color:var(--oa-color-text-primary-on-${on})}
.sh-hl .ln{display:block;white-space:nowrap}
.sh-b{display:inline-block;vertical-align:-1.08px;color:var(--oa-color-palette-pillar-red)}
.sh-wm{position:absolute;left:${M}px;top:${H - M - WM_H}px;color:var(--oa-color-text-primary-on-${on});--amp:var(--oa-color-identity-signature-on-${on});--lever:var(--oa-color-identity-signature-on-${on});--link:${dark ? `var(--oa-color-text-primary-on-${on})` : 'var(--oa-color-palette-stone)'};--line:${dark ? `var(--oa-color-text-primary-on-${on})` : 'var(--oa-color-palette-stone)'}}
.sh-sign{position:absolute;left:${W - M - SIGN}px;top:${H - M - SIGN}px;color:var(--oa-color-text-primary-on-${on});--lever:var(--oa-color-identity-signature-on-${on});--link:${dark ? `var(--oa-color-text-primary-on-${on})` : 'var(--oa-color-palette-stone)'};--line:${dark ? `var(--oa-color-text-primary-on-${on})` : 'var(--oa-color-palette-stone)'}}
`;
  const html = `<div class="sh" data-oa-application="${esc(spec.id)}">`
    + `<div class="sh-top"><p class="sh-k">${esc(spec.kicker[0])}<span class="t">${esc(spec.kicker[1] || '')}</span></p>`
    + `<p class="sh-hl">${spec.headline.map(line).join('')}</p></div>`
    + wm + sign + `</div>`;
  const layers = [{ x: M, y: M, w: W - 2 * M, h: H - 2 * M, label: 'Margin, 72 px', lx: M, ly: 24 }];
  return {
    id: spec.id, type, w: W, h: H, unit: 'px', css, html, layers, alt: spec.alt, alt_short: spec.alt_short,
    live: [M, M, W - 2 * M, H - 2 * M], floor_px: KICK, ground: on,
    sign_off: { x: W - M - SIGN, y: H - M - SIGN, size: SIGN, ground: on },
    exports: [{ kind: 'png', name: spec.export_name, platform: row.id, theme: dark ? 'dark' : 'light', viewport: [W, H] }],
    plate: { head: spec.plate_head, line: spec.plate_line, feed_px: 500 },
    meta: { 'og:image:width': String(W), 'og:image:height': String(H), 'og:image:alt': spec.alt_short || spec.alt },
  };
}
