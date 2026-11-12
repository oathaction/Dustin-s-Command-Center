/* Small-multiple area sparklines (coverage plan 3.3, core; S13) and the sparkline table (3.15, core; S13's totals rows).
 * area-sparklines: one panel per series on one shared vertical scale, the area from zero, a gray line of the context series
 * in every panel, an end label with the change. sparkline-table: one row per series with its sparkline and the last row's
 * figures in columns.
 * encode: x (month), y (number), series (category), and for the table, columns (list of columns printed from the last row).
 * labels: panels ([{value, label}] in order), context (the series drawn gray in every panel), context_label, end (words with
 * {name} placeholders from the last row), domain ([lo, hi]), columns_titles (for the table). formats: by column name. */
(function (K) {
  'use strict';
  function series(c) {
    var rows = c.rows, ex = c.field('x'), es = c.field('series'), by = {};
    rows.forEach(function (r) { (by[String(r[es])] = by[String(r[es])] || []).push(r); });
    Object.keys(by).forEach(function (k) { by[k].sort(function (a, b) { return K.time(a[ex]) - K.time(b[ex]); }); });
    return by;
  }
  function spark(c, list, ctx, xs, ys, o) {
    var ex = c.field('x'), ey = c.field('y');
    var pts = list.map(function (r) { return [xs(K.time(r[ex])), ys(r[ey])]; });
    // the area first, then the context series' gray line over it, then the series' own line: the line the key promises
    // shows in every panel (KM3)
    if (o.area) c.path('M' + K.round(pts[0][0]) + ',' + K.round(ys(0)) + pts.map(function (p) { return 'L' + K.round(p[0]) + ',' + K.round(p[1]); }).join('') + 'L' + K.round(pts[pts.length - 1][0]) + ',' + K.round(ys(0)) + 'Z', { fill: 'band', mark: false });
    if (ctx) c.path(ctx.map(function (r, i) { return (i ? 'L' : 'M') + K.round(xs(K.time(r[ex]))) + ',' + K.round(ys(r[ey])); }).join(''), { stroke: 'context', width: c.t('spark-context'), mark: false });
    c.path(pts.map(function (p, i) { return (i ? 'L' : 'M') + K.round(p[0]) + ',' + K.round(p[1]); }).join(''), { stroke: 'subject', width: c.t('spark-line'), data: { series: o.key } }, [Math.min(pts[0][0], pts[pts.length - 1][0]), Math.min.apply(null, pts.map(function (p) { return p[1]; })), Math.abs(pts[pts.length - 1][0] - pts[0][0]), 1]);
    list.forEach(function (r) { c.datum(xs(K.time(r[ex])), ys(r[ey]), { data: { key: o.key + '|' + r[ex], field: ey, value: r[ey] } }); });
    var last = pts[pts.length - 1];
    c.circle(last[0], last[1], c.t('spark-end-radius'), { fill: 'subject', mark: false });
  }
  function totals_table(c, by, rows_def, cols, titles, y0) {
    var W = c.width, ey = c.field('y'), f = c.spec.formats || {}, vals = [];
    rows_def.forEach(function (p) { (by[String(p.value)] || []).forEach(function (r) { vals.push(r[ey]); }); });
    var dom = K.nice(Math.min(0, Math.min.apply(null, vals)), Math.max.apply(null, vals), 2);
    var nw = 0;
    rows_def.forEach(function (p) { nw = Math.max(nw, c.measure(p.label, 'tick', 600) + (p.indent || 0) * 14); });
    var cw = cols.map(function (k) { var w = c.measure(titles[k] || '', 'tick', 600); rows_def.forEach(function (p) { var l = by[String(p.value)] || []; if (l.length) w = Math.max(w, c.measure(K.fmt(l[l.length - 1][k], f[k] || 'number'), 'tick', 700)); }); return Math.ceil(w + 14); });
    var cwSum = cw.reduce(function (a, b) { return a + b; }, 0);
    var sx0 = c.phone ? 0 : Math.ceil(nw + 16), sw = Math.max(60, W - sx0 - cwSum - 10), rh = 44, y = y0;
    var colx = function (j) { return W - cw.slice(j + 1).reduce(function (a, b) { return a + b; }, 0); };
    cols.forEach(function (k, j) { if (titles[k]) c.text(colx(j), y + c.size('tick'), titles[k], { role: 'tick', weight: 600, anchor: 'end', fill: 'secondary' }); });
    y += c.size('tick') + 8;
    rows_def.forEach(function (p) {
      var list = by[String(p.value)] || [];
      if (!list.length) { c.warn('no rows for the totals row ' + p.value); return; }
      var ry = y + (c.phone ? c.size('tick') + 4 : 0), ind = (p.indent || 0) * 14;
      var lb = c.text(ind, c.phone ? y + c.size('tick') : ry + rh / 2 + 4, p.label, { role: 'tick', weight: 600 }), under = 0;
      if (ind) c.line(ind - 9, y + (c.phone ? 2 : 4), ind - 9, (c.phone ? y + c.size('tick') : ry + rh / 2), { stroke: 'gridline', width: c.t('line-hairline'), mark: false });
      var xs = K.scale.linear([K.time(list[0][c.field('x')]), K.time(list[list.length - 1][c.field('x')])], [sx0, sx0 + sw]);
      var ys = K.scale.linear([dom[0], dom[1]], [ry + rh - 4, ry + 4]);
      // each sparkline on its own baseline at its first value (KS2), with its peak marked where the spec names it
      var base = list[0][ey];
      c.line(sx0, ys(base), sx0 + sw, ys(base), { stroke: 'gridline', width: c.t('line-hairline'), mark: false });
      spark(c, list, null, xs, ys, { key: p.value, area: false });
      if (p.peak) {
        var pk = list.reduce(function (m, r) { return r[ey] > m[ey] ? r : m; }, list[0]), pkx = xs(K.time(pk[c.field('x')])), pky = ys(pk[ey]);
        c.circle(pkx, pky, c.t('spark-end-radius'), { fill: 'subject', mark: false });
        var pw0 = String(p.peak).replace('{value}', K.fmt(pk[p.peak_field || ey], (c.spec.formats || {})[p.peak_field || ey] || 'integer')).replace('{x}', K.fmt(pk[c.field('x')], 'month'));
        var pkw = c.measure(pw0, 'tick');
        if (!c.phone) c.text(Math.max(sx0, Math.min(pkx - pkw / 2, sx0 + sw - pkw)), ry - 2, pw0, { role: 'tick' });
        // on a phone the row's name shares the line above the sparkline: the peak's words go right of the name where they
        // fit, else under the sparkline (E32)
        else if (lb.x + lb.w + 12 + pkw <= W) c.text(W - pkw, y + c.size('tick'), pw0, { role: 'tick' });
        else { under = c.size('tick') + 8; c.text(Math.max(0, Math.min(pkx - pkw / 2, W - pkw)), ry + rh + c.size('tick') + 2, pw0, { role: 'tick' }); }
      }
      cols.forEach(function (k, j) { c.text(colx(j), ry + rh / 2 + 4, K.fmt(list[list.length - 1][k], f[k] || 'number'), { role: 'tick', weight: j ? 400 : 700, anchor: 'end', fill: j ? 'secondary' : 'label' }); });
      y = ry + rh + 4 + under;
    });
    return y;
  }
  K.register_chart({
    form: 'area-sparklines', name: 'Small Multiple Area Sparklines', family: 'change-over-time',
    encode: { x: 'month', y: 'number', series: 'category', columns: 'list?' },
    labels: ['panels', 'context', 'context_label', 'end', 'domain', 'totals', 'totals_title', 'panels_title', 'columns_titles', 'panel_height'],
    phone: 'same',
    draw: function (c) {
      var by = series(c), L = c.labels, W = c.width, ey = c.field('y'), f = c.spec.formats || {};
      var panels = L.panels || [];
      var vals = [];
      panels.forEach(function (p) { (by[String(p.value)] || []).forEach(function (r) { vals.push(r[ey]); }); });
      var dom = L.domain || K.nice(Math.min(0, Math.min.apply(null, vals)), Math.max.apply(null, vals), 4);
      var cols = c.phone ? 2 : 4, gx = c.t(c.phone ? 'spark-phone-gap-x' : 'spark-gap-x');
      var ticks = K.ticks(dom[0], dom[1], 0, dom.step || K.nice(dom[0], dom[1], 4).step);
      var gut = 0;
      ticks.forEach(function (t, i) { gut = Math.max(gut, c.measure(K.fmt(t, (i === ticks.length - 1 && f.y_tick_top) || f.tick || 'signed'), 'tick') + 10); });
      gut = Math.ceil(gut);
      var pw = Math.floor((W - gut - gx * (cols - 1) - c.t('spark-end-radius') - 1) / cols), ph = L.panel_height || 88, tl = 1, el = 1;
      var tlh = Math.round(c.size('tick') * 1.25);
      panels.forEach(function (p) {
        tl = Math.max(tl, K.wrap(p.label, c.size('tick'), pw, 600).length);
        var lst = by[String(p.value)] || [];
        if (L.end && lst.length) el = Math.max(el, K.wrap(K.parts.fill(c, L.end, lst[lst.length - 1]), c.size('tick'), pw, 700).length);
      });
      // an end label wider than its panel wraps inside it (D3-93)
      var head = tl * tlh + (L.end ? 16 + (el - 1) * tlh + 10 : 10);
      var y0 = 0, xs0 = null;
      if (L.totals && L.totals.length) {
        if (L.totals_title) { var tt = c.text(0, c.size('tick'), L.totals_title, { role: 'eyebrow', weight: 700, fill: 'secondary', max: W }); y0 = tt.bottom + 8; }
        y0 = totals_table(c, by, L.totals, c.field('columns', false) || [], L.columns_titles || {}, y0) + 22;
        if (L.panels_title) { var pt = c.text(0, y0 + c.size('tick'), L.panels_title, { role: 'eyebrow', weight: 700, fill: 'secondary', max: W }); y0 = pt.bottom + 10; }
      }
      if (L.context_label) { c.line(0, y0 + 8, 22, y0 + 8, { stroke: 'context', width: c.t('spark-context'), mark: false }); var cl = c.text(28, y0 + 13, L.context_label, { role: 'tick', max: W - 28 }); y0 = cl.y + cl.h + 14; }
      var ctx = L.context ? by[String(L.context)] : null;
      panels.forEach(function (p, i) {
        var list = by[String(p.value)] || [];
        if (!list.length) { c.warn('no rows for panel ' + p.value); return; }
        var col = i % cols, row = Math.floor(i / cols), px = gut + col * (pw + gx), py = y0 + row * (ph + head + 30);
        var xs = K.scale.linear([K.time(list[0][c.field('x')]), K.time(list[list.length - 1][c.field('x')])], [px, px + pw]);
        var ys = K.scale.linear(dom, [py + head + ph, py + head]);
        xs0 = xs;
        // a one-word name wider than its panel keeps inside the drawing (D3-904's width sweep, placement only)
        var plw = c.measure(p.label, 'tick', 600);
        c.text(plw > pw && p.label.indexOf(' ') < 0 ? Math.min(px, W - plw - 1) : px, py + c.size('tick'), p.label, { role: 'tick', weight: 600, max: pw });
        if (L.end) c.text(px + pw, py + head - 10 - (el - 1) * tlh, K.parts.fill(c, L.end, list[list.length - 1]), { role: 'tick', weight: 700, anchor: 'end', max: pw });
        ticks.forEach(function (t) {
          c.line(px, ys(t), px + pw, ys(t), { stroke: t === 0 ? 'baseline' : 'gridline', width: c.t(t === 0 ? 'line-baseline' : 'line-hairline'), mark: false });
          if (col === 0) c.text(gut - 6, ys(t) + 4, K.fmt(t, (t === ticks[ticks.length - 1] && f.y_tick_top) || f.tick || 'signed'), { role: 'tick', anchor: 'end' });
        });
        spark(c, list, ctx && p.value !== L.context ? ctx : null, xs, ys, { key: p.value, area: true });
        c.text(px, py + head + ph + 18, K.fmt(list[0][c.field('x')], 'year'), { role: 'tick' });
        c.text(px + pw, py + head + ph + 18, K.fmt(list[list.length - 1][c.field('x')], 'year'), { role: 'tick', anchor: 'end' });
      });
      void xs0;
      c.height(y0 + Math.ceil(panels.length / cols) * (ph + head + 30));
    }
  });
  K.register_chart({
    form: 'sparkline-table', name: 'Sparkline Table', family: 'tables-and-plain-words',
    encode: { x: 'month', y: 'number', series: 'category', columns: 'list' },
    labels: ['panels', 'domain', 'columns_titles'],
    phone: 'same',
    draw: function (c) {
      var by = series(c), L = c.labels, W = c.width, ey = c.field('y'), cols = c.field('columns'), f = c.spec.formats || {};
      var panels = L.panels || [], vals = [];
      panels.forEach(function (p) { (by[String(p.value)] || []).forEach(function (r) { vals.push(r[ey]); }); });
      var dom = L.domain || K.nice(Math.min(0, Math.min.apply(null, vals)), Math.max.apply(null, vals), 2);
      var nw = 0;
      panels.forEach(function (p) { nw = Math.max(nw, c.measure(p.label, 'label', 600) + (p.indent || 0)); });
      var cw = cols.map(function (k) { var w = c.measure((L.columns_titles || {})[k] || '', 'tick', 600); panels.forEach(function (p) { var l = by[String(p.value)] || []; if (l.length) w = Math.max(w, c.measure(K.fmt(l[l.length - 1][k], f[k] || 'number'), 'label', 700)); }); return Math.ceil(w + 14); });
      var cwSum = cw.reduce(function (a, b) { return a + b; }, 0);
      var sx0 = c.phone ? 0 : Math.ceil(nw + 16), sw = Math.max(60, W - sx0 - cwSum - 10), rh = 34, y = 18;
      if (c.phone) sw = Math.max(60, W - cwSum - 10);
      cols.forEach(function (k, i) { var x = W - cw.slice(i + 1).reduce(function (a, b) { return a + b; }, 0); c.text(x, 12, (L.columns_titles || {})[k] || '', { role: 'tick', weight: 600, anchor: 'end' }); });
      panels.forEach(function (p, i) {
        var list = by[String(p.value)] || [];
        if (!list.length) return;
        var ry = y + 14 + i * (rh + (c.phone ? 22 : 0));
        var ly = c.phone ? ry : ry + rh / 2 + 5;
        c.text((p.indent || 0), ly, p.label, { role: 'label', weight: 600 });
        var top = c.phone ? ry + 8 : ry + 4;
        var xs = K.scale.linear([K.time(list[0][c.field('x')]), K.time(list[list.length - 1][c.field('x')])], [sx0, sx0 + sw]);
        var ys = K.scale.linear(dom, [top + rh - 8, top]);
        spark(c, list, null, xs, ys, { key: p.value, area: false });
        cols.forEach(function (k, j) { var x = W - cw.slice(j + 1).reduce(function (a, b) { return a + b; }, 0); c.text(x, (c.phone ? top + rh / 2 : ly), K.fmt(list[list.length - 1][k], f[k] || 'number'), { role: 'label', weight: j ? 400 : 700, anchor: 'end', fill: j ? 'secondary' : 'label' }); });
      });
      c.height(y + 14 + panels.length * (rh + (c.phone ? 22 : 0)) + 6);
    }
  });
})(globalThis.OAChart);
