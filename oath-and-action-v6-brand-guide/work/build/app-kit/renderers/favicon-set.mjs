// Favicon set renderer (chat 11, contract C6): the website's icons, each sized by its row in the specifications table, each
// from ampersand B's masters (DR-116; Rule 04.7; Rule 08.2's row "Favicon": never the lockmark).
//   SVG favicon         website.favicon_svg     B's 16 px master (14 by 16) centered on whole pixels in a 16 by 16 viewBox, no
//                                               tile, in the content file's favicon_ink (signature red, as Rule 04.7's plate
//                                               draws it on a light and a dark tab)
//   favicon.ico         website.favicon_ico     the same drawing at 16, 32 and 48 px (1x, 2x and 3x) on a clear ground, in one
//                                               file (the row's studio choice), PNG inside
//   Apple touch icon    website.apple_touch_icon  the app icon: B on the Charcoal square (oa.component.appIcon.tile), B 58 percent
//                                               of the tile from its display master, in its accent (signature red); full
//                                               bleed, since iOS rounds the corners itself
//   Manifest icons      website.manifest_192, website.manifest_512 (maskable): as the Apple touch icon; at 512 px B's box
//                                               stays inside the row's safe circle (radius 40 percent of the width)
// Content keys: id, type "favicon-set", favicon_ink (a token, default --oa-color-identity-signature-on-white), export_stem
// (the dated file names' words), alt, plate_head, plate_line.
import fs from 'fs';
import path from 'path';
import { ROOT, esc, platform, token_value } from '../lib.mjs';

export const type = 'favicon-set';
const AMP16 = 'work/build/assets/identity/ampersand/20261028_Amp-B-16px-Master.svg';
const AMP_DISPLAY = 'work/build/assets/identity/ampersand/20261028_Amp-B-Display-Master.svg';
const B_SHARE = 0.58;   // Rule 04.7: B's height, 58 percent of the tile

function master(rel) {
  const t = fs.readFileSync(path.join(ROOT, rel), 'utf8');
  const vb = t.match(/viewBox="([^"]+)"/)[1].split(/\s+/).map(Number);
  const paths = [...t.matchAll(/<path\b[^>]*\sd="([^"]+)"/g)].map((m) => m[1]);
  return { vb, paths };
}

// The standalone SVG favicon: literal colors, since a favicon file reads no stylesheet (the value read from tokens.css)
export function favicon_svg(ink_token) {
  const m = master(AMP16);
  const [, , w, h] = m.vb;
  const ink = token_value(ink_token);
  const dx = (16 - w) / 2, dy = (16 - h) / 2;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="16" height="16" role="img" aria-labelledby="t d">`
    + `<title id="t">Oath &amp; Action</title><desc id="d">Ampersand B from its 16 px master, the site's favicon.</desc>`
    + `<g transform="translate(${dx} ${dy})" fill="${ink}">${m.paths.map((d) => `<path d="${d}"/>`).join('')}</g></svg>\n`;
}

function app_icon(px) {
  const m = master(AMP_DISPLAY);
  const [, , vw, vh] = m.vb;
  const bh = +(B_SHARE * px).toFixed(2), bw = +(vw * bh / vh).toFixed(2);
  const css = `.fi-tile{width:${px}px;height:${px}px;display:flex;align-items:center;justify-content:center;background:var(--oa-component-app-icon-tile)}`
    + `.fi-tile svg{display:block;color:var(--oa-component-app-icon-accent)}`;
  const t = fs.readFileSync(path.join(ROOT, AMP_DISPLAY), 'utf8').replace(/<\?xml[^>]*>/, '').replace(/<title>[\s\S]*?<\/title>|<desc>[\s\S]*?<\/desc>/g, '');
  const svg = t.replace(/<svg\b/, `<svg width="${bw}" height="${bh}" aria-hidden="true" focusable="false" data-red="signature"`).replace(/\s*\n\s*/g, ' ');
  return { css, html: `<div class="fi-tile">${svg}</div>`, b: [bw, bh] };
}

export function render(spec) {
  const ink = spec.favicon_ink || '--oa-color-identity-signature-on-white';
  const stem = spec.export_stem || 'Website';
  const svg = favicon_svg(ink);
  const rows = { svg: platform('website.favicon_svg'), ico: platform('website.favicon_ico'), apple: platform('website.apple_touch_icon'),
    m192: platform('website.manifest_192'), m512: platform('website.manifest_512') };
  const tiles = [['apple', 'Apple-Touch-Icon-180', 'apple-touch-icon.png'], ['m192', 'Manifest-Icon-192', 'icon-192.png'], ['m512', 'Manifest-Icon-512-Maskable', 'icon-512-maskable.png']]
    .map(([k, words, serve]) => { const r = rows[k]; const a = app_icon(r.width); return { kind: 'png', name: `${stem}-${words}`, platform: r.id, w: r.width, h: r.height, css: a.css, html: a.html, serve_as: serve, b: a.b, theme: 'light' }; });
  const ico_sizes = [16, 32, 48];
  return {
    id: spec.id, type, alt: spec.alt, svg,
    exports: [
      { kind: 'svg', name: `${stem}-Favicon`, platform: rows.svg.id, text: svg, serve_as: 'icon.svg', theme: 'light' },
      { kind: 'ico', name: `${stem}-Favicon-16-32-48`, platform: rows.ico.id, sizes: ico_sizes, serve_as: 'favicon.ico', theme: 'light',
        html_at: (px) => `<img src="data:image/svg+xml;base64,${Buffer.from(svg).toString('base64')}" width="${px}" height="${px}" alt="" style="display:block">` },
      ...tiles,
    ],
    // the maskable icon's safe circle, for the plate's overlay and the check
    safe_512: { cx: rows.m512.width / 2, cy: rows.m512.height / 2, r: rows.m512.width * rows.m512.safe_area.radius_pct / 100 },
    plate: { head: spec.plate_head, line: spec.plate_line },
  };
}

// Every icon's markup for the guide's plate: the favicon at 16 px on a light and a dark tab, and the three tiles
export function plate_html(r) {
  const tab = (ground) => `<span class="fi-tab fi-tab--${ground}">${r.svg.replace('<svg ', '<svg aria-hidden="true" focusable="false" ')}<span class="fi-tab-t">${esc('Oath & Action')}</span></span>`;
  return tab('light') + tab('dark');
}
