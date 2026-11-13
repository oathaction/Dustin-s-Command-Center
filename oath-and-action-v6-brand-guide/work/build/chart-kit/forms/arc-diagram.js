/* Arc diagram (coverage plan 3.12, extended; S75). Items on one line in a stated order, each pair the data links joined
 * by an arc whose width is the pair's measure in one linear unit (K.parts.link's arc), with a key of widths; an arc
 * narrower than a pixel draws at 1 px, and the key says so. Arcs draw widest first, so narrow ones sit on top. The line
 * runs across under the arcs at a desk and down the left on a phone (under labels.down_below px, default 560), its
 * items named by number. The pair the title names (labels.named) takes the subject ink and a key line of its own; every
 * other arc takes the context ink (the data lead's round 3 ruling (b)).
 * encode: from (text), to (text), value (number).
 * labels: order ([item], the line's order), unit (px of width per unit of the measure), key_steps ([measures]),
 * key_words ([words for each step]), key_title, key_hairline (words under the key), named ([from, to]), named_words (the
 * named pair's key words, with {from}, {to} and {v}), split (true: an item's name breaks at its first space onto two lines
 * under the line, "H.R." over "950"), down_below (px).
 * formats: value. Maker B, round 3. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'arc-diagram', name: 'Arc Diagram', family: 'relationships',
    encode: { from: 'text', to: 'text', value: 'number' },
    labels: ['order', 'unit', 'key_steps', 'key_words', 'key_title', 'key_hairline', 'named', 'named_words', 'split', 'down_below'],
    phone: 'differs',
    draw: function (c) {
      var P = K.parts, L = c.labels, f = c.spec.formats || {}, W = c.width, down = W < (L.down_below || 560);
      var ef = c.field('from'), et = c.field('to'), ev = c.field('value');
      var order = (L.order || []).map(String), unit = +L.unit || 1, tk = c.size('tick'), lb = c.size('label');
      var named = (L.named || []).map(String), isn = function (r) { return named.length === 2 && named.indexOf(String(r[ef])) >= 0 && named.indexOf(String(r[et])) >= 0; };
      c.rows.forEach(function (r) { [r[ef], r[et]].forEach(function (k) { if (order.indexOf(String(k)) < 0) c.warn('arc-diagram: ' + k + ' is not in labels.order'); }); });
      var y = 0;
      // the key: widths, the hairline's words, then the named pair as a line of its own
      if (L.key_steps) {
        y += P.width_key(c, 0, y, unit, L.key_steps, { words: L.key_words, len: 32, title: L.key_title, max: W });
        if (L.key_hairline) y = c.text(0, y + tk * 0.9, L.key_hairline, { role: 'tick', max: W }).bottom + 6;
      }
      var nr = c.rows.filter(isn)[0];
      if (nr) {
        var nw = Math.max(1, nr[ev] * unit), ky = y + Math.max(nw, tk) / 2 + 4;
        c.line(0, ky, 32, ky, { stroke: 'subject', width: nw, mark: false });
        c.key([{ fill: 'subject', pattern: true }]);
        y = c.text(40, ky + tk * 0.35, String(L.named_words || '{from} and {to}: {v}').split('{from}').join(nr[ef]).split('{to}').join(nr[et]).split('{v}').join(K.fmt(nr[ev], f.value || 'integer')), { role: 'tick', weight: 700, max: W - 40, fill: 'label' }).bottom;
      }
      y += 16;
      var n = order.length, pos = {}, box = function (k) { var p = pos[k]; return { x: p[0], y: p[1], w: 0, h: 0 }; };
      var lw = 0;
      order.forEach(function (k) { lw = Math.max(lw, c.measure(k, 'tick', 600)); });
      var rows = c.rows.slice().sort(function (a, b) { return b[ev] - a[ev]; }), bottom;
      if (!down) {
        // across: the widest arc, a half circle over the whole line, sets the line's height
        var m = Math.ceil(lw / 2) + 2, step = (W - 2 * m) / Math.max(1, n - 1), base = y + (n - 1) * step / 2 + 8;
        order.forEach(function (k, i) { pos[k] = [m + i * step, base]; });
        rows.forEach(function (r) { P.link(c, box(r[ef]), box(r[et]), { shape: 'arc', side: 'above', stroke: isn(r) ? 'subject' : 'context', width: Math.max(1, r[ev] * unit), data: { key: r[ef] + ' and ' + r[et], from: r[ef], to: r[et], value: r[ev] } }); });
        c.line(m, base, W - m, base, { stroke: 'baseline', width: c.t('line-baseline'), mark: false });
        bottom = base;
        order.forEach(function (k) {
          var p = pos[k], parts = L.split ? [k.slice(0, k.indexOf(' ')), k.slice(k.indexOf(' ') + 1)] : [k];
          c.circle(p[0], p[1], 3.5, { fill: 'subject', mark: false });
          parts.forEach(function (w, j) { bottom = c.text(p[0], base + 10 + tk * 0.9 + j * Math.round(tk * 1.2), w, { role: 'tick', weight: 600, anchor: 'middle', fill: 'label' }).bottom; });
        });
      } else {
        // down: names at the left, the line beside them, arcs bowing to the right
        var lx = Math.ceil(lw) + 12, pitch = 30, room = W - lx - 4, span = (n - 1) * pitch;
        var sag = Math.min(0.5, room / Math.max(1, span));
        order.forEach(function (k, i) { pos[k] = [lx, y + 6 + i * pitch]; });
        rows.forEach(function (r) { P.link(c, box(r[ef]), box(r[et]), { shape: 'arc', side: 'above', sag: sag, stroke: isn(r) ? 'subject' : 'context', width: Math.max(1, r[ev] * unit), data: { key: r[ef] + ' and ' + r[et], from: r[ef], to: r[et], value: r[ev] } }); });
        c.line(lx, y + 6, lx, y + 6 + span, { stroke: 'baseline', width: c.t('line-baseline'), mark: false });
        order.forEach(function (k) { var p = pos[k]; c.circle(p[0], p[1], 3.5, { fill: 'subject', mark: false }); c.text(lx - 10, p[1] + tk * 0.35, k, { role: 'tick', weight: 600, anchor: 'end', fill: 'label' }); });
        bottom = y + 6 + span + tk;
        c.arrange('phone');
      }
      void lb;
      c.height(bottom + 2);
    }
  });
})(globalThis.OAChart);
