/* Ranked bar (coverage plan 3.1, core; S03). One bar per category from a zero line, in the order of the data or spec.sort,
 * the total printed at the end; a bar may split into parts that read in grayscale by fill, outline, hatch and dash.
 * encode: category (text), value (number, the total), parts (list of number columns, optional).
 * labels: parts ([{field, label, style}] where style is solid, open, gray, hatch or dashed), total_suffix ({category: words}),
 * value_unit (words after each total, optional), named (a category or list the title names: the rest take the light fill,
 * K.parts.named_fill). formats: value. A negative value draws left of the zero line; a long
 * category name wraps. */
(function (K) {
  'use strict';
  var STYLE = function (n) { return K.parts.style(n); };
  K.register_chart({
    form: 'ranked-bar',
    name: 'Ranked Bar',
    family: 'comparison',
    encode: { category: 'text', value: 'number', parts: 'list?' },
    labels: ['parts', 'total_suffix', 'value_unit', 'named'],
    phone: 'same',
    draw: function (c) {
      var P = K.parts, rows = c.rows, ek = c.field('category'), ev = c.field('value'), parts = c.field('parts', false) || [];
      var f = c.spec.formats || {}, W = c.width, y = 0, fill = P.named_fill(c, c.labels.named, ek);
      var defs = (c.labels.parts || []).filter(function (p) { return parts.indexOf(p.field) >= 0; });
      parts.forEach(function (p) { if (!defs.some(function (d) { return d.field === p; })) c.warn('labels.parts names no style for ' + p); });
      if (defs.length) {
        y += c.size('label') + 2;
        y += P.key(c, defs.map(function (d) {
          var s = STYLE(d.style);
          return { label: d.label, fill: s.fill === 'none' || s.fill === 'surface' ? null : s.fill, stroke: s.stroke, dash: s.dash, open: s.fill === 'surface', pattern: s.pattern, direct: d.style !== 'solid' && d.style !== 'gray' };
        }), 0, y, W) + 10;
      }
      // label column: on a phone the category sits above its bar; a long name wraps (production test S6)
      var size = c.size('label'), bh = c.t(c.phone ? 'bar-phone-height' : 'bar-height'), pitch = c.t(c.phone ? 'bar-phone-pitch' : 'bar-pitch');
      var lw = 0, lmax = c.phone ? W : Math.floor(W * 0.4);
      rows.forEach(function (r) { K.wrap(String(r[ek]), size, lmax, 600).forEach(function (l) { lw = Math.max(lw, c.measure(l, 'label', 600)); }); });
      var x0 = c.phone ? 0 : Math.ceil(lw + 24);
      // bars run from zero either way, so a negative value draws to the left of the zero line
      var max = Math.max(0, Math.max.apply(null, rows.map(function (r) { return r[ev]; })));
      var min = Math.min(0, Math.min.apply(null, rows.map(function (r) { return r[ev]; })));
      var suffix = c.labels.total_suffix || {};
      var lab = function (r) { return K.fmt(r[ev], f.value || 'integer') + (c.labels.value_unit ? ' ' + c.labels.value_unit : ''); };
      var tw = 0, twn = 0;
      rows.forEach(function (r) { var w = c.measure(lab(r) + (suffix[r[ek]] || ''), 'label', 700); if (r[ev] < 0) twn = Math.max(twn, w); else tw = Math.max(tw, w); });
      var left = x0 + (min < 0 ? twn + 10 : 0);
      var xs = K.scale.linear([min, max], [left, Math.max(left + 60, W - tw - 10)]), zx = xs(0);
      var top = y + (c.phone ? size + 6 : 0), by = top;
      var bottom = top;
      rows.forEach(function (r, i) {
        var lines = K.wrap(String(r[ek]), size, lmax, 600).length, lh = Math.round(size * 1.25);
        if (c.phone) { if (i) by += Math.max(pitch, bh + 14 + lines * lh); }
        else if (i) by += Math.max(pitch, lines * lh + 8);
        var cy = by + bh / 2;
        if (c.phone) c.text(0, by - 8 - (lines - 1) * lh, r[ek], { role: 'label', weight: 600, max: lmax });
        else c.text(0, cy + size * 0.35 - (lines - 1) * lh / 2, r[ek], { role: 'label', weight: 600, max: lmax });
        var x = zx;
        if (defs.length) {
          defs.forEach(function (d) {
            var v = r[d.field] || 0;
            if (!v) return;
            var w = xs(v) - zx, s = STYLE(d.style);
            K.parts.styled(c, x, by, w, bh, s, { kind: x === zx ? 'bar' : 'segment', axis: 'x', zero: zx, data: { key: r[ek], field: d.field, value: v } });
            var t = K.fmt(v, f.value || 'integer');
            if (s.text && c.measure(t, 'label', 700) + 8 < w) c.text(x + w / 2, cy + size * 0.35, t, { role: 'label', weight: 700, anchor: 'middle', fill: s.text });
            x += w;
          });
        } else {
          var xe = xs(r[ev]);
          c.rect(Math.min(zx, xe), by, Math.abs(xe - zx), bh, { fill: fill(r), kind: 'bar', axis: 'x', zero: zx, data: { key: r[ek], field: ev, value: r[ev] } });
          x = xe;
        }
        var neg = r[ev] < 0;
        var tb = c.text(neg ? x - 8 : x + 8, cy + size * 0.35, lab(r), { role: 'label', weight: 700, anchor: neg ? 'end' : 'start' });
        if (suffix[r[ek]]) c.text(neg ? tb.x - c.measure(suffix[r[ek]], 'label') : tb.x + tb.w, cy + size * 0.35, suffix[r[ek]], { role: 'label', weight: 400 });
        // on a phone the zero line runs beside each bar only, never through the names above them (editor's request)
        if (c.phone) c.line(zx, by - 3, zx, by + bh + 3, { stroke: 'baseline', width: c.t('line-baseline'), mark: false });
        bottom = by + bh;
      });
      if (!c.phone) c.line(zx, top - 6, zx, bottom + 6, { stroke: 'baseline', width: c.t('line-baseline'), mark: false });
      c.height(bottom + 8);
    }
  });
})(globalThis.OAChart);
