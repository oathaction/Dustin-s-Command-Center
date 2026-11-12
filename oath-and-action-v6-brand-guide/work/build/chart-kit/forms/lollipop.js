/* Lollipop (coverage plan 3.1, extended; S21). A ranked list drawn light: one thin stem per row from the zero line to a dot
 * at the value, the value printed past the dot and the name at the left (above the stem on a phone). Rows the title names
 * are set in ink, the rest in gray. A row the title names as its one point (labels.point) ends in the working red dot
 * with its keyline on Newsprint, on a stem in ink, and every other row takes the light fill on Newsprint and the context
 * ink on Charcoal (Rule 14.6, palette rule R3).
 * encode: category (text, the printed name), value (number), key (optional: the column labels.named matches; the
 * category otherwise). labels: named (a key or list set in ink; with none, every row is in ink), point (the one key in
 * red), categories ({category: printed name}). formats: value. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'lollipop',
    name: 'Lollipop',
    family: 'comparison',
    encode: { category: 'text', value: 'number', key: 'id?' },
    labels: ['named', 'point', 'categories'],
    phone: 'same',
    draw: function (c) {
      var rows = c.rows, ec = c.field('category'), ev = c.field('value'), ek = c.field('key', false) || ec;
      var f = c.spec.formats || {}, W = c.width, L = c.labels, names = L.categories || {};
      var pt = L.point === undefined || L.point === null ? null : String(L.point);
      var named = pt !== null ? [pt] : L.named === undefined ? null : [].concat(L.named).map(String);
      var ink = function (r) { return !named || named.indexOf(String(r[ek])) >= 0; };
      // with a red point, the shared part gives the other rows the light fill (R3); with none, the rows keep ink and gray
      var fill = pt !== null ? K.parts.named_fill(c, [pt], ek, null, pt) : null;
      var stem_fill = function (r) { return fill ? (fill.is_point(r) ? 'subject' : fill(r)) : ink(r) ? 'subject' : 'context'; };
      var dot_paint = function (r) { return fill ? Object.assign({ fill: fill(r) }, fill.keyline(r)) : { fill: ink(r) ? 'subject' : 'context' }; };
      var name = function (r) { return names[String(r[ec])] !== undefined ? names[String(r[ec])] : String(r[ec]); };
      var val = function (r) { return K.fmt(r[ev], f.value || 'integer'); };
      var size = c.size('label'), lh = Math.round(size * 1.25), rdot = c.t('dot-subject-radius');
      var lmax = c.phone ? W : Math.floor(W * 0.4), lw = 0, vw = 0;
      rows.forEach(function (r) {
        c.wrap(name(r), 'label', lmax, ink(r) ? 700 : 400).forEach(function (l) { lw = Math.max(lw, c.measure(l, 'label', ink(r) ? 700 : 400)); });
        vw = Math.max(vw, c.measure(val(r), 'label', 700, true));
      });
      var x0 = c.phone ? Math.ceil(c.t('line-baseline')) + 1 : Math.ceil(lw + 24);   // on a phone the zero line shows whole (DL-A2)
      var max = Math.max(0, Math.max.apply(null, rows.map(function (r) { return r[ev]; })));
      var xs = K.scale.linear([0, max], [x0, Math.max(x0 + 60, W - vw - rdot - 14)]), zx = xs(0);
      var pitch = c.phone ? Math.round(size * 1.25 + 2 * rdot + 14) : Math.max(Math.round(size * 1.9), 2 * rdot + 12);
      var y = c.phone ? size + 4 : rdot + 2, top = y, last = y;
      rows.forEach(function (r, i) {
        var lines = c.wrap(name(r), 'label', lmax, ink(r) ? 700 : 400).length;
        if (i) y = last + (c.phone ? pitch + (lines - 1) * lh : Math.max(pitch, lines * lh + 10));
        var cy = y, x = xs(r[ev]), on = ink(r);
        if (c.phone) c.text(0, cy - rdot - 6 - (lines - 1) * lh, name(r), { role: 'label', weight: on ? 700 : 400, max: lmax });
        else c.text(0, cy + size * 0.35 - (lines - 1) * lh / 2, name(r), { role: 'label', weight: on ? 700 : 400, max: lmax });
        // the stem is a bar one line wide, so the zero check reads it; the dot sits on its end
        var sw = c.t('line-context');
        c.rect(zx, cy - sw / 2, x - zx, sw, { fill: stem_fill(r), kind: 'bar', axis: 'x', zero: zx, data: { key: r[ek], field: ev, value: r[ev] } });
        c.circle(x, cy, rdot, Object.assign({ mark: false }, dot_paint(r)));
        c.text(x + rdot + 8, cy + size * 0.35, val(r), { role: 'label', weight: on ? 700 : 600, tnum: true });
        if (c.phone) c.line(zx, cy - rdot - 3, zx, cy + rdot + 3, { stroke: 'baseline', width: c.t('line-baseline'), mark: false });
        last = y;
      });
      if (!c.phone) c.line(zx, top - rdot - 4, zx, last + rdot + 4, { stroke: 'baseline', width: c.t('line-baseline'), mark: false });
      c.height(last + rdot + 6);
    }
  });
})(globalThis.OAChart);
