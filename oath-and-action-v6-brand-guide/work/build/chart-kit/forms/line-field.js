/* Line field with highlight (coverage plan 3.3, extended; S27). Every series as a thin gray line on one scale, so the
 * reader sees the spread, and one series lit in ink with its name and latest value (or a few, where the title names a
 * near tie). A few other series may be named in gray at their ends, to mark the field's edges, and one series, such as the
 * nation, may be set apart as a dashed line in the text's ink (DR-64). The scale starts at zero; a line at the index
 * base, where the data has one, is drawn as a thin reference line in the secondary ink, named at its right end.
 * encode: x (year, month or date), y (number), series (category), label (text, optional: the series' name). labels: lit
 * (the series in ink, or a list of them), named (a list of series named in gray), apart (a series drawn dashed in the
 * text's ink and named at its end, such as "US"), end (words at a named line's end, with {name} and {y}), apart_end
 * (the same for the apart series), base (a y value drawn as the reference line, such as 100 for an index), base_end
 * (words at the reference line's right end), base_label (words over the value axis). formats: y (in the words), tick.
 * The time axis labels the last x and every k-th x back from it, the smallest k whose labels sit apart, so the run is
 * even (brand S15). Maker B, round 1. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'line-field',
    name: 'Line Field',
    family: 'change-over-time',
    encode: { x: 'time', y: 'number', series: 'category', label: 'text?' },
    labels: ['lit', 'named', 'apart', 'end', 'apart_end', 'base', 'base_end', 'base_label'],
    phone: 'same',
    draw: function (c) {
      var P = K.parts, L = c.labels, f = c.spec.formats || {}, W = c.width, ex = c.field('x'), ey = c.field('y'), es = c.field('series'), el = c.field('label', false);
      var by = {}, order = [];
      c.rows.forEach(function (r) { var k = String(r[es]); if (!by[k]) { by[k] = []; order.push(k); } by[k].push(r); });
      order.forEach(function (k) { by[k].sort(function (a, b) { return K.time(a[ex]) - K.time(b[ex]); }); });
      var ts = c.rows.map(function (r) { return K.time(r[ex]); }), tlo = Math.min.apply(null, ts), thi = Math.max.apply(null, ts);
      var vmax = Math.max.apply(null, c.rows.map(function (r) { return r[ey]; }));
      var vs = P.value_scale(c, 0, vmax, 5), ticks = vs.ticks;
      var lits = [].concat(L.lit === undefined || L.lit === null ? [] : L.lit).map(String), isLit = function (k) { return lits.indexOf(k) >= 0; };
      var apart = L.apart === undefined || L.apart === null ? null : String(L.apart);
      var named = lits.concat((L.named || []).map(String)).concat(apart !== null ? [apart] : []).filter(function (k) { return by[k]; });
      var endw = function (k) { var l = by[k][by[k].length - 1]; return String((k === apart && L.apart_end) || L.end || '{name}').replace('{name}', el ? l[el] : k).replace('{y}', K.fmt(l[ey], f.y || 'number:0')); };
      var maxw = Math.round(W * (c.phone ? 0.3 : 0.25)), lw = 0, lines = {};
      // a name and its figure never part: a line that would hold the figure alone takes the name's last word with it
      // (a one-word name keeps its figure on its own line, a little past the width)
      var keep_with = function (ls) {
        if (ls.length > 1 && !/[A-Za-z]/.test(ls[ls.length - 1])) {
          var w = ls[ls.length - 2].split(' '), fig = ls.pop();
          if (w.length > 1) { ls[ls.length - 1] = w.slice(0, -1).join(' '); ls.push(w[w.length - 1] + ' ' + fig); } else ls[ls.length - 1] += ' ' + fig;
        }
        return ls;
      };
      named.forEach(function (k) { var wt = isLit(k) ? 700 : 400; lines[k] = keep_with(c.wrap(endw(k), 'label', maxw, wt)); lines[k].forEach(function (l) { lw = Math.max(lw, c.measure(l, 'label', wt)); }); });
      var bw = L.base !== undefined && L.base_end ? c.measure(L.base_end, 'tick') : 0;
      lw = Math.max(lw, bw - 6);
      var head = L.base_label ? c.size('tick') + 10 : 0;
      if (L.base_label) c.text(0, c.size('tick'), L.base_label, { role: 'tick', weight: 600, max: W });
      var top = head + c.size('tick') + 6, plotH = c.t(c.phone ? 'columns-phone-height' : 'columns-height'), bot = top + plotH;
      var gut = P.value_gutter(c, ticks, f.tick || 'integer');
      var x0 = gut + 8, x1 = W - Math.ceil(lw) - 16;
      var ys = K.scale.linear([vs.lo, vs.hi], [bot, top]), xs = K.scale.linear([tlo, thi], [x0, x1]);
      P.value_grid(c, ys, ticks, f.tick || 'integer', x0, x1, gut);
      P.zero_line(c, ys, x0, x1);
      // the index base: a thin reference line in the secondary ink, so it never reads as a series (CD B-S2, brand S14)
      if (L.base !== undefined) c.line(x0, ys(L.base), x1, ys(L.base), { stroke: 'secondary', width: c.t('line-hairline'), mark: false });
      var path = function (k) { return by[k].map(function (r, i) { return (i ? 'L' : 'M') + K.round(xs(K.time(r[ex]))) + ',' + K.round(ys(r[ey])); }).join(''); };
      // the field in gray, the named gray lines a step darker, then the lit line on its keyline
      order.forEach(function (k) {
        if (isLit(k) || k === apart) return;
        var nm = named.indexOf(k) >= 0;
        c.path(path(k), { stroke: nm ? 'context' : 'ghost', width: nm ? c.t('spark-context') : c.t('line-hairline'), data: { series: k } }, [x0, top, x1 - x0, plotH]);
        by[k].forEach(function (r) { c.datum(xs(K.time(r[ex])), ys(r[ey]), { data: { key: k + '|' + r[ex], field: ey, value: r[ey] } }); });
      });
      // the series set apart: dashed, in the text's ink, at the field's weight on a keyline of the ground
      if (apart !== null && by[apart]) {
        c.path(path(apart), { stroke: 'surface', width: c.t('spark-context') + 2 * c.t('keyline'), mark: false });
        c.path(path(apart), { stroke: 'label', width: c.t('spark-context'), dash: '5 3', data: { series: apart } }, [x0, top, x1 - x0, plotH]);
        by[apart].forEach(function (r) { c.datum(xs(K.time(r[ex])), ys(r[ey]), { data: { key: apart + '|' + r[ex], field: ey, value: r[ey] } }); });
      } else if (apart !== null) c.warn('labels.apart names no series');
      if (!lits.some(function (k) { return by[k]; })) c.warn('labels.lit names no series');
      lits.forEach(function (k0) {
        if (!by[k0]) return;
        c.path(path(k0), { stroke: 'surface', width: c.t('line-subject') + 2 * c.t('keyline'), mark: false });
        c.path(path(k0), { stroke: 'subject', width: c.t('line-subject'), data: { series: k0 } }, [x0, top, x1 - x0, plotH]);
        by[k0].forEach(function (r) { c.datum(xs(K.time(r[ex])), ys(r[ey]), { data: { key: k0 + '|' + r[ex], field: ey, value: r[ey] } }); });
      });
      // the names at the ends, spread apart where they would touch
      var lh = Math.round(c.size('label') * 1.2), gap = 4;
      var labs = named.map(function (k) { var l = by[k][by[k].length - 1]; return { k: k, want: ys(l[ey]), h: lh * lines[k].length, last: l }; });
      if (L.base !== undefined && L.base_end) labs.push({ k: null, want: ys(L.base), h: lh, base: true });
      labs.sort(function (a, b) { return a.want - b.want; });
      labs.forEach(function (l) { l.y = l.want - l.h / 2; });
      for (var pass = 0; pass < 30; pass++) {
        var moved = false;
        for (var i = 1; i < labs.length; i++) { var o = labs[i - 1].y + labs[i - 1].h + gap - labs[i].y; if (o > 0.1) { labs[i - 1].y -= o / 2; labs[i].y += o / 2; moved = true; } }
        if (labs.length && labs[0].y < top - 6) { labs[0].y = top - 6; moved = true; }
        if (!moved) break;
      }
      labs.forEach(function (l) {
        var lx = x1 + 10, ly = l.y + c.size('label') * 0.85;
        if (l.base) { c.text(x1 + 6, l.y + c.size('label') * 0.75, L.base_end, { role: 'tick', fill: 'secondary' }); return; }
        var lit = isLit(l.k), ap = l.k === apart;
        c.circle(xs(K.time(l.last[ex])), ys(l.last[ey]), c.t(lit ? 'dot-vertex-radius' : 'dot-small-vertex-radius'), { fill: lit || ap ? 'subject' : 'context', mark: false });
        lines[l.k].forEach(function (ln, j) { c.text(lx, ly + j * lh, ln, { role: 'label', weight: lit ? 700 : 400, fill: lit || ap ? 'label' : 'secondary' }); });
      });
      // the time axis: a tick and a centered label at each x the rows hold, thinned to fit
      var ay = bot + c.size('tick') + 10, xsv = [];
      c.rows.forEach(function (r) { var t = K.time(r[ex]); if (xsv.indexOf(t) < 0) xsv.push(t); });
      xsv.sort(function (a, b) { return a - b; });
      // the last x keeps its label, and every k-th x back from it takes one, the smallest k whose labels sit apart, so the
      // labeled years run evenly (brand S15: 1991, 2001, 2011 and 2026 read as an uneven run)
      var box = function (t) { var word = String(Math.floor(t)), w = c.measure(word, 'tick'), x = xs(t), anchor = x + w / 2 > W ? 'end' : x - w / 2 < 0 ? 'start' : 'middle'; return { t: t, word: word, x: x, anchor: anchor, l: anchor === 'end' ? x - w : anchor === 'start' ? x : x - w / 2, r: anchor === 'end' ? x : anchor === 'start' ? x + w : x + w / 2 }; };
      var keep = [];
      for (var kk = 1; kk <= xsv.length; kk++) {
        var pick = [];
        for (var ii = xsv.length - 1; ii >= 0; ii -= kk) pick.push(box(xsv[ii]));
        if (pick.every(function (b, j) { return !j || b.r + 8 <= pick[j - 1].l; })) { keep = pick; break; }
      }
      xsv.forEach(function (t) { c.line(xs(t), bot + 1, xs(t), bot + 5, { stroke: 'baseline', width: c.t('line-hairline'), mark: false }); });
      keep.forEach(function (b) { c.text(b.x, ay, b.word, { role: 'tick', anchor: b.anchor }); });
      c.height(Math.max(ay + 4, labs.length ? labs[labs.length - 1].y + labs[labs.length - 1].h : 0));
    }
  });
})(globalThis.OAChart);
