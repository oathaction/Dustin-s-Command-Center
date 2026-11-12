/* Stacked area (coverage plan 3.4, extended; S46). Up to four parts of a whole over time, stacked as bands from the zero
 * line in a fixed order, the first at the bottom; drawn as shares of each period's total ('expand') or as amounts
 * ('zero'). The bands take the categorical inks in DR-236's order (Charcoal, Verdigris, Prussian, then Stone, always
 * hatched). Each band is named inside itself at its right end, and its last share prints past the right edge.
 * encode: x (year), parts (list of number columns, the first at the bottom).
 * labels: parts ([{field, label, at}]: at, optional, is an x value over which the band's name is centered), offset ('expand' or 'zero'),
 * end_words ('{v}' words printed at each band's right end), x_ticks (x values to label). formats: y_tick, end. */
(function (K) {
  'use strict';
  var CAT = ['cat-1', 'cat-2', 'cat-3', 'cat-4'];
  K.register_chart({
    form: 'stacked-area', name: 'Stacked Area', family: 'composition',
    encode: { x: 'time', parts: 'list' },
    labels: ['parts', 'offset', 'end_words', 'x_ticks'],
    phone: 'same',
    draw: function (c) {
      var P = K.parts, ex = c.field('x'), parts = c.field('parts'), L = c.labels, f = c.spec.formats || {}, W = c.width, R = K.round;
      if (parts.length > 4) c.warn('more than four parts: split into small multiples (DR-234)');
      var defs = {}; (L.parts || []).forEach(function (d) { defs[d.field] = d; });
      var rows = c.rows.slice().sort(function (a, b) { return K.time(a[ex]) - K.time(b[ex]); });
      var offset = L.offset || 'expand', st = P.stack(rows, parts, { offset: offset === 'zero' ? 'zero' : 'expand' });
      var size = c.size('label'), tick = c.size('tick'), lh = Math.round(size * 1.2);
      var vs = offset === 'zero' ? P.value_scale(c, 0, st.hi, 5) : { lo: 0, hi: 100, ticks: [0, 25, 50, 75, 100] };
      var fmt = f.y_tick || (offset === 'zero' ? 'integer' : 'percent:0');
      var endw = function (g) { return String(L.end_words || '{v}').split('{v}').join(K.fmt(offset === 'zero' ? g.value : g.share, f.end || 'percent:0')); };
      var last = st[st.length - 1], ew = 0;
      last.segs.forEach(function (g) { ew = Math.max(ew, c.measure(endw(g), 'label', 700, true)); });
      var top = Math.round(tick * 0.6), plotH = c.t(c.phone ? 'columns-phone-height' : 'columns-height'), bot = top + plotH;
      var gut = P.value_gutter(c, vs.ticks, fmt), x0 = gut + 10, x1 = W - ew - 10;
      var ys = K.scale.linear([vs.lo, vs.hi], [bot, top]), xs = K.scale.linear([K.time(rows[0][ex]), K.time(last.row[ex])], [x0, x1]);
      var X = function (s) { return xs(K.time(s.row[ex])); };
      c.pattern('hatch', 'cat-4');
      // each band as one closed path, its upper edge left to right and its lower edge back
      parts.forEach(function (p, j) {
        var up = st.map(function (s) { return R(X(s)) + ',' + R(ys(s.segs[j].end)); });
        var dn = st.slice().reverse().map(function (s) { return R(X(s)) + ',' + R(ys(s.segs[j].start)); });
        var d = 'M' + up.join('L') + 'L' + dn.join('L') + 'Z', hatch = CAT[Math.min(j, 3)] === 'cat-4';
        c.path(d, hatch ? { pattern: 'hatch', mark: false } : { fill: CAT[j], mark: false }, [x0, top, x1 - x0, plotH]);
        // a hairline of the ground between bands keeps each edge crisp
        c.path('M' + up.join('L'), { fill: 'none', stroke: 'surface', width: c.t('line-hairline'), mark: false });
        st.forEach(function (s) { var g = s.segs[j]; if (!g.missing) c.datum(X(s), ys((g.start + g.end) / 2), { data: { key: s.row[ex], field: p, value: g.value } }); });
      });
      P.value_grid(c, ys, vs.ticks, fmt, x0 - 4, x0, gut);
      P.zero_line(c, ys, x0, x1);
      // the band names inside each band at its right end, flush right (or centered over labels.parts[].at); group 4's on a
      // plate of the ground over its hatch
      parts.forEach(function (p, j) {
        var dfn = defs[p] || {}, lab = dfn.label || p, at = dfn.at !== undefined ? st.filter(function (s) { return String(s.row[ex]) === String(dfn.at); })[0] : last;
        if (!at) { c.warn('labels.parts.at matches no row for ' + p); return; }
        var g = at.segs[j], hgt = ys(g.start) - ys(g.end), mw = Math.max(60, (x1 - x0) * 0.42), lines = c.wrap(lab, 'label', mw, 600);
        var hatch = CAT[Math.min(j, 3)] === 'cat-4', end = dfn.at === undefined, ax = end ? x1 - 8 : X(at);
        var cy = (ys(g.start) + ys(g.end)) / 2 - (lines.length - 1) * lh / 2 + size * 0.35;
        if (hgt < lines.length * lh + 4) c.warn('the band ' + p + ' is too thin for its name');
        // on the hatch, a plate of the ground knocks the strokes out from behind the words, 5 px clear of them (BC S7)
        if (hatch) {
          var tw = 0; lines.forEach(function (ln) { tw = Math.max(tw, c.measure(ln, 'label', 600)); });
          var bx = end ? ax - tw : ax - tw / 2, bt = cy - 0.864 * size, bb = cy + (lines.length - 1) * lh + 0.136 * size;
          c.rect(bx - 5, bt - 5, tw + 10, bb - bt + 10, { fill: 'surface', mark: false });
        }
        c.text(ax, cy, lab, { role: 'label', weight: 600, anchor: end ? 'end' : 'middle', max: mw + 1, leading: lh,
          fill: hatch ? 'beside-cat-4' : 'on-' + CAT[j] });
      });
      // each band's last share at the right edge, at its middle, moved apart where two would touch
      var ends = last.segs.map(function (g, j) { return { y: ys((g.start + g.end) / 2) + size * 0.35, g: g, j: j }; }).sort(function (a, b) { return a.y - b.y; });
      for (var k = 1; k < ends.length; k++) if (ends[k].y - ends[k - 1].y < lh) ends[k].y = ends[k - 1].y + lh;
      ends.forEach(function (e) { c.text(x1 + 8, e.y, endw(e.g), { role: 'label', weight: 700, tnum: true }); });
      // the time axis
      var t0 = K.time(rows[0][ex]), t1 = K.time(last.row[ex]), ay = bot + tick + 10, picks = L.x_ticks;
      if (!picks) {
        var wmax = c.measure('0000', 'tick') + 16, step = [1, 2, 5, 10, 20, 25, 50].filter(function (s) { return xs(t0 + s) - xs(t0) >= wmax; })[0] || 50;
        picks = []; for (var yr = Math.ceil(t0 / step) * step; yr <= t1; yr += step) picks.push(yr);
      }
      picks.forEach(function (p) {
        var x = xs(K.time(p)), w = c.measure(String(p), 'tick'), tx = Math.max(w / 2, Math.min(W - w / 2, x));
        c.line(x, bot + 1, x, bot + 5, { stroke: 'baseline', width: c.t('line-hairline'), mark: false });
        c.text(tx, ay, K.fmt(p, 'year'), { role: 'tick', anchor: 'middle' });
      });
      c.height(ay + 4);
    }
  });
})(globalThis.OAChart);
