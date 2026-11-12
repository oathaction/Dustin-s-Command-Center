/* Fan chart (coverage plan 3.7, extended; S59). A projection's median as a line in the subject ink with a dot and its
 * value at each period, over two nested bands (K.parts.band): the outer in magnitude step 1 and the inner in step 2, so
 * the fan reads from its middle outward in grayscale too. A key over the plot names the two bands and the line. The
 * outer band's two ends are printed at the last period. A period drawn apart (labels.apart, such as the longer run) sits
 * to the right of a thin rule, its median a dot and its inner band a whisker, since it has no date.
 * encode: x (category: the periods, years in order, and the one drawn apart), y (number: the median), outer_low and
 * outer_high (numbers), inner_low and inner_high (numbers, optional).
 * labels: apart (the x value drawn apart), apart_label (its words under the axis), key_outer, key_inner, key_median (the
 * key's words; an entry is left out when its words are), y_axis (words over the value axis).
 * history ({dataset, x, y}: where the measure stood before the projections, from the spec's second dataset, one dot a
 * period joined by a line in the subject ink at the field's weight, on the same axis of periods; a period with no value
 * breaks the line and takes a light column, named in the key), key_history and key_gap (their key words).
 * The two bands take 1 px edges in the context ink, since neither fill reaches 3 to 1 (the data lead's RF-2, round 2 fix
 * pass), and so do their key swatches.
 * formats: y (values and ticks unless tick is set), tick. scale: y ([lo, hi]). On a phone the same arrangement draws
 * narrower, the key wrapping to more rows. Maker B, round 2. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'fan-chart',
    name: 'Fan Chart',
    family: 'uncertainty-and-estimates',
    encode: { x: 'category', y: 'number', outer_low: 'number', outer_high: 'number', inner_low: 'number?', inner_high: 'number?' },
    labels: ['apart', 'apart_label', 'key_outer', 'key_inner', 'key_median', 'y_axis', 'history', 'key_history', 'key_gap'],
    interval: 'level',
    phone: 'same',
    draw: function (c) {
      var P = K.parts, L = c.labels, f = c.spec.formats || {}, W = c.width, ph = c.phone;
      var ex = c.field('x'), ey = c.field('y'), eol = c.field('outer_low'), eoh = c.field('outer_high'), eil = c.field('inner_low', false), eih = c.field('inner_high', false);
      var tick = c.size('tick'), size = c.size('label'), fy = f.y || 'number:1', ft = f.tick || 'integer';
      var apart = L.apart === undefined || L.apart === null ? null : String(L.apart);
      var main = c.rows.filter(function (r) { return String(r[ex]) !== apart; }), ap = c.rows.filter(function (r) { return String(r[ex]) === apart; })[0] || null;
      // the history before the projections, from the spec's second dataset (RF-20)
      var hc = L.history || null, hist = [];
      if (hc) {
        var hds = (c.extra || {})[hc.dataset];
        if (!hds) c.warn('labels.history names no second dataset: ' + hc.dataset);
        else hist = hds.slice().sort(function (a, b) { return +a[hc.x] - +b[hc.x]; }).filter(function (h) { return !main.length || +h[hc.x] < +main[0][ex]; });
      }
      var hv = function (h) { return typeof h[hc.y] === 'number' ? h[hc.y] : null; };
      var vals = [];
      c.rows.forEach(function (r) { [ey, eol, eoh, eil, eih].forEach(function (k) { if (k && typeof r[k] === 'number') vals.push(r[k]); }); });
      hist.forEach(function (h) { if (hv(h) !== null) vals.push(hv(h)); });
      var vs = P.value_scale(c, Math.min(0, Math.min.apply(null, vals)), Math.max.apply(null, vals), ph ? 4 : 5), ticks = vs.ticks;
      var y = 0;
      // the key over the plot
      var kents = [];
      if (hist.length && L.key_history) kents.push({ label: L.key_history, shape: 'line', stroke: 'subject', width: c.t('line-context') });
      if (L.key_outer) kents.push({ label: L.key_outer, fill: 'mag-1', edge: 'context' });
      if (L.key_inner && eil) kents.push({ label: L.key_inner, fill: 'mag-2', edge: 'context' });
      if (L.key_median) kents.push({ label: L.key_median, shape: 'line', stroke: 'subject', width: c.t('line-subject') });
      if (hist.some(function (h) { return hv(h) === null; }) && L.key_gap) kents.push({ label: L.key_gap, stroke: 'context', open: true, dash: '2 2' });
      if (kents.length) y += P.key(c, kents, 0, size, W) + 6;
      if (L.y_axis) { c.text(0, y + tick, L.y_axis, { role: 'tick', weight: 600, max: W }); y += tick + 8; }
      var top = y + tick, plotH = ph ? 240 : 300, bot = top + plotH;
      var gut = P.value_gutter(c, ticks, ft), x0 = gut + 8;
      var endw = Math.ceil(Math.max(c.measure(K.fmt(main[main.length - 1][eoh], fy), 'label', 600), c.measure(K.fmt(main[main.length - 1][eol], fy), 'label', 600)));
      var apw = ap ? Math.max(48, Math.ceil(c.measure(L.apart_label || apart, 'tick')) + 12) : 0;
      var x1 = W - (ap ? apw + 24 : 0) - endw - 10;
      var nh = hist.length, xs = K.scale.linear([0, Math.max(1, nh + main.length - 1)], [x0 + 16, x1]), ys = K.scale.linear([vs.lo, vs.hi], [bot, top]);
      var hx = function (j) { return xs(j); }, step = xs(1) - xs(0);
      // a history period with no value: a light column under the grid, as a line with a gap draws it (Rule 14.11)
      // (an empty column edged by a dashed hairline in the context ink, as its key swatch is, so no fill stands for a value
      // that does not exist)
      hist.forEach(function (h, j) { if (hv(h) === null) c.rect(K.round(hx(j) - step * 0.3) + 0.5, top + 0.5, Math.max(4, K.round(step * 0.6) - 1), bot - top - 1, { stroke: 'context', width: c.t('line-hairline'), dash: '2 2', data: { key: String(h[hc.x]), field: hc.y, gap: 'yes' } }); });
      P.value_grid(c, ys, ticks, ft, x0, W, gut);
      P.zero_line(c, ys, x0, W);
      var px = function (i) { return xs(i + nh); };
      // the two bands, the outer first
      var key = function (r) { return String(r[ex]); };
      P.band(c, main.map(function (r, i) { return { x: px(i), y0: ys(r[eol]), y1: ys(r[eoh]), key: key(r), low: r[eol], high: r[eoh] }; }), { fill: 'mag-1', edge: 'context', field_low: eol, field_high: eoh });
      if (eil && eih) P.band(c, main.map(function (r, i) { return { x: px(i), y0: ys(r[eil]), y1: ys(r[eih]), key: key(r), low: r[eil], high: r[eih] }; }), { fill: 'mag-2', edge: 'context', field_low: eil, field_high: eih });
      var vlab = [], vdots = [];   // the values over the dots, set after every dot: the ones a reader must have first, then the rest where they sit apart
      // the history: one dot a period joined in the subject ink at the field's weight, broken where a period has no value;
      // the last value printed always, the others where they sit apart
      if (hist.length) {
        var hrun = [], hruns = [];
        hist.forEach(function (h, j) { if (hv(h) === null) { if (hrun.length) hruns.push(hrun); hrun = []; } else hrun.push(j); });
        if (hrun.length) hruns.push(hrun);
        hruns.forEach(function (rn) { if (rn.length > 1) c.path(rn.map(function (j, q) { return (q ? 'L' : 'M') + K.round(hx(j)) + ',' + K.round(ys(hv(hist[j]))); }).join(''), { stroke: 'subject', width: c.t('line-context'), data: { series: 'history' } }, [x0, top, x1 - x0, plotH]); });
        var lastj = -1;
        hist.forEach(function (h, j) { if (hv(h) !== null) lastj = j; });
        hist.forEach(function (h, j) {
          if (hv(h) === null) return;
          c.circle(hx(j), ys(hv(h)), c.t('dot-vertex-radius'), { fill: 'subject', data: { key: String(h[hc.x]), field: hc.y, value: hv(h) } });
          vlab.push({ x: hx(j), y: ys(hv(h)) - 8, words: K.fmt(hv(h), fy), weight: 400, must: j === lastj });
          vdots.push({ x: hx(j), y: ys(hv(h)), r: c.t('dot-vertex-radius') + 1 });
        });
      }
      // the median: a line with a dot and its value at each period
      var d = main.map(function (r, i) { return (i ? 'L' : 'M') + K.round(px(i)) + ',' + K.round(ys(r[ey])); }).join('');
      c.path(d, { stroke: 'surface', width: c.t('line-subject') + 2 * c.t('keyline'), mark: false });
      c.path(d, { stroke: 'subject', width: c.t('line-subject') }, [x0, top, x1 - x0, plotH]);
      main.forEach(function (r, i) {
        c.circle(px(i), ys(r[ey]), c.t('dot-vertex-radius') + 1, Object.assign({ fill: 'subject', data: { key: key(r), field: ey, value: r[ey] } }));
        // a value whose words the outer band's edge would cross sits just over that edge (the data lead's MB-F3)
        var vy = ys(r[eih] !== undefined && eih ? Math.max(r[ey], r[eih]) : r[ey]) - 8, oy = ys(r[eoh]);
        if (oy > vy - tick - 2 && oy < vy + 4) vy = oy - 5;
        vlab.push({ x: px(i), y: vy, words: K.fmt(r[ey], fy), weight: 600, halo: true, must: i === 0 || i === main.length - 1 });
        vdots.push({ x: px(i), y: ys(r[ey]), r: c.t('dot-vertex-radius') + 2 });
      });
      var setl = [], lbox = function (v) { var w = c.measure(v.words, 'tick', v.weight); return { x: v.x - w / 2 - 3, y: v.y - tick, w: w + 6, h: tick + 2 }; };
      var clash = function (b) {
        return setl.some(function (t) { return b.x < t.x + t.w && t.x < b.x + b.w && b.y < t.y + t.h && t.y < b.y + b.h; }) ||
          vdots.some(function (q) { var nx = Math.max(b.x, Math.min(q.x, b.x + b.w)), ny = Math.max(b.y, Math.min(q.y, b.y + b.h)); return Math.pow(nx - q.x, 2) + Math.pow(ny - q.y, 2) < q.r * q.r; });
      };
      vlab.filter(function (v) { return v.must; }).concat(vlab.filter(function (v) { return !v.must; }).sort(function (a, b) { return a.x - b.x; })).forEach(function (v) {
        var b = lbox(v);
        if (!v.must && clash(b)) return;
        setl.push(b);
        c.text(v.x, v.y, v.words, { role: 'tick', weight: v.weight, anchor: 'middle', fill: 'label', halo: !!v.halo });
      });
      // the outer band's ends at the last period
      var lr = main[main.length - 1], lx = px(main.length - 1) + 8;
      c.text(lx, ys(lr[eoh]) + tick * 0.35, K.fmt(lr[eoh], fy), { role: 'label', weight: 600 });
      c.text(lx, ys(lr[eol]) + tick * 0.35, K.fmt(lr[eol], fy), { role: 'label', weight: 600 });
      // the period drawn apart, past a thin rule
      if (ap) {
        var rx = W - apw / 2, sep = W - apw - 12;
        c.line(sep, top - tick, sep, bot + 4, { stroke: 'gridline', width: c.t('line-hairline'), mark: false });
        if (eil && eih && typeof ap[eil] === 'number') P.whisker(c, ys(ap[eil]), ys(ap[eih]), rx, { dir: 'v', stroke: 'context', key: key(ap), low: ap[eil], high: ap[eih] });
        c.circle(rx, ys(ap[ey]), c.t('dot-vertex-radius') + 1, { fill: 'subject', data: { key: key(ap), field: ey, value: ap[ey] } });
        c.text(rx, ys(Math.max(ap[ey], eih && typeof ap[eih] === 'number' ? ap[eih] : ap[ey])) - 8, K.fmt(ap[ey], fy), { role: 'tick', weight: 600, anchor: 'middle', fill: 'label', halo: true });
      }
      // the periods along the bottom
      // the periods along the bottom: the last, and every k-th back from it that sits apart
      var slots = hist.map(function (h) { return String(h[hc.x]); }).concat(main.map(function (r) { return String(r[ex]); }));
      var ay = bot + tick + 10, n = slots.length, pick = [];
      for (var k = 1; k <= n; k++) {
        pick = slots.map(function (r, i) { return i; }).filter(function (i) { return (n - 1 - i) % k === 0; });
        if (pick.every(function (i, j) { return !j || xs(pick[j - 1]) + c.measure(slots[pick[j - 1]], 'tick') / 2 + 10 <= xs(i) - c.measure(slots[i], 'tick') / 2; })) break;
      }
      slots.forEach(function (sl, i) { c.line(xs(i), bot, xs(i), bot + 4, { stroke: 'baseline', width: c.t('line-hairline'), mark: false }); });
      pick.forEach(function (i) { c.text(xs(i), ay, slots[i], { role: 'tick', anchor: 'middle' }); });
      var end = ay + 4;
      if (ap) { var ab = c.text(W - apw / 2, ay, L.apart_label || apart, { role: 'tick', anchor: 'middle', max: apw + 10 }); end = Math.max(end, ab.bottom); }
      c.height(end + 2);
    }
  });
})(globalThis.OAChart);
