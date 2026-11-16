/* Social data card (coverage plan 3.16, core; S95). A still image for Substack, email and social posts (DR-49), drawn at
 * true size for each crop the spec names (spec.card.crops; DR-268: 1080 by 1350 and 1080 by 1080): the evidence word and
 * the grade line, the title, one other form drawn at card scale through c.inner (encode.of), so the inner form's 13 px words print at the
 * card's floor, and under a hairline the card's short source line. Every word stands at 36 px or more at true size
 * (R4-4: 13 px in a feed that shows the card at about a third of its size), the title larger. The inner form keeps its
 * own inks, key and words and reads labels.card_inner as c.card, with the height the crop leaves it. No red and blue on
 * any election card (DR-64); a web address joins once the site is settled (DR-55). A crop that cannot hold the inner
 * form says so (c.warn) and the kit fails what runs past its foot.
 * encode: of (the inner form's ID) and the inner form's own names. labels: the inner form's labels, plus card_source (the
 * card's short source line), card_note (the line over the source that says what a mark stands for), card_inner (options
 * the inner form reads as c.card), card_title ([px on a tall crop, px on a square one], default [56, 40]), card_margin (px to every edge on
 * both crops, default 64, the safe margin a platform's own controls leave).
 * NB-M2 and call 18 (fix pass after rounds 4 and 5, DR-211, Rule 08.2): every crop signs off with the lockmark, the 48 px
 * master (work/build/assets/identity/lockmark/20261109_Lockmark-48px-Master-Outline.svg, held below as LOCK48 and checked
 * against the file by maker_i_round4_derive.py) drawn at exactly twice its size, 96 px, bottom right inside the margin, on
 * whole pixels, so each of its pixels is a 2 by 2 block. Its inks are the identity masters board's: letters' ink for the
 * nodes, the signature red for the lever (data-red="signature"), Stone links on Newsprint and Newsprint links on Charcoal
 * (light-dark(), which follows the surface class's color-scheme). The source line under the hairline wraps clear of it. */
(function (K) {
  'use strict';
  var LOCK48 = '<g fill="var(--link,#5D636D)"><rect x="4.5" y="4" width="38" height="1"/><rect x="4" y="4.5" width="1" height="38"/><rect x="4.5" y="23" width="38" height="1"/><rect x="23" y="4.5" width="1" height="38"/><rect x="4.5" y="42" width="38" height="1"/><rect x="42" y="4.5" width="1" height="38"/></g><g fill="currentColor"><path d="M3 1H6V2H7V3H8V6H7V7H6V8H3V7H2V6H1V3H2V2H3Z"/><path d="M22 1H25V2H26V3H27V6H26V7H25V8H22V7H21V6H20V3H21V2H22Z"/><path d="M41 1H44V2H45V3H46V6H45V7H44V8H41V7H40V6H39V3H40V2H41Z"/><path d="M3 20H6V21H7V22H8V25H7V26H6V27H3V26H2V25H1V22H2V21H3Z"/><path d="M22 20H25V21H26V22H27V25H26V26H25V27H22V26H21V25H20V22H21V21H22Z"/><path d="M41 20H44V21H45V22H46V25H45V26H44V27H41V26H40V25H39V22H40V21H41Z"/><path d="M3 39H6V40H7V41H8V44H7V45H6V46H3V45H2V44H1V41H2V40H3Z"/><path d="M22 39H25V40H26V41H27V44H26V45H25V46H22V45H21V44H20V41H21V40H22Z"/></g><path fill="var(--lever,#E63946)" d="M40 38H45V39H46V40H47V45H46V46H45V47H40V46H39V45H38V40H39V39H40Z"/>', SIGN = 96, SIGN_GAP = 32;
  K.register_chart({
    form: 'social-data-card', name: 'Social Data Card', family: 'infographics', inner: true,
    encode: { of: 'form' },
    labels: ['card_source', 'card_note', 'card_inner', 'card_title', 'card_margin'],
    phone: 'same',
    draw: function (c) {
      var inner = K.forms[c.encode.of];
      if (!inner || !inner.draw || inner.form === 'social-data-card') throw new Error('social-data-card: encode.of names no other drawn form');
      var L = c.labels, W = c.width, H = c.crop ? c.crop.h : Math.round(W * 1.25), tall = H > W * 1.1;
      var min = c.min_text || 36, pad = L.card_margin || 64, cw = W - 2 * pad, lh = Math.round(min * 1.3), k = min / c.t('type-tick');
      var ts = (L.card_title || [56, 40])[tall ? 0 : 1], y = pad, base = y + min * 0.8;
      var ev = c.text(pad, base, c.spec.evidence_label || '', { role: 'eyebrow', size: min, weight: 700 });
      // the grade line runs on after the evidence word, as the figure sets them side by side (R4-4): the words that fit
      // beside it on its line, the rest on the lines under it
      var g = c.spec.grade_line ? K.typeset(c.spec, c.spec.grade_line) : '';
      if (g) {
        var gx = ev.x + ev.w + 18, ws = g.split(' '), n = 0;
        while (n < ws.length && K.measure(ws.slice(0, n + 1).join(' '), min, 400, 'reading') <= W - pad - gx) n++;
        if (n) ev = c.text(gx, base, ws.slice(0, n).join(' '), { role: 'tick', size: min, fill: 'secondary' });
        if (n < ws.length) ev = c.text(pad, base + (n ? lh : 0), ws.slice(n).join(' '), { role: 'tick', size: min, fill: 'secondary', max: cw, leading: lh });
      }
      // the title's measure narrowed a step at a time, by up to a third, until no word stands alone on its last line
      var tt = K.typeset(c.spec, c.spec.title), tm = cw, n0 = K.wrap(tt, ts, cw, 800, 'display').length;
      for (var m = cw; n0 > 1 && m > cw * 0.67; m -= 8) {
        var ls = K.wrap(tt, ts, m, 800, 'display');
        if (ls.length > n0) break;
        if (ls[ls.length - 1].indexOf(' ') > 0) { tm = m; break; }
      }
      var t = c.text(pad, ev.bottom + (tall ? 20 : 14) + ts * 0.8, c.spec.title, { role: 'label', face: 'display', size: ts, weight: 800, max: tm, leading: Math.round(ts * 1.12) });
      y = t.bottom + (tall ? 36 : 20);
      // the foot first (the line that says what a mark is, then the source), so the inner form takes what the crop leaves
      var nb = function (w) { return w ? K.wrap(K.typeset(c.spec, w), min, cw, 400, 'reading').length * lh : 0; };
      // the source line wraps clear of the 96 px sign-off at its right, and the foot under the hairline holds the taller of the two
      var sw = cw - SIGN - SIGN_GAP, nbs = function (w) { return w ? K.wrap(K.typeset(c.spec, w), min, sw, 400, 'reading').length * lh : 0; };
      var note = L.card_note || '', src = L.card_source || c.spec.source_line || '', nh = nb(note), sh = nbs(src);
      var fy = H - pad - Math.max(sh, SIGN) - 24, ny = fy - (note ? nh + 20 : 0), room = ny - (tall ? 32 : 24) - y;
      // the inner form's lowest words hang about 16 px under the height it fills, so it is given that much less
      var ih = c.inner(pad, y, cw, k, Object.assign({}, L.card_inner || {}, { height: (room - 18) / k }));
      if (ih > room + 0.5) c.warn('social-data-card: the inner form runs ' + Math.round(ih - room) + ' px past the room the ' + (c.crop ? c.crop.name : '') + ' crop leaves it');
      if (note) c.text(pad, ny + min * 0.93, note, { role: 'label', size: min, fill: 'label', max: cw, leading: lh });
      c.line(pad, fy, W - pad, fy, { stroke: 'gridline', width: 2, mark: false });
      c.text(pad, fy + 24 + min * 0.93, src, { role: 'tick', size: min, fill: 'secondary', max: sw, leading: lh });
      // the sign-off (DR-211): the 48 px master at exactly 96 px, its box on whole pixels, bottom right inside the margin
      var sx = Math.round(W - pad - SIGN), sy = Math.round(H - pad - SIGN);
      // the master's three paints, its letters' ink (currentColor), lever and links, set straight on its shapes as tokens, so the
      // standalone export resolves each to its color and carries no var() (no style attribute)
      var paint = LOCK48.split('var(--link,#5D636D)').join('light-dark(var(--oa-color-palette-stone), var(--oa-color-palette-newsprint))')
        .split('currentColor').join('var(--oa-color-text-primary)').split('var(--lever,#E63946)').join('var(--oa-color-identity-signature)');
      c._push('<g class="oac-sign-off" data-red="signature" data-oa-sign-off="lockmark-48-at-96" aria-hidden="true" transform="translate(' + sx + ',' + sy + ') scale(' + SIGN / 48 + ')">' + paint + '</g>');
      c._ink('icon', sx, sy, SIGN, SIGN, { fill: 'label' }, { a: SIGN * SIGN });
      c.height(H);
    }
  });
})(globalThis.OAChart);
