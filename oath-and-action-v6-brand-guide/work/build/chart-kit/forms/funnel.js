/* Funnel (coverage plan 3.10, extended; S65). Stages of one process drawn from one base, each nested inside the one
 * before: one bar a stage from a shared left edge, so lengths compare exactly, and beside each bar the people the stage
 * lost, drawn as a segment from the bar's end to the stage before's end and named under it. A row that is neither a stage
 * nor a loss (a breakdown of the last stage) prints in the table only. Each stage's name prints over its bar with its
 * count and its share of the base; the drawing is the same on a phone.
 * encode: category (text, the table's words), value (number), key (code), role (category: labels.stage marks a stage,
 * any other value a loss or a part set apart).
 * labels: stage (the role value of a stage; default "stage"), losses ({stage key: key of the row it lost before it}),
 * names ({key: printed name}), short ({key: name printed under 400 px}), value ('{v}' and '{p}' words beside a stage's
 * name; default '{v}, {p}'), loss ('{name}' and '{v}' words under a loss; default '{name}: {v}'), named (keys the title
 * names: the subject ink, words in bold), fills ({key: color role}, for any other bar or loss), set_apart (keys of losses
 * drawn as an outline with a dashed edge: a part held aside, not lost).
 * formats: value, share. Maker B, round 3. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'funnel', name: 'Funnel', family: 'behavior',
    encode: { category: 'text', value: 'number', key: 'code', role: 'category' },
    labels: ['stage', 'losses', 'names', 'short', 'value', 'loss', 'named', 'fills', 'set_apart'],
    phone: 'same',
    draw: function (c) {
      var P = K.parts, L = c.labels, f = c.spec.formats || {}, W = c.width, ph = W < 400;
      var ec = c.field('category'), ev = c.field('value'), ek = c.field('key'), er = c.field('role');
      var sv = String(L.stage || 'stage'), names = L.names || {}, short = L.short || {}, fills = L.fills || {};
      var named = [].concat(L.named || []).map(String), apart = [].concat(L.set_apart || []).map(String);
      var byk = {};
      c.rows.forEach(function (r) { byk[String(r[ek])] = r; });
      var stages = c.rows.filter(function (r) { return String(r[er]) === sv; });
      if (!stages.length) { c.warn('funnel: no row has role "' + sv + '"'); return; }
      var base = stages[0][ev], lb = c.size('label'), tk = c.size('tick');
      var nm = function (r) { var k = String(r[ek]); return ph && short[k] !== undefined ? short[k] : names[k] !== undefined ? names[k] : r[ec]; };
      var v = function (x) { return K.fmt(x, f.value || 'integer'); };
      var p = function (x) { return K.fmt(100 * x / base, f.share || 'percent:1'); };
      var x0 = 0, x1 = W - 1, sx = function (x) { return x0 + (x1 - x0) * x / base; };
      var bh = c.t(ph ? 'bar-phone-height' : 'bar-height'), y = 0, prev = null;
      stages.forEach(function (r, i) {
        var k = String(r[ek]), isn = named.indexOf(k) >= 0, wt = isn ? 700 : 400;
        // the stage's name, and its count with its share of the base flush right where both fit on one line
        var vw = String(L.value || '{v}, {p}').split('{v}').join(v(r[ev])).split('{p}').join(p(r[ev]));
        if (i === 0) vw = v(r[ev]);
        var vwid = c.measure(vw, 'label', wt, true), nwid = c.measure(nm(r), 'label', wt);
        var nb = c.text(0, y + lb * 0.95, nm(r), { role: 'label', weight: wt, max: W });
        if (nwid + vwid + 16 <= W) c.text(W, y + lb * 0.95, vw, { role: 'label', weight: wt, anchor: 'end', tnum: true });
        else nb = c.text(0, nb.bottom + lb * 0.95, vw, { role: 'label', weight: wt, tnum: true, max: W });
        var by = Math.ceil(nb.bottom) + 6, w = sx(r[ev]) - x0;
        var fill = fills[k] || (isn ? 'subject' : 'context');
        c.rect(x0, by, w, bh, { fill: fill, kind: 'bar', axis: 'x', zero: x0, data: { key: k, field: ev, value: r[ev] } });
        var bottom = by + bh;
        // the loss between the stage before and this one, from this bar's end to the stage before's end
        var lk = (L.losses || {})[k];
        if (prev && lk !== undefined) {
          var lr = byk[String(lk)];
          if (!lr) c.warn('funnel: labels.losses names no row: ' + lk);
          else {
            if (Math.abs(prev[ev] - r[ev] - lr[ev]) > 0.5) c.warn('funnel: ' + lk + ' is not the gap between ' + prev[ek] + ' and ' + k);
            var lx = sx(r[ev]), lw = sx(prev[ev]) - lx, ln = named.indexOf(String(lk)) >= 0, la = apart.indexOf(String(lk)) >= 0;
            var lf = fills[String(lk)] || (ln ? 'subject' : 'track');
            c.rect(lx, by, lw, bh, { fill: la ? 'none' : lf, kind: 'segment', data: { key: String(lk), field: ev, value: lr[ev] } });
            if (!ln || la) c.rect(lx + 0.5, by + 0.5, lw - 1, bh - 1, { stroke: 'context', width: 1, dash: la ? '3 2' : undefined, mark: false });
            var words = String(L.loss || '{name}: {v}').split('{name}').join(nm(lr)).split('{v}').join(v(lr[ev]));
            var lwid = c.measure(words, 'tick', ln ? 700 : 400), end = lx + lw, ty = bottom + 4 + tk * 0.95;
            // under the loss, ending at its right edge, or from its left edge, or flush right
            var ax = end - lwid >= 0 ? end : lx + lwid <= W ? lx : W, an = end - lwid >= 0 ? 'end' : lx + lwid <= W ? 'start' : 'end';
            var tb = c.text(ax, ty, words, { role: 'tick', weight: ln ? 700 : 400, anchor: an, max: W, fill: 'label' });
            bottom = tb.bottom;
          }
        }
        prev = r;
        y = Math.ceil(bottom) + (ph ? 14 : 16);
      });
      c.height(y - (ph ? 14 : 16) + 2);
    }
  });
})(globalThis.OAChart);
