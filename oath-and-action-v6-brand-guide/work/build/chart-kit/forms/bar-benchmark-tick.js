/* Bar with a benchmark tick (coverage plan 3.1, core; S18). One bar per row from a zero line, with a tick across it at
 * the row's benchmark, such as a share of income against a share of households. The value prints at the bar's end, or
 * past the tick where it would touch it; the benchmark's words print once over the first tick when every row shares one
 * benchmark, else each tick prints its own value.
 * A value that would touch the tick prints inside its bar's end where it fits.
 * encode: category (text), value (number), benchmark (number). labels: benchmark (words over the first tick),
 * categories ({category: printed name}). formats: value, benchmark. On a phone each name sits above its bar. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'bar-benchmark-tick',
    name: 'Bar With Benchmark Tick',
    family: 'comparison',
    encode: { category: 'text', value: 'number', benchmark: 'number' },
    labels: ['benchmark', 'categories'],
    phone: 'same',
    draw: function (c) {
      var rows = c.rows, ek = c.field('category'), ev = c.field('value'), eb = c.field('benchmark');
      var f = c.spec.formats || {}, W = c.width, L = c.labels, names = L.categories || {};
      var name = function (r) { return names[String(r[ek])] !== undefined ? names[String(r[ek])] : String(r[ek]); };
      var val = function (r) { return K.fmt(r[ev], f.value || 'number:1'); };
      var size = c.size('label'), tick = c.size('tick');
      var bh = c.t(c.phone ? 'bar-phone-height' : 'bar-height'), pitch = c.t(c.phone ? 'bar-phone-pitch' : 'bar-pitch');
      var lmax = c.phone ? W : Math.floor(W * 0.36), lw = 0;
      rows.forEach(function (r) { c.wrap(name(r), 'label', lmax, 600).forEach(function (l) { lw = Math.max(lw, c.measure(l, 'label', 600)); }); });
      var x0 = c.phone ? 0 : Math.ceil(lw + 24);
      var bvals = rows.map(function (r) { return r[eb]; });
      var one = bvals.every(function (b) { return b === bvals[0]; });
      var hi = Math.max.apply(null, rows.map(function (r) { return Math.max(r[ev], r[eb]); }));
      var vw = 0;
      rows.forEach(function (r) { vw = Math.max(vw, c.measure(val(r), 'label', 700, true)); });
      var xs = K.scale.linear([0, hi], [x0, Math.max(x0 + 60, W - vw - 10)]), zx = xs(0);
      var y = 0;
      // the benchmark's words over the first tick, kept inside the artboard
      if (one && L.benchmark) {
        var bx = xs(bvals[0]), bw = c.measure(L.benchmark, 'tick', 600);
        var ax = Math.min(Math.max(bx, bw / 2), W - bw / 2);
        y = tick + 2;
        c.text(ax, y, L.benchmark, { role: 'tick', weight: 600, anchor: 'middle', fill: 'label' });
        y += c.phone ? 18 : 10;
      }
      var lh = Math.round(size * 1.25), by = y + (c.phone ? size + 6 : 6), top = by, bottom = by;
      var over = 5;   // the tick runs past the bar's edges by this much
      rows.forEach(function (r, i) {
        var lines = c.wrap(name(r), 'label', lmax, 600).length;
        if (i) by += c.phone ? Math.max(pitch, bh + 14 + lines * lh) : Math.max(pitch, lines * lh + 8);
        var cy = by + bh / 2, xe = xs(r[ev]), tx = xs(r[eb]);
        if (c.phone) c.text(0, by - 8 - (lines - 1) * lh, name(r), { role: 'label', weight: 600, max: lmax });
        else c.text(0, cy + size * 0.35 - (lines - 1) * lh / 2, name(r), { role: 'label', weight: 600, max: lmax });
        c.rect(zx, by, xe - zx, bh, { fill: 'subject', kind: 'bar', axis: 'x', zero: zx, data: { key: r[ek], field: ev, value: r[ev] } });
        // the tick: a ground-colored keyline under an ink line, so it reads across the bar and beyond it
        c.line(tx, by - over, tx, by + bh + over, { stroke: 'surface', width: c.t('line-subject') + 2 * c.t('keyline'), mark: false });
        c.line(tx, by - over, tx, by + bh + over, { stroke: 'subject', width: c.t('line-subject'), data: { key: r[ek], field: eb, value: r[eb] } });
        // the value at the bar's end, or past the tick where it would touch it
        // the value at the bar's end; where it would touch the tick, inside the bar's end if it fits, else past the tick
        var w = c.measure(val(r), 'label', 700, true), lx = xe + 8;
        if (lx < tx + 6 && lx + w > tx - 6) {
          if (w + 16 < xe - zx) c.text(xe - 8, cy + size * 0.35, val(r), { role: 'label', weight: 700, tnum: true, anchor: 'end', fill: 'label-on-subject' });
          else c.text(tx + 8, cy + size * 0.35, val(r), { role: 'label', weight: 700, tnum: true });
        } else c.text(lx, cy + size * 0.35, val(r), { role: 'label', weight: 700, tnum: true });
        if (!one) c.text(tx, by - over - 4, K.fmt(r[eb], f.benchmark || f.value || 'number:1'), { role: 'tick', anchor: 'middle' });
        // on a phone the zero line runs beside each bar only, never through the names above them
        if (c.phone) c.line(zx, by - 3, zx, by + bh + 3, { stroke: 'baseline', width: c.t('line-baseline'), mark: false });
        bottom = by + bh;
      });
      if (!c.phone) c.line(zx, top - over - 2, zx, bottom + over + 2, { stroke: 'baseline', width: c.t('line-baseline'), mark: false });
      c.height(bottom + over + 4);
    }
  });
})(globalThis.OAChart);
