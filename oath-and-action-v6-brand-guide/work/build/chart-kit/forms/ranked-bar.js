/* Ranked bar (coverage plan 3.1, core; S03). One bar per category from a zero line, in the order of the data or spec.sort,
 * the total printed at the end; a bar may split into parts that read in grayscale by fill, outline, hatch and dash.
 * encode: category (text), value (number, the total), parts (list of number columns, optional).
 * labels: parts ([{field, label, style}] where style is solid, open, gray, hatch or dashed), total_suffix ({category: words}),
 * value_unit (words after each total, optional). formats: value. */
(function (K) {
  'use strict';
  var STYLE = function (n) { return K.parts.style(n); };
  K.register_chart({
    form: 'ranked-bar',
    name: 'Ranked Bar',
    family: 'comparison',
    encode: { category: 'text', value: 'number', parts: 'list?' },
    labels: ['parts', 'total_suffix', 'value_unit'],
    phone: 'same',
    draw: function (c) {
      var P = K.parts, rows = c.rows, ek = c.field('category'), ev = c.field('value'), parts = c.field('parts', false) || [];
      var f = c.spec.formats || {}, W = c.width, y = 0;
      var defs = (c.labels.parts || []).filter(function (p) { return parts.indexOf(p.field) >= 0; });
      parts.forEach(function (p) { if (!defs.some(function (d) { return d.field === p; })) c.warn('labels.parts names no style for ' + p); });
      if (defs.length) {
        y += c.size('label') + 2;
        y += P.key(c, defs.map(function (d) {
          var s = STYLE(d.style);
          return { label: d.label, fill: s.fill === 'none' || s.fill === 'surface' ? null : s.fill, stroke: s.stroke, dash: s.dash, open: s.fill === 'surface', pattern: s.pattern, direct: d.style !== 'solid' && d.style !== 'gray' };
        }), 0, y, W) + 10;
      }
      // label column: on a phone the category sits above its bar
      var size = c.size('label'), bh = c.t(c.phone ? 'bar-phone-height' : 'bar-height'), pitch = c.t(c.phone ? 'bar-phone-pitch' : 'bar-pitch');
      var lw = 0;
      rows.forEach(function (r) { lw = Math.max(lw, c.measure(r[ek], 'label', 600)); });
      var x0 = c.phone ? 0 : Math.ceil(lw + 24);
      var max = Math.max.apply(null, rows.map(function (r) { return r[ev]; }));
      var suffix = c.labels.total_suffix || {};
      var tw = 0;
      rows.forEach(function (r) { tw = Math.max(tw, c.measure(K.fmt(r[ev], f.value || 'integer') + (suffix[r[ek]] || '') + (c.labels.value_unit ? ' ' + c.labels.value_unit : ''), 'label', 700)); });
      var xs = K.scale.linear([0, max], [x0, Math.max(x0 + 60, W - tw - 10)]);
      var top = y + (c.phone ? size + 6 : 0);
      rows.forEach(function (r, i) {
        var by = top + i * pitch, cy = by + bh / 2;
        if (c.phone) c.text(0, by - 8, r[ek], { role: 'label', weight: 600 });
        else c.text(0, cy + size * 0.35, r[ek], { role: 'label', weight: 600 });
        var x = x0;
        if (defs.length) {
          defs.forEach(function (d) {
            var v = r[d.field] || 0;
            if (!v) return;
            var w = xs(v) - x0, s = STYLE(d.style);
            K.parts.styled(c, x, by, w, bh, s, { kind: x === x0 ? 'bar' : 'segment', axis: 'x', zero: x0, data: { key: r[ek], field: d.field, value: v } });
            var t = K.fmt(v, f.value || 'integer');
            if (s.text && c.measure(t, 'label', 700) + 8 < w) c.text(x + w / 2, cy + size * 0.35, t, { role: 'label', weight: 700, anchor: 'middle', fill: s.text });
            x += w;
          });
        } else {
          c.rect(x0, by, xs(r[ev]) - x0, bh, { fill: 'subject', kind: 'bar', axis: 'x', zero: x0, data: { key: r[ek], field: ev, value: r[ev] } });
          x = xs(r[ev]);
        }
        var total = K.fmt(r[ev], f.value || 'integer') + (c.labels.value_unit ? ' ' + c.labels.value_unit : '');
        var tb = c.text(x + 8, cy + size * 0.35, total, { role: 'label', weight: 700 });
        if (suffix[r[ek]]) c.text(tb.x + tb.w, cy + size * 0.35, suffix[r[ek]], { role: 'label', weight: 400 });
      });
      var bottom = top + (rows.length - 1) * pitch + bh;
      c.line(x0, top - 6, x0, bottom + 6, { stroke: 'baseline', width: c.t('line-baseline'), mark: false });
      c.height(bottom + 8);
    }
  });
})(globalThis.OAChart);
