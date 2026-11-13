/* Icon array (coverage plan 3.8, core; S85). A share as people out of 100: one plain unit mark for each person, in rows of
 * ten read from the top left, filled for those counted and open for the rest (DR-266), so "one in ten" can be counted. The
 * share prints as whole people (10 of 100) and the table prints the published figure. A topic symbol, a Civic Line drawing
 * at 48 px with its word beside it, heads the drawing where the spec names one (Rules 10.4, 10.6), and means its topic only.
 * encode: value (number: the share, in percent of the whole), category (text, optional: the row's name).
 * labels: draw ({column: value, ...}: the row the array draws; the first row by default), total (marks in all, default 100),
 * per_row (marks a row, default 10), filled and open (the key's words beside each kind of mark, {n} its count), topic
 * ({id, words}). The counted marks take the subject ink (an area form spends no red, RF-1); the rest are open, a 1 px edge in
 * the context ink and no fill (RF-2). */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'icon-array', name: 'Icon Array', family: 'proportion-and-overlap',
    encode: { value: 'number', category: 'text?' },
    labels: ['draw', 'total', 'per_row', 'filled', 'open', 'topic'],
    phone: 'same',
    draw: function (c) {
      var L = c.labels, W = c.width, ev = c.field('value'), ec = c.field('category', false);
      var all = c.all_rows || c.rows, want = L.draw || null;
      var row = want ? all.filter(function (r) { return Object.keys(want).every(function (k) { return String(r[k]) === String(want[k]); }); })[0] : all[0];
      if (!row) { c.warn('labels.draw matches no row'); c.height(10); return; }
      var tot = L.total || 100, per = L.per_row || 10, n = Math.round(+row[ev] / 100 * tot);
      if (!(n >= 0 && n <= tot)) { c.warn('the share ' + row[ev] + ' is not between 0 and 100 percent'); c.height(10); return; }
      var rowsN = Math.ceil(tot / per), y = 0;
      // the topic: the drawing at 48 px, its word beside it, read once (Rule 10.6: the drawing is hidden from screen readers)
      if (L.topic) {
        var ic = 48;
        if (!(K.parts.icon)) c.warn('labels.topic names ' + L.topic.id + ', and the kit has no part that draws a Civic Line drawing yet');
        else K.parts.icon(c, L.topic.id, 0, y, ic);
        c.text(ic + 12, y + ic / 2 + c.size('label') * 0.35, L.topic.words, { role: 'label', weight: 600, max: W - ic - 12 });
        y += ic + 18;
      }
      // the marks: the unit chart's own steps, larger, so a hundred stay countable; a row of ten fits the column on a phone
      var gap = c.phone ? c.t('unit-gap') : c.t('unit-gap') + 1;
      var u = Math.max(c.t('unit-size'), Math.min(c.phone ? 22 : 24, Math.floor((W + gap) / per) - gap));
      var gw = per * (u + gap) - gap, gh = rowsN * (u + gap) - gap;
      var top = y;
      for (var i = 0; i < tot; i++) {
        var x = (i % per) * (u + gap), yy = top + Math.floor(i / per) * (u + gap), on = i < n;
        var d = { key: (on ? 'counted ' : 'rest ') + (i + 1), field: ev, value: row[ev] };
        if (on) c.rect(x, yy, u, u, { fill: 'subject', kind: 'unit', data: d });
        else c.rect(x + 0.5, yy + 0.5, u - 1, u - 1, { fill: 'none', stroke: 'context', width: 1, kind: 'unit', data: d });
      }
      // words for each kind of mark, each with its swatch: beside the first row of its marks at a desk, under the marks on a phone
      var fw = String(L.filled || '{n}').split('{n}').join(K.fmt(n, 'integer'));
      var ow = String(L.open || '{n}').split('{n}').join(K.fmt(tot - n, 'integer'));
      var sw = 12, lx = gw + 20, side = !c.phone && W - lx >= 200;
      var words = function (x0, base, txt, on, max) {
        var t0 = base - c.size('label') * 0.35 - sw / 2;
        if (on) c.rect(x0, t0, sw, sw, { fill: 'subject', mark: false });
        else c.rect(x0 + 0.5, t0 + 0.5, sw - 1, sw - 1, { fill: 'none', stroke: 'context', width: 1, mark: false });
        return c.text(x0 + sw + 8, base, txt, { role: 'label', weight: on ? 600 : 400, max: max - sw - 8 });
      };
      var bottom = top + gh;
      if (side) {
        var r1 = Math.floor(Math.max(0, n - 1) / per), r2 = Math.floor(Math.min(tot - 1, n) / per);
        var b1 = top + r1 * (u + gap) + u / 2 + c.size('label') * 0.35;
        var b2 = top + r2 * (u + gap) + u / 2 + c.size('label') * 0.35;
        var t1 = n ? words(lx, b1, fw, true, W - lx) : null;
        if (t1 && b2 < t1.bottom + 8) b2 = t1.bottom + 8 + c.size('label') * 0.7;
        if (tot - n) { var t2 = words(lx, b2, ow, false, W - lx); bottom = Math.max(bottom, t2.bottom); }
        if (t1) bottom = Math.max(bottom, t1.bottom);
      } else {
        var by = bottom + 20 + c.size('label') * 0.7;
        if (n) { var p1 = words(0, by, fw, true, W); by = p1.bottom + 10 + c.size('label') * 0.7; bottom = p1.bottom; }
        if (tot - n) { var p2 = words(0, by, ow, false, W); bottom = p2.bottom; }
      }
      // the open marks are told apart by their edge, so the lightness test reads the filled marks alone
      c.key([{ fill: 'subject', direct: true }, { fill: 'context', pattern: true, direct: true }]);
      c.height(bottom + 6);
    }
  });
})(globalThis.OAChart);
