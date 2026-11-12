/* Indexed line (coverage plan 3.3, core; S33). Many series on one scale as an index: each series' value divided by its own
 * value at the base date, times 100, so every line starts at 100 and a reader compares growth, never size. The base line
 * at 100 is a thin reference line in the secondary ink, named at its right end, so it never reads as a series (CD B-S2,
 * brand S14). Past four series (DR-234) one series takes the ink and the rest take gray. On a drawing 600 px or wider
 * every series is named at its end, the names spread apart where they would touch, with a short leader back to the line,
 * and a name never leaves its figure alone on a line. Under 600 px the plot takes the full width: the subject and the
 * second series are named in a key inside the plot's empty corner (above it where no corner is empty), and the other
 * series are listed under the plot with their latest index, highest first (CD BM1, Rule 14.12).
 * encode: x (year, month or date), y (number: the raw values), series (category). labels: base (the x value that is 100),
 * base_label (words over the value axis, naming the base), base_end (words at the base line's right end, wide drawings),
 * subject (the series in ink), second (a series in the context ink, such as the total, optional), names ({series: words}),
 * end (words at each line's end, with {name} and {index}), list_title (words over the list under a narrow plot).
 * formats: index (the index in the words, "integer" by default), tick. Maker B, round 1. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'indexed-line',
    name: 'Indexed Line',
    family: 'change-over-time',
    encode: { x: 'time', y: 'number', series: 'category' },
    labels: ['base', 'base_label', 'base_end', 'subject', 'second', 'names', 'end', 'list_title'],
    phone: 'differs',
    draw: function (c) {
      var P = K.parts, L = c.labels, f = c.spec.formats || {}, W = c.width, ex = c.field('x'), ey = c.field('y'), es = c.field('series');
      var by = {}, order = [];
      c.rows.forEach(function (r) { var k = String(r[es]); if (!by[k]) { by[k] = []; order.push(k); } by[k].push(r); });
      var series = order.map(function (k) {
        var list = by[k].slice().sort(function (a, b) { return K.time(a[ex]) - K.time(b[ex]); });
        var base = list.filter(function (r) { return String(r[ex]) === String(L.base); })[0] || list[0];
        return { key: k, name: (L.names || {})[k] || k, pts: list.map(function (r) { return { r: r, t: K.time(r[ex]), v: r[ey] / base[ey] * 100 }; }) };
      });
      var all = [];
      series.forEach(function (s) { s.pts.forEach(function (p) { all.push(p); }); });
      var vmax = Math.max.apply(null, all.map(function (p) { return p.v; }));
      var vs = P.value_scale(c, 0, vmax, 5), ticks = vs.ticks;
      var tlo = Math.min.apply(null, all.map(function (p) { return p.t; })), thi = Math.max.apply(null, all.map(function (p) { return p.t; }));
      // the end names: their width sets the plot's right edge; a name too wide for a third of the drawing wraps, and its
      // figure always keeps the name's last word beside it (CD BM1: "100" stood alone above the next name)
      var narrow = W < 600;
      var endw = function (s) { var last = s.pts[s.pts.length - 1]; return String(L.end || '{name}').replace('{name}', s.name).replace('{index}', K.fmt(last.v, f.index || 'integer')); };
      var rank = function (s) { return s.key === String(L.subject) ? 2 : s.key === String(L.second) ? 1 : 0; };
      var keep_with = function (ls) {
        if (ls.length > 1 && !/[A-Za-z]/.test(ls[ls.length - 1])) {
          var w = ls[ls.length - 2].split(' '), fig = ls.pop();
          if (w.length > 1) { ls[ls.length - 1] = w.slice(0, -1).join(' '); ls.push(w[w.length - 1] + ' ' + fig); } else ls[ls.length - 1] += ' ' + fig;
        }
        return ls;
      };
      var maxw = Math.round(W * 0.34), lw = 0;
      if (!narrow) series.forEach(function (s) { var wt = rank(s) ? 700 : 400; s.lines = keep_with(c.wrap(endw(s), 'label', maxw, wt)); s.lines.forEach(function (l) { lw = Math.max(lw, c.measure(l, 'label', wt)); }); });
      if (!narrow && L.base_end) lw = Math.max(lw, c.measure(L.base_end, 'tick') - 4);
      // the base's words head the value axis, above the plot
      var head = L.base_label ? c.size('tick') + 10 : 0;
      if (L.base_label) c.text(0, c.size('tick'), L.base_label, { role: 'tick', weight: 600, max: W });
      var top = head + c.size('tick') + 6, plotH = c.t(c.phone ? 'columns-phone-height' : 'columns-height'), bot = top + plotH;
      var gut = P.value_gutter(c, ticks, f.tick || 'integer');
      var x0 = gut + 8, x1 = narrow ? W - 8 : W - Math.ceil(lw) - 22;
      var ys = K.scale.linear([vs.lo, vs.hi], [bot, top]), xs = K.scale.linear([tlo, thi], [x0, x1]);
      // narrow: the key of the inked series, in the plot's upper left where no line passes, or above the plot
      var keyed = narrow ? series.filter(function (s) { return rank(s); }).sort(function (a, b) { return rank(b) - rank(a); }) : [];
      var klh = Math.round(c.size('label') * 1.45), ksw = 22, kbox = null;
      if (keyed.length) {
        var kw = 0;
        keyed.forEach(function (s) { kw = Math.max(kw, ksw + 8 + c.measure(endw(s), 'label', 700)); });
        var kh = klh * keyed.length, kx = x0 + 10;
        var clear = function (bx, by, bw, bh) {
          return series.every(function (s) {
            for (var i = 1; i < s.pts.length; i++) {
              var ax = xs(s.pts[i - 1].t), ay2 = ys(s.pts[i - 1].v), bx2 = xs(s.pts[i].t), by2 = ys(s.pts[i].v), n = Math.ceil(Math.max(Math.abs(bx2 - ax), Math.abs(by2 - ay2)));
              for (var j = 0; j <= n; j++) { var px = ax + (bx2 - ax) * j / (n || 1), py = ay2 + (by2 - ay2) * j / (n || 1); if (px > bx - 6 && px < bx + bw + 6 && py > by - 6 && py < by + bh + 6) return false; }
            }
            return true;
          });
        };
        if (kx + kw <= x1 && clear(kx, top + 6, kw, kh)) kbox = { x: kx, y: top + 6 };
        else {
          kbox = { x: 0, y: top };
          top += kh + 8; bot = top + plotH;
          ys = K.scale.linear([vs.lo, vs.hi], [bot, top]);
        }
      }
      P.value_grid(c, ys, ticks.filter(function (t) { return t !== 100; }), f.tick || 'integer', x0, x1, gut);
      P.zero_line(c, ys, x0, x1);
      // the base line at 100: a thin reference line in the secondary ink, with its figure in the gutter
      c.line(x0, ys(100), x1, ys(100), { stroke: 'secondary', width: c.t('line-hairline'), mark: false });
      c.text(gut, ys(100) + c.size('tick') * 0.35, K.fmt(100, f.tick || 'integer'), { role: 'tick', anchor: 'end', tnum: true });
      // the lines: gray first, then the second series, then the subject on top
      var drawn = series.slice().sort(function (a, b) { return rank(a) - rank(b); });
      drawn.forEach(function (s) {
        var d = s.pts.map(function (p, i) { return (i ? 'L' : 'M') + K.round(xs(p.t)) + ',' + K.round(ys(p.v)); }).join('');
        var rk = rank(s), stroke = rk === 2 ? 'subject' : rk === 1 ? 'context' : 'ghost', w = rk === 2 ? c.t('line-subject') : rk === 1 ? c.t('line-context') : c.t('spark-context');
        if (rk) c.path(d, { stroke: 'surface', width: w + 2 * c.t('keyline'), mark: false });
        c.path(d, { stroke: stroke, width: w, data: { series: s.key } }, [x0, top, x1 - x0, plotH]);
        s.pts.forEach(function (p) { c.datum(xs(p.t), ys(p.v), { data: { key: s.key + '|' + p.r[ex], field: 'index', value: Math.round(p.v * 10) / 10 } }); });
        var last = s.pts[s.pts.length - 1];
        c.circle(xs(last.t), ys(last.v), rk ? c.t('dot-vertex-radius') : c.t('dot-small-vertex-radius'), { fill: rk === 2 ? 'subject' : 'context', mark: false });
      });
      // narrow: the key, each entry a short line in its series' ink and weight, and its name and latest index
      if (kbox) keyed.forEach(function (s, i) {
        var rk = rank(s), ky = kbox.y + i * klh + klh / 2;
        c.line(kbox.x, ky, kbox.x + ksw, ky, { stroke: rk === 2 ? 'subject' : 'context', width: rk === 2 ? c.t('line-subject') : c.t('line-context'), mark: false });
        c.text(kbox.x + ksw + 8, ky + c.size('label') * 0.35, endw(s), { role: 'label', weight: 700, halo: true });
      });
      // the end names, spread so none touches the next, each kept inside the plot's height (wide drawings)
      var lh = Math.round(c.size('label') * 1.2);
      var labs = narrow ? [] : series.map(function (s) {
        var lines = s.lines, last = s.pts[s.pts.length - 1];
        return { s: s, lines: lines, want: ys(last.v), h: lh * lines.length, rk: rank(s) };
      });
      if (!narrow && L.base_end) labs.push({ base: true, want: ys(100), h: lh, lines: [] });
      labs.sort(function (a, b) { return a.want - b.want; });
      var gap = 3;
      labs.forEach(function (l) { l.y = l.want - l.h / 2; });
      for (var pass = 0; labs.length && pass < 40; pass++) {
        var moved = false;
        for (var i = 1; i < labs.length; i++) {
          var over = labs[i - 1].y + labs[i - 1].h + gap - labs[i].y;
          if (over > 0.1) { labs[i - 1].y -= over / 2; labs[i].y += over / 2; moved = true; }
        }
        if (labs[0].y < 0) { labs[0].y = 0; moved = true; }
        // the names stay above the axis while they fit there; a taller stack runs on below it
        var lz = labs[labs.length - 1], total = labs.reduce(function (a, l) { return a + l.h + gap; }, 0);
        if (total <= bot + 6 && lz.y + lz.h > bot + 6) { lz.y = bot + 6 - lz.h; moved = true; }
        if (!moved) break;
      }
      var lx = x1 + 14;
      labs.forEach(function (l) {
        if (l.base) { c.text(x1 + 8, l.y + c.size('label') * 0.75, L.base_end, { role: 'tick', fill: 'secondary' }); return; }
        var last = l.s.pts[l.s.pts.length - 1], ly = l.y + c.size('label') * 0.85;
        l.lines.forEach(function (ln, k) { c.text(lx, ly + k * lh, ln, { role: 'label', weight: l.rk ? 700 : 400, fill: l.rk ? 'label' : 'secondary' }); });
        var cy = l.y + l.h / 2 - 2;
        if (Math.abs(cy - ys(last.v)) > 3) c.line(xs(last.t) + 4, ys(last.v), lx - 3, ly - c.size('label') * 0.32, { stroke: 'leader', width: c.t('line-hairline'), mark: false });
      });
      // the time axis
      // the time axis: a tick at each label, centered under it, thinned to fit and ending on the last x when it can
      var ay = bot + c.size('tick') + 10, span = Math.round(thi - tlo), wmax = c.measure('0000', 'tick') + 14, step = null;
      [1, 2, 3, 4, 5, 10, 20].forEach(function (st) { if (step === null && xs(tlo + st) - xs(tlo) >= wmax && span % st === 0) step = st; });
      if (step === null) [1, 2, 3, 4, 5, 10, 20].forEach(function (st) { if (step === null && xs(tlo + st) - xs(tlo) >= wmax) step = st; });
      for (var yr = Math.ceil(tlo - 1e-9); yr <= thi + 1e-9; yr += step || 1) {
        c.line(xs(yr), bot + 1, xs(yr), bot + 5, { stroke: 'baseline', width: c.t('line-hairline'), mark: false });
        var hw2 = c.measure(String(yr), 'tick') / 2, edge = xs(yr) + hw2 > x1 + 6;
        c.text(edge ? x1 + 6 : xs(yr), ay, String(yr), { role: 'tick', anchor: edge ? 'end' : 'middle' });
      }
      var end = Math.max(ay + 4, labs.length ? labs[labs.length - 1].y + labs[labs.length - 1].h : 0);
      // narrow: the other series under the plot, highest latest index first, each name with its figure on one row
      if (narrow) {
        var rest = series.filter(function (s) { return !rank(s); }).sort(function (a, b) { return b.pts[b.pts.length - 1].v - a.pts[a.pts.length - 1].v; });
        var ry = ay + 22, rlh = Math.round(c.size('label') * 1.45);
        if (L.list_title && rest.length) { var lt = c.text(0, ry + c.size('tick'), L.list_title, { role: 'tick', weight: 600, max: W }); ry = lt.bottom + 6; }
        rest.forEach(function (s) {
          var last = s.pts[s.pts.length - 1], fig = K.fmt(last.v, f.index || 'integer'), fw = c.measure(fig, 'label', 400, true);
          var nl = c.wrap(s.name, 'label', W - fw - 16, 400);
          c.text(0, ry + c.size('label'), s.name, { role: 'label', max: W - fw - 16 });
          c.text(W, ry + c.size('label') + (nl.length - 1) * Math.round(c.size('label') * 1.25), fig, { role: 'label', anchor: 'end', tnum: true });
          ry += rlh + (nl.length - 1) * Math.round(c.size('label') * 1.25);
        });
        end = Math.max(end, ry + 2);
      }
      c.height(end);
    }
  });
})(globalThis.OAChart);
