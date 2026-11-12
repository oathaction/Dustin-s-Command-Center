/* Dot plot (coverage plan 3.1, core; S19). Many items on one scale, one row each: the name at the left, a dot at the
 * value, every value printed in a column at the right edge. One row may be drawn as a reference line across the plot in
 * place of a dot (labels.reference names its key), labeled once above the rows. Rows whose status equals labels.open take an
 * open dot, explained by a key above the rows. Ticks and light gridlines run along the bottom.
 * encode: key (code), label (text), value (number), status (category, optional).
 * labels: reference (the key drawn as a line), reference_label (words over the line, with {value}), open (the status value
 * drawn as an open dot), key_open (the key's words for an open dot), named (keys whose names print bold), names ({key: printed name}).
 * formats: value, tick. scale: x ([lo, hi]). On a phone the same arrangement draws at a narrower plot. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'dot-plot',
    name: 'Dot Plot',
    family: 'comparison',
    encode: { key: 'code', label: 'text', value: 'number', status: 'category?' },
    labels: ['reference', 'reference_label', 'open', 'key_open', 'named', 'names'],
    phone: 'same',
    draw: function (c) {
      var P = K.parts, ek = c.field('key'), el = c.field('label'), ev = c.field('value'), es = c.field('status', false);
      var f = c.spec.formats || {}, W = c.width, L = c.labels, names = L.names || {};
      var ref = L.reference === undefined ? null : String(L.reference);
      var named = [].concat(L.named || []).map(String);
      var rows = c.rows.filter(function (r) { return String(r[ek]) !== ref; });
      var refrow = ref === null ? null : c.rows.filter(function (r) { return String(r[ek]) === ref; })[0];
      if (ref !== null && !refrow) c.warn('labels.reference names no row: ' + ref);
      var is_open = function (r) { return es && L.open !== undefined && String(r[es]) === String(L.open); };
      var name = function (r) { return names[String(r[ek])] !== undefined ? names[String(r[ek])] : String(r[el]); };
      var val = function (r) { return K.fmt(r[ev], f.value || 'integer'); };
      var size = c.size('label'), tick = c.size('tick'), pitch = Math.round(size * 1.5), y = 0;
      // the key, when any row takes an open dot: the open dot and its words (a filled dot needs none)
      if (rows.some(is_open) && L.key_open) {
        var kr = c.t('dot-open-radius');
        y += size + 2;
        c.circle(kr + 1, y - size * 0.35, kr, { fill: 'surface', mark: false });
        c.circle(kr + 1, y - size * 0.35, kr, { stroke: 'subject', width: c.t('line-context'), mark: false });
        var kb = c.text(2 * kr + 10, y, L.key_open, { role: 'label', max: W - 2 * kr - 10 });
        y = kb.bottom - size * 0.241 + 14;
        c.key([{ fill: 'subject', direct: true }, { fill: 'surface', pattern: true }]);   // the open dot reads by its outline
      }
      // the name column and the value column
      var lw = 0, vw = 0;
      rows.forEach(function (r) { lw = Math.max(lw, c.measure(name(r), 'label', named.indexOf(String(r[ek])) >= 0 ? 700 : 400)); vw = Math.max(vw, c.measure(val(r), 'label', 600, true)); });
      var x0 = Math.ceil(lw + (c.phone ? 12 : 20)), x1 = W - Math.ceil(vw + (c.phone ? 12 : 20));
      var vals = c.rows.map(function (r) { return r[ev]; });
      var sx = (c.spec.scale || {}).x, dom = sx || K.nice(Math.min(0, Math.min.apply(null, vals)), Math.max.apply(null, vals), c.phone ? 3 : 6);
      var xs = K.scale.linear([dom[0], dom[1]], [x0 + 8, x1 - 8]);
      // the reference line's words above the rows, kept inside the plot
      if (refrow && L.reference_label) {
        var words = P.fill(c, L.reference_label, refrow), ww = c.measure(words, 'tick', 600);
        y += tick;
        c.text(Math.min(Math.max(xs(refrow[ev]), x0 + ww / 2), W - ww / 2), y, words, { role: 'tick', weight: 600, anchor: 'middle', fill: 'label' });
        y += 10;
      }
      var top = y, r_dot = c.t('dot-open-radius');
      var bottom = top + rows.length * pitch;
      // gridlines at the ticks, then the reference line, then the rows over them
      var ticks = K.ticks(dom[0], dom[1], c.phone ? 3 : 6);
      ticks.forEach(function (t) { c.line(xs(t), top, xs(t), bottom, { stroke: 'gridline', width: c.t('line-hairline'), mark: false }); });
      if (refrow) c.line(xs(refrow[ev]), top - 4, xs(refrow[ev]), bottom, { stroke: 'label', width: c.t('line-baseline'), dash: '4 3', data: { key: refrow[ek], field: ev, value: refrow[ev] } });
      rows.forEach(function (r, i) {
        var cy = top + i * pitch + pitch / 2, ty = cy + size * 0.35, b = named.indexOf(String(r[ek])) >= 0;
        c.text(0, ty, name(r), { role: 'label', weight: b ? 700 : 400 });
        var x = xs(r[ev]);
        if (is_open(r)) {
          c.circle(x, cy, r_dot, { fill: 'surface', data: { key: r[ek], field: ev, value: r[ev] } });
          c.circle(x, cy, r_dot, { stroke: 'subject', width: c.t('line-context'), mark: false });
        } else c.circle(x, cy, r_dot, { fill: 'subject', data: { key: r[ek], field: ev, value: r[ev] } });
        c.text(W, ty, val(r), { role: 'label', weight: b ? 700 : 600, anchor: 'end', tnum: true });
      });
      // the scale along the bottom
      var ay = bottom + tick + 8;
      ticks.forEach(function (t, i) {
        c.line(xs(t), bottom, xs(t), bottom + 4, { stroke: 'baseline', width: c.t('line-hairline'), mark: false });
        c.text(xs(t), ay, K.fmt(t, i === ticks.length - 1 && f.tick_last ? f.tick_last : (f.tick || 'integer')), { role: 'tick', anchor: 'middle' });
      });
      c.height(ay + 4);
    }
  });
})(globalThis.OAChart);
