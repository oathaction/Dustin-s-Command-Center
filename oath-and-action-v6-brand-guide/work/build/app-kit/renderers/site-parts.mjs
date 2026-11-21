// The website's shared parts (chat 11): the masthead with its parts and phone menu, the theme switch, the skip link and the
// site's script, each read from chapter 18's own files and changed only where the website's answers say (DR-307's seven
// parts, the accessibility lead's AL-05 to AL-11), never copied. The page renderers (web-site.mjs) put these around each
// page's content; the footer and the page bodies follow the design director's page specs.
//
// From c-18-masthead.html: the header, bar, home link with the 24 and 16 px wordmark masters, the parts' navigation, Menu,
// the dialog with its head, Close and its navigation; the Topics row and its list go (DR-307's parts hold no sublist), the
// parts become the site's, ids take the page's prefix, and every icon is a <use> of the guide's sprite (contract C4).
// From c-18-theme-switch.html: the fieldset alone, twice: in the bar after the parts (AL-07, AL-08) and in the menu after its
// head; each instance its own radio group, both setting one target, so chapter 18's script keeps them showing one choice.
import fs from 'fs';
import path from 'path';
import { CODE, esc } from '../lib.mjs';
import { sprite_icons } from './web-page.mjs';

const read = (f) => fs.readFileSync(path.join(CODE, f), 'utf8');
export const UTILITY_SPRITE = ['oa-sym-u-menu-24px', 'oa-sym-u-close-24px', 'oa-sym-u-selected-check-24px', 'oa-sym-u-another-site-16px'];

// chapter 18's switch, its fieldset alone, for one target and one radio group
export function theme_switch({ theme = 'device', target = null, group = 'oa-theme', cls = '' } = {}) {
  let f = read('c-18-theme-switch.html').match(/<fieldset class="oa-theme"[\s\S]*?<\/fieldset>/)[0];
  f = target ? f.replace(/data-oa-theme-for="[^"]*"/, `data-oa-theme-for="${target}"`) : f.replace(/\s*data-oa-theme-for="[^"]*"/, '');
  f = f.replace(/name="oa-theme"/g, `name="${group}"`).replace(/\s+checked>/g, '>').replace(new RegExp(`(value="${theme}")`), '$1 checked');
  if (cls) f = f.replace('class="oa-theme"', `class="oa-theme ${cls}"`);
  return sprite_icons(f).replace(/\s*\n\s*/g, ' ').replace(/<input\s+/g, '<input ');
}

// The masthead. parts: [{ label, href, current: false | 'page' | 'true' }]; pid prefixes every id; home: { href, name };
// sw: { theme, target, group } for the two switches
export function masthead({ pid, parts, home, sw }) {
  let h = read('c-18-masthead.html').match(/<header class="oa-masthead"[\s\S]*?<\/header>/)[0];
  const cur = (p) => (p.current ? ` aria-current="${p.current === true ? 'page' : p.current}"` : '');
  const bar = parts.map((p) => `<li><a class="oa-masthead-part" href="${esc(p.href)}"${cur(p)}>${esc(p.label)}</a></li>`).join('');
  const rows = parts.map((p) => `<li><a class="oa-masthead-row-link" href="${esc(p.href)}"${cur(p)}>${esc(p.label)}</a></li>`).join('');
  h = h.replace(/<ul class="oa-masthead-parts">[\s\S]*?<\/ul>/, `<ul class="oa-masthead-parts">${bar}</ul>`);
  h = h.replace(/<ul class="oa-masthead-list">[\s\S]*?<\/ul>/, `<ul class="oa-masthead-list">${rows}</ul>`);
  h = h.replace(/\s*<button\s+type="button"\s+class="oa-masthead-row"[\s\S]*?<\/button>\s*<ul class="oa-masthead-sub"[\s\S]*?<\/ul>/, '');
  h = h.replace(/href="#oa-masthead-page"/, `href="${esc(home.href)}"`);
  h = h.replace(/aria-label="Oath &amp; Action"/g, `aria-label="${esc(home.name)}"`);
  h = h.replace(/(id|aria-labelledby)="oa-masthead-dialog-name"/g, `$1="${pid}-menu-name"`).replace(/(id|aria-controls)="oa-masthead-dialog"/g, `$1="${pid}-menu"`);
  // AL-07, AL-08: the switch after the parts in the bar, and at the top of the menu after its head
  h = h.replace(/(<\/nav>\s*)(<button\s+type="button"\s+class="oa-masthead-menu")/, `$1${theme_switch({ ...sw, group: `${sw.group}-bar`, cls: 'oa-site-switch-bar' })}$2`);
  h = h.replace(/(<\/div>\s*)(<nav\s+class="oa-masthead-dialog-nav")/, `$1${theme_switch({ ...sw, group: `${sw.group}-menu`, cls: 'oa-site-switch-menu' })}$2`);
  return sprite_icons(h).replace(/\s*\n\s*/g, ' ');
}

export const masthead_css = () => read('c-18-masthead.css');
export const switch_css = () => read('c-18-theme-switch.css');
export const masthead_js = () => read('c-18-masthead.js');
export const switch_js = () => read('c-18-theme-switch.js');
export const switch_head_js = () => read('c-18-theme-switch.head.js');

// AL-06, the website's addition to chapter 18's masthead script (not chapter 18's code set): when the window widens past
// the breakpoint while the menu is open, the menu closes and focus goes to the current part's link in the bar, or to the
// home link when no part is current, since Menu is then hidden. bp_em is the masthead's breakpoint in em.
export function close_on_widen_js(bp_em) {
  return `(function () {
  // W1 (2.4.11): when the menu opens, its scroll padding is its sticky title row's height and rule, so no focused row
  // hides under the row, at any text size
  document.querySelectorAll('[data-oa-masthead] .oa-masthead-menu').forEach(function (menu) {
    menu.addEventListener('click', function () {
      var dialog = document.getElementById(menu.getAttribute('aria-controls'));
      var head = dialog && dialog.querySelector('.oa-masthead-dialog-head');
      // the row, then room for the focus ring (2 px, 2 px out) and a little air
      if (head) dialog.style.scrollPaddingTop = (Math.ceil(head.getBoundingClientRect().height) + 9) + 'px';
    });
  });
  var mq = window.matchMedia('(min-width: ${bp_em}em)');
  function widened() {
    if (!mq.matches) return;
    document.querySelectorAll('[data-oa-masthead]').forEach(function (head) {
      var menu = head.querySelector('.oa-masthead-menu');
      var dialog = menu && document.getElementById(menu.getAttribute('aria-controls'));
      if (!dialog || !dialog.open) return;
      var to = head.querySelector('.oa-masthead-part[aria-current]') || head.querySelector('.oa-masthead-home');
      dialog.addEventListener('close', function () { if (to) to.focus(); }, { once: true });
      dialog.close();
    });
  }
  if (mq.addEventListener) mq.addEventListener('change', widened); else mq.addListener(widened);
})();`;
}
