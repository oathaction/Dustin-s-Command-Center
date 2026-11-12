/* Ranked register (coverage plan 3.15, core; S36). A sorted list a reader scans: the rank, the name with a second line
 * under it, the amount right-aligned in figures of one width, and a thin bar from zero for each amount, under a row of
 * column heads, with hairlines between rows. On a phone the bar runs under the name. Rows the title names print bold and
 * keep their bar in ink; the other bars take the light fill on Newsprint and the context ink on Charcoal (palette rule R3).
 * encode: rank (integer), name (text), value (number), sub (category, optional: the second line).
 * labels: heads ({rank, name, value}: the column heads), names ({name: printed name}), subs ({sub value: printed words}),
 * divide (a number each value is divided by before it prints, such as 1000000), prefix and suffix (words around each
 * printed value, such as "$" and " million"), named (names printed bold). formats: value (after divide). */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'ranked-register',
    name: 'Ranked Register',
    family: 'tables-and-plain-words',
    encode: { rank: 'integer', name: 'text', value: 'number', sub: 'category?' },
    labels: ['heads', 'names', 'subs', 'divide', 'prefix', 'suffix', 'named'],
    phone: 'same',
    draw: function (c) {
      var rows = c.rows, er = c.field('rank'), en = c.field('name'), ev = c.field('value'), es = c.field('sub', false);
      var f = c.spec.formats || {}, W = c.width, L = c.labels, H = L.heads || {}, names = L.names || {}, subs = L.subs || {};
      var named = [].concat(L.named || []).map(String);
      var bold = function (r) { return named.indexOf(String(r[en])) >= 0; };
      var name = function (r) { return names[String(r[en])] !== undefined ? names[String(r[en])] : String(r[en]); };
      var sub = function (r) { if (!es || r[es] === null || r[es] === undefined) return ''; return subs[String(r[es])] !== undefined ? subs[String(r[es])] : String(r[es]); };
      var div = +L.divide || 1;
      var val = function (r) { return (L.prefix || '') + K.fmt(r[ev] / div, f.value || 'number:1') + (L.suffix || ''); };
      var size = c.size('label'), tick = c.size('tick'), lh = Math.round(size * 1.25), slh = Math.round(tick * 1.3);
      var rw = H.rank ? c.measure(H.rank, 'tick', 600) : 0, vw = c.measure(H.value || '', 'tick', 600);
      rows.forEach(function (r) { rw = Math.max(rw, c.measure(String(r[er]), 'label', 400, true)); vw = Math.max(vw, c.measure(val(r), 'label', 600, true)); });
      var xr = Math.ceil(rw + 12);
      // desktop: rank | name and sub | value | bar; phone: rank | name and sub | value, the bar under the name
      var barw = c.phone ? 0 : Math.max(80, Math.floor(W * 0.22));
      var xv = W - barw - (c.phone ? 0 : 16);
      var namew = xv - vw - 16 - xr;
      var max = Math.max.apply(null, rows.map(function (r) { return r[ev]; }));
      var xb0 = c.phone ? xr : W - barw, xs = K.scale.linear([0, max], [xb0, (c.phone ? xr + namew : W) - 8]);
      var fill = K.parts.named_fill(c, L.named, en);   // palette rule R3 (DR-236), the kit's shared part
      // the heads
      var y = tick + 2;
      if (H.rank) c.text(xr - 12, y, H.rank, { role: 'tick', weight: 600, anchor: 'end', fill: 'label' });
      if (H.name) c.text(xr, y, H.name, { role: 'tick', weight: 600, fill: 'label' });
      if (H.value) c.text(xv, y, H.value, { role: 'tick', weight: 600, anchor: 'end', fill: 'label' });
      y += 8;
      c.line(0, y, W, y, { stroke: 'baseline', width: c.t('line-hairline'), mark: false });
      var pad = 9, bh = 4;
      rows.forEach(function (r, i) {
        var b = bold(r), lines = c.wrap(name(r), 'label', namew, b ? 700 : 600).length;
        var base = y + pad + size;
        c.text(xr - 12, base, String(r[er]), { role: 'label', anchor: 'end', tnum: true, fill: 'secondary' });
        c.text(xr, base, name(r), { role: 'label', weight: b ? 700 : 600, max: namew });
        c.text(xv, base, val(r), { role: 'label', weight: b ? 700 : 600, anchor: 'end', tnum: true });
        var last = base + (lines - 1) * lh;
        if (sub(r)) { last += slh; c.text(xr, last, sub(r), { role: 'tick', fill: 'secondary' }); }
        if (c.phone) {
          var byy = last + 8;
          c.rect(xs(0), byy, xs(r[ev]) - xs(0), bh, { fill: fill(r), kind: 'bar', axis: 'x', zero: xs(0), data: { key: r[en], field: ev, value: r[ev] } });
          last = byy + bh;
        } else {
          c.rect(xs(0), base - size * 0.35 - bh / 2 - 2, xs(r[ev]) - xs(0), bh + 4, { fill: fill(r), kind: 'bar', axis: 'x', zero: xs(0), data: { key: r[en], field: ev, value: r[ev] } });
        }
        y = last + pad;
        c.line(0, y, W, y, { stroke: i === rows.length - 1 ? 'baseline' : 'gridline', width: c.t(i === rows.length - 1 ? 'line-baseline' : 'line-hairline'), mark: false });
      });
      c.height(y + 2);
    }
  });
})(globalThis.OAChart);
