/* Unit chart (coverage plan 3.4, core; S08). One square per row, keyed by its ID, so every mark traces to one record; squares
 * stack in columns by group (such as year) and in bands by category, read by fill, outline, hatch and dash.
 * encode: key (id), category (category), group (year or category, optional).
 * labels: categories ([{value, label, style}] style solid, open, gray, hatch or dashed, in band order), bins ([{label, max}],
 * optional: groups up to max print as one column), count_label (words before the counts row, optional). */
(function (K) {
  'use strict';
  var STY = { solid: { fill: 'subject' }, open: { fill: 'surface', stroke: 'subject' }, gray: { fill: 'light-fill' }, hatch: { pattern: 'u-hatch', stroke: 'subject' }, dashed: { fill: 'none', stroke: 'subject', dash: '2 2' } };
  K.register_chart({
    form: 'unit-chart', name: 'Unit Chart', family: 'composition',
    encode: { key: 'id', category: 'category', group: 'any?' },
    labels: ['categories', 'bins', 'count_label'],
    phone: 'same',
    draw: function (c) {
      var rows = c.rows, ek = c.field('key'), ec = c.field('category'), eg = c.field('group', false), L = c.labels, W = c.width;
      var cats = L.categories || [], bins = L.bins || [];
      var gkey = function (r) {
        if (!eg) return '';
        var v = r[eg];
        for (var i = 0; i < bins.length; i++) if (bins[i].max !== undefined && +v <= +bins[i].max) return bins[i].label;
        return String(v);
      };
      var groups = [];
      rows.forEach(function (r) { var g = gkey(r); if (groups.indexOf(g) < 0) groups.push(g); });
      if (eg) groups.sort(function (a, b) { var ia = bins.findIndex(function (x) { return x.label === a; }), ib = bins.findIndex(function (x) { return x.label === b; }); if (ia >= 0 || ib >= 0) return (ia < 0 ? 99 : ia) - (ib < 0 ? 99 : ib); return a < b ? -1 : 1; });
      var u = c.t('unit-size'), ug = c.t('unit-gap');
      var lw = 0;
      cats.forEach(function (x) { lw = Math.max(lw, c.measure(x.label, 'label', 600) + 22); });
      var x0 = c.phone ? 0 : Math.ceil(lw + 16), cw = (W - x0) / Math.max(1, groups.length);
      var per = Math.max(1, Math.floor((cw - 4 + ug) / (u + ug)));
      var cell = {};
      rows.forEach(function (r) { var k = gkey(r) + '\u0000' + r[ec]; (cell[k] = cell[k] || []).push(r); });
      var y = c.phone ? 6 : 0;
      if (L.count_label) {
        c.text(c.phone ? 0 : 0, y + c.size('tick'), L.count_label, { role: 'tick' });
        y += c.phone ? c.size('tick') + 8 : 0;
      }
      groups.forEach(function (g, gi) {
        var n = rows.filter(function (r) { return gkey(r) === g; }).length;
        c.text(x0 + gi * cw + cw / 2, y + c.size('tick'), K.fmt(n, 'integer'), { role: 'tick', anchor: 'middle', tnum: true });
      });
      y += c.size('tick') + 14;
      cats.forEach(function (cat) {
        var st = STY[cat.style] || STY.solid, maxrows = 1;
        groups.forEach(function (g) { var m = (cell[g + '\u0000' + cat.value] || []).length; maxrows = Math.max(maxrows, Math.ceil(m / per)); });
        var bandH = maxrows * (u + ug) + 10;
        if (c.phone) { c.text(0, y + c.size('label'), cat.label, { role: 'label', weight: 600 }); y += c.size('label') + 8; }
        else c.text(0, y + c.size('label') * 0.9, cat.label, { role: 'label', weight: 600, max: lw });
        groups.forEach(function (g, gi) {
          (cell[g + '\u0000' + cat.value] || []).forEach(function (r, j) {
            var col = j % per, rw = Math.floor(j / per);
            var x = x0 + gi * cw + (cw - Math.min(per, (cell[g + '\u0000' + cat.value] || []).length) * (u + ug) + ug) / 2 + col * (u + ug), yy = y + rw * (u + ug);
            if (st.pattern) c.pattern(st.pattern, st.stroke);
            c.rect(x, yy, u, u, { fill: st.fill === 'none' ? 'none' : st.fill, pattern: st.pattern, kind: 'unit', data: { key: r[ek], field: ec, value: r[ec] } });
            if (st.stroke) c.rect(x + 0.5, yy + 0.5, u - 1, u - 1, { stroke: st.stroke, dash: st.dash, mark: false });
          });
        });
        y += bandH + 8;
        c.line(x0, y - 9, W, y - 9, { stroke: 'gridline', width: c.t('line-hairline'), mark: false });
      });
      var right = -1e9;
      groups.forEach(function (g, gi) {
        var tw = c.measure(g, 'tick'), cx = Math.min(Math.max(x0 + gi * cw + cw / 2, tw / 2), W - tw / 2);
        if (cx - tw / 2 < right + 6 && gi !== groups.length - 1) return;
        if (cx - tw / 2 < right + 6) return;
        c.text(cx, y + c.size('tick'), g, { role: 'tick', anchor: 'middle' });
        right = cx + tw / 2;
      });
      c.key(cats.map(function (x) { var s = STY[x.style] || STY.solid; return { fill: s.fill && s.fill !== 'none' && s.fill !== 'surface' ? s.fill : 'subject', pattern: !!s.pattern, direct: true }; }));
      c.height(y + c.size('tick') + 6);
    }
  });
})(globalThis.OAChart);
