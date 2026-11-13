/* Funnel (coverage plan 3.10, extended; S65). Stages of one process drawn from one base, each nested inside the one
 * before: one bar a stage from a shared left edge, so each reads against the base by length, and beside each bar what
 * the stage lost, a segment from the bar's end to the end of the stage before, named under it. A part held aside rather
 * than lost (labels.apart) sits below the stages, set off by a gap, from the same left edge. Rows that are neither print
 * in the table only. Each stage prints its count and its share of the base over its bar; the drawing is the same on a
 * phone, with shorter names where the spec gives them.
 * Inks (the data lead's round 3 ruling (b)): stages in the light fill with the context edge (the context ink on
 * Charcoal); the loss the title names (labels.named) in the subject ink; every other loss and the part held aside in the
 * track ink with the context edge. No red: a stage and a loss are areas (RF-1).
 * encode: category (text, the table's words), value (number), key (code), role (category: labels.stage marks a stage).
 * labels: stage (the role value of a stage; default "stage"), losses ({stage key: key of the row lost before it}), apart
 * ([keys] drawn below the stages), names ({key: printed name}), short ({key: name printed under 400 px}), value ('{v}' and
 * '{p}' words beside a stage's name; default '{v}, {p}'), loss ('{name}' and '{v}' words under a loss or a part held
 * aside; default '{name}: {v}'), named ([keys]).
 * formats: value, share. Maker B, round 3. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'funnel', name: 'Funnel', family: 'behavior',
    encode: { category: 'text', value: 'number', key: 'code', role: 'category' },
    labels: ['stage', 'losses', 'apart', 'names', 'short', 'value', 'loss', 'named'],
    phone: 'same',
    draw: function (c) {
      var L = c.labels, f = c.spec.formats || {}, W = c.width, sm = W < 400;
      var ec = c.field('category'), ev = c.field('value'), ek = c.field('key'), er = c.field('role');
      var sv = String(L.stage || 'stage'), names = L.names || {}, short = L.short || {};
      var named = [].concat(L.named || []).map(String), apart = [].concat(L.apart || []).map(String);
      var byk = {};
      c.rows.forEach(function (r) { byk[String(r[ek])] = r; });
      var stages = c.rows.filter(function (r) { return String(r[er]) === sv; });
      if (!stages.length) { c.warn('funnel: no row has role "' + sv + '"'); return; }
      var base = stages[0][ev], lb = c.size('label'), tk = c.size('tick');
      var nm = function (r) { var k = String(r[ek]); return sm && short[k] !== undefined ? short[k] : names[k] !== undefined ? names[k] : r[ec]; };
      var v = function (x) { return K.fmt(x, f.value || 'integer').replace(/ (million|billion|thousand)$/, ' $1'); };
      var p = function (x) { return K.fmt(100 * x / base, f.share || 'percent:1'); };
      var sx = function (x) { return (W - 1) * x / base; };
      var bh = c.t(sm ? 'bar-phone-height' : 'bar-height'), y = 0, gap = sm ? 14 : 16;
      var stage_fill = c.ground === 'charcoal' ? 'context' : 'light-fill';
      // a bar's name with its words flush right where both fit on one line, else under the name
      var head = function (name, words, wt) {
        var nb = c.text(0, y + lb * 0.95, name, { role: 'label', weight: wt, max: W });
        if (!words) return nb;
        if (c.measure(name, 'label', wt) + c.measure(words, 'label', wt, true) + 16 <= W) c.text(W, y + lb * 0.95, words, { role: 'label', weight: wt, anchor: 'end', tnum: true });
        else nb = c.text(0, nb.bottom + lb * 0.95, words, { role: 'label', weight: wt, tnum: true, max: W });
        return nb;
      };
      // a segment in the track ink with the context edge, or in the subject ink where the title names it
      var seg = function (x, by, w, k, val, isn, kind) {
        c.rect(x, by, w, bh, { fill: isn ? 'subject' : 'track', kind: kind, axis: 'x', zero: kind === 'bar' ? 0 : undefined, data: { key: k, field: ev, value: val } });
        if (!isn) c.rect(x + 0.5, by + 0.5, Math.max(0, w - 1), bh - 1, { stroke: 'context', width: 1, mark: false });
      };
      var under = function (x0, x1, by, words, isn) {
        var lw = c.measure(words, 'tick', isn ? 700 : 400), ty = by + bh + 4 + tk * 0.95;
        var right = x1 - lw >= 0, ax = right ? x1 : x0 + lw <= W ? x0 : W;
        return c.text(ax, ty, words, { role: 'tick', weight: isn ? 700 : 400, anchor: right || x0 + lw > W ? 'end' : 'start', max: W, fill: 'label' });
      };
      var prev = null;
      stages.forEach(function (r, i) {
        var k = String(r[ek]);
        var nb = head(nm(r), i === 0 ? v(r[ev]) : String(L.value || '{v}, {p}').split('{v}').join(v(r[ev])).split('{p}').join(p(r[ev])), 400);
        var by = Math.ceil(nb.bottom) + 6, w = sx(r[ev]), bottom = by + bh;
        c.rect(0, by, w, bh, { fill: stage_fill, kind: 'bar', axis: 'x', zero: 0, data: { key: k, field: ev, value: r[ev] } });
        if (stage_fill === 'light-fill') c.rect(0.5, by + 0.5, w - 1, bh - 1, { stroke: 'context', width: 1, mark: false });
        // what the stage lost since the stage before, from this bar's end to the stage before's end
        var lk = (L.losses || {})[k], lr = lk === undefined ? null : byk[String(lk)];
        if (lk !== undefined && !lr) c.warn('funnel: labels.losses names no row: ' + lk);
        if (prev && lr) {
          if (Math.abs(prev[ev] - r[ev] - lr[ev]) > 0.5) c.warn('funnel: ' + lk + ' is not the gap between ' + prev[ek] + ' and ' + k);
          var isn = named.indexOf(String(lk)) >= 0, lx = sx(r[ev]);
          seg(lx, by, sx(prev[ev]) - lx, String(lk), lr[ev], isn, 'segment');
          bottom = under(lx, sx(prev[ev]), by, String(L.loss || '{name}: {v}').split('{name}').join(nm(lr)).split('{v}').join(v(lr[ev])), isn).bottom;
        }
        prev = r;
        y = Math.ceil(bottom) + gap;
      });
      // the parts held aside, below the stages after a wider gap, from the same left edge
      apart.forEach(function (k, i) {
        var r = byk[k];
        if (!r) { c.warn('funnel: labels.apart names no row: ' + k); return; }
        if (i === 0) y += gap;
        var words = String(L.loss || '{name}: {v}').split('{name}').join(nm(r)).split('{v}').join(v(r[ev]));
        var nb = head(words, null, named.indexOf(k) >= 0 ? 700 : 400), by = Math.ceil(nb.bottom) + 6;
        seg(0, by, sx(r[ev]), k, r[ev], named.indexOf(k) >= 0, 'bar');
        y = by + bh + gap;
      });
      c.height(y - gap + 2);
    }
  });
})(globalThis.OAChart);
