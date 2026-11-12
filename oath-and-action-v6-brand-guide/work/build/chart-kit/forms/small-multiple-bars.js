/* Small-multiple bars (coverage plan 3.1, extended; S23). The same bar comparison repeated in one panel per group, on one
 * shared scale, so a reader compares the groups panel to panel. Each panel has its title, then one bar per category from a
 * zero line with the category's name at the left and the value at the bar's end. Panels sit in a grid, as many across as
 * fit at the panel's least width, one across on a phone. Categories the title names are set in ink, the rest in the light
 * fill on Newsprint and the context ink on Charcoal (palette rule R3). A bar the title names by panel and category
 * (labels.point) takes the working red with its keyline on Newsprint (Rule 14.6), and every other bar the light fill.
 * encode: panel (category), category (category), value (number).
 * labels: panel_title (words with {column} placeholders, filled from the panel's first row), categories ({category:
 * printed name}), named (a category or list set in ink; with none, every bar is in ink), point ({panel, category}: the
 * one bar in red). formats: value.
 * scale: x ([lo, hi], shared by every panel). */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'small-multiple-bars',
    name: 'Small Multiple Bars',
    family: 'comparison',
    encode: { panel: 'category', category: 'category', value: 'number' },
    labels: ['panel_title', 'categories', 'named', 'point'],
    phone: 'same',
    draw: function (c) {
      var P = K.parts, rows = c.rows, ep = c.field('panel'), ek = c.field('category'), ev = c.field('value');
      var f = c.spec.formats || {}, W = c.width, L = c.labels, names = L.categories || {};
      // palette rule R3 (DR-236) and the red point by panel and category, through the kit's shared part
      var pt = L.point && typeof L.point === 'object' ? L.point : null;
      var fill = K.parts.named_fill(c, pt ? [] : L.named, ek, null, pt ? pt.category : null);
      var is_pt = function (r) { return !!pt && String(r[ep]) === String(pt.panel) && fill.is_point(r); };
      var ink = function (r) { return is_pt(r) || fill.is_named(r); };
      var paint = function (r) { return is_pt(r) ? Object.assign({ fill: 'point' }, fill.keyline(r)) : { fill: pt ? fill.is_named(r) ? 'subject' : (c.ground === 'charcoal' ? 'context' : 'light-fill') : fill(r) }; };
      var name = function (k) { return names[k] !== undefined ? names[k] : k; };
      var val = function (r) { return K.fmt(r[ev], f.value || 'number:1'); };
      var panels = [], by = {};
      rows.forEach(function (r) { var p = String(r[ep]); if (!by[p]) { by[p] = []; panels.push(p); } by[p].push(r); });
      var size = c.size('label'), lh = Math.round(size * 1.25), gapx = 32, gapy = 28;
      var minw = 300, cols = c.phone ? 1 : Math.max(1, Math.min(panels.length, Math.floor((W + gapx) / (minw + gapx))));
      var pw = (W - gapx * (cols - 1)) / cols;
      // one label column and one scale for every panel
      var lw = 0, vw = 0;
      rows.forEach(function (r) { lw = Math.max(lw, c.measure(name(String(r[ek])), 'label', ink(r) ? 700 : 400)); vw = Math.max(vw, c.measure(val(r), 'label', ink(r) ? 700 : 600, true)); });
      var vals = rows.map(function (r) { return r[ev]; });
      var dom = (c.spec.scale || {}).x || [0, Math.max.apply(null, vals)];
      var bh = c.t('bar-dense-height'), pitch = Math.max(bh + 10, lh + 6);
      var y = 0, rowtop = 0, rowh = 0;
      panels.forEach(function (p, i) {
        var col = i % cols;
        if (col === 0) { rowtop = y + (i ? gapy : 0); rowh = 0; }
        var px = col * (pw + gapx), pr = by[p];
        var tw = L.panel_title ? P.fill(c, L.panel_title, pr[0]) : p;
        var tb = c.text(px, rowtop + size, tw, { role: 'label', weight: 700, max: pw });
        var top = tb.bottom + 10;
        var x0 = px + Math.ceil(lw + 14), x1 = px + pw - vw - 10;
        var xs = K.scale.linear(dom, [x0, Math.max(x0 + 40, x1)]), zx = xs(0);
        pr.forEach(function (r, j) {
          var yy = top + j * pitch, cy = yy + bh / 2, on = ink(r), xe = xs(r[ev]);
          c.text(px, cy + size * 0.35, name(String(r[ek])), { role: 'label', weight: on ? 700 : 400 });
          c.rect(zx, yy, xe - zx, bh, Object.assign({ kind: 'bar', axis: 'x', zero: zx, data: { key: p + '|' + r[ek], field: ev, value: r[ev] } }, paint(r)));
          c.text(xe + 6, cy + size * 0.35, val(r), { role: 'label', weight: on ? 700 : 600, tnum: true });
        });
        var bottom = top + (pr.length - 1) * pitch + bh;
        c.line(zx, top - 4, zx, bottom + 4, { stroke: 'baseline', width: c.t('line-baseline'), mark: false });
        rowh = Math.max(rowh, bottom - rowtop);
        if (col === cols - 1 || i === panels.length - 1) y = rowtop + rowh;
      });
      c.height(y + 6);
    }
  });
})(globalThis.OAChart);
