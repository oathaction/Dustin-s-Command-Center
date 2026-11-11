/* Social data card (coverage plan 3.16, core; any specimen). A still image for Substack, email and social posts (DR-49):
 * the evidence word, the title and the source inside the drawing, around one other form drawn at the card's width. No red
 * and blue on any election card (DR-64); a web address joins once the site is settled (DR-55).
 * encode: of (the inner form's ID) and the inner form's own names. labels: the inner form's labels, plus card_source (the
 * shortened source printed on the card). */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'social-data-card', name: 'Social Data Card', family: 'infographics', inner: true,
    encode: { of: 'form' },
    labels: ['card_source'],
    phone: 'same',
    draw: function (c) {
      var inner = K.forms[c.encode.of];
      if (!inner || inner.form === 'social-data-card') throw new Error('social-data-card: encode.of names no other form');
      var W = c.width, pad = 24, y = pad;
      c.rect(0, 0, W, 10, { fill: 'none', mark: false });
      c.text(pad, y + 13, c.spec.evidence_label || '', { role: 'eyebrow', weight: 700 });
      y += 26;
      var tsize = c.phone ? c.t('type-title-phone-size') : c.t('type-title-size');
      var t = c.text(pad, y + tsize * 0.8, c.spec.title, { role: 'label', face: 'display', size: tsize, weight: 800, max: W - 2 * pad, leading: c.phone ? c.t('type-title-phone-leading') : c.t('type-title-leading') });
      y = t.y + t.h + 24;
      // the inner form, drawn by its own module into this context, shifted down and in
      var sub = new K.Ctx(c.spec, c.rows, { width: W - 2 * pad, ground: c.ground, t: c.t, uid: c.uid + '-in' });
      sub.encode = c.encode; sub.labels = c.labels;
      inner.draw(sub);
      var ih = sub._h;
      sub.texts.forEach(function (b) { ih = Math.max(ih, b.y + b.h + 2); });
      c._defs = c._defs.concat(sub._defs);
      c._push('<g transform="translate(' + pad + ',' + y + ')">' + sub._els.join('') + '</g>');
      sub.texts.forEach(function (b) { c.texts.push(Object.assign({}, b, { x: b.x + pad, y: b.y + y })); });
      sub.marks.forEach(function (m) { c.marks.push(Object.assign({}, m, { x: m.x + pad, y: m.y + y, zero: m.zero === undefined ? undefined : m.zero + (m.axis === 'x' ? pad : y) })); });
      (sub.keys || []).forEach(function (k) { c.key(k); });
      sub.warnings.forEach(function (w) { c.warn(w); });
      y += ih + 18;
      c.line(pad, y, W - pad, y, { stroke: 'gridline', width: c.t('line-hairline'), mark: false });
      var s = c.text(pad, y + 20, c.labels.card_source || c.spec.source_line, { role: 'tick', fill: 'secondary', max: W - 2 * pad });
      c.height(s.y + s.h + pad);
    }
  });
})(globalThis.OAChart);
