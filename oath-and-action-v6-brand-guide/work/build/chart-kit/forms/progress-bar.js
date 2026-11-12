/* Progress bar (coverage plan 3.9, core; S61). A count toward a threshold on one bar that runs to the whole: the count
 * in the subject ink from zero, the rest in the track ink, the threshold as a tick in the text's ink with its words over
 * it, and the gap between count and threshold marked under the bar with its words. Under the bar the count and the rest
 * are named, with each group's share of them in words (a vote by party in one ink, each party named: DR-48, DR-58).
 * Where the count is a vote, labels.rest "outline" draws the other side as a segment of its own in outline in the same
 * ink, and labels.ink "party" sets both sides in the party-mark ink (Rule 01.2, the data lead's RF-12).
 * encode: group (category), value (number: each group's part of the count), against (number, optional: each group's
 * part of the rest).
 * labels: of (the whole, such as 100 senators), needed (the threshold), needed_words, short_words ('{n} short'),
 * value_words ('{v} yes'), against_words ('{v} no'), groups ({group: printed name}), group_words ('{name} {v}'), ink
 * (the count's ink role, default subject), rest ("track", default, or "outline"). */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'progress-bar', name: 'Progress Bar', family: 'gauges-and-indicators',
    encode: { group: 'category', value: 'number', against: 'number?' },
    labels: ['of', 'needed', 'needed_words', 'short_words', 'value_words', 'against_words', 'groups', 'group_words', 'ink', 'rest'],
    phone: 'same',
    draw: function (c) {
      var rows = c.rows, eg = c.field('group'), ev = c.field('value'), ea = c.field('against', false), L = c.labels, W = c.width;
      var size = c.size('label'), tick = c.size('tick'), lh = Math.round(size * 1.3);
      var sum = function (f) { return rows.reduce(function (s, r) { return s + (r[f] || 0); }, 0); };
      var v = sum(ev), against = ea ? sum(ea) : null, of = L.of || (v + (against || 0)), need = L.needed;
      var fmt = function (t, n) { return String(t || '').split('{n}').join(K.fmt(n, 'integer')).split('{v}').join(K.fmt(n, 'integer')); };
      var xs = K.scale.linear([0, of], [0, W]), bh = Math.round(c.t('bar-height') * 1.25), y = 0;
      // the threshold's words over its tick, kept inside the drawing
      if (need !== undefined && L.needed_words) {
        var nw = c.measure(L.needed_words, 'label', 600), nx = Math.max(nw / 2, Math.min(W - nw / 2, xs(need)));
        c.text(nx, size, L.needed_words, { role: 'label', weight: 600, anchor: 'middle' });
        y = size + 10;
      }
      var by = y;
      var ink = L.ink || 'subject';
      c.rect(0, by, xs(v), bh, { fill: ink, kind: 'bar', axis: 'x', zero: 0, data: { key: 'count', field: ev, value: v } });
      if (L.rest === 'outline') {
        // the other side of a vote, its own segment in outline in the same ink, inside its length (Rule 01.2)
        c.rect(xs(v) + 1, by, W - xs(v) - 1, bh, { fill: 'surface', kind: 'segment', data: { key: 'rest', field: ea || 'rest', value: of - v } });
        c.rect(xs(v) + 1.6, by + 0.6, W - xs(v) - 2.2, bh - 1.2, { stroke: ink, width: 1.2, mark: false });
      } else c.rect(xs(v), by, W - xs(v), bh, { fill: 'track', kind: 'segment', data: { key: 'rest', field: ea || 'rest', value: of - v } });
      // count each group's part for the checks
      rows.forEach(function (r) { c.datum(xs(v) / 2, by + bh / 2, { data: { key: r[eg], field: ev, value: r[ev] } }); if (ea) c.datum(xs(v) + 2, by + bh / 2, { data: { key: r[eg], field: ea, value: r[ea] } }); });
      var yy = by + bh;
      if (need !== undefined) {
        c.line(xs(need), by - 6, xs(need), by + bh + 4, { stroke: 'label', width: 2, mark: false });
        // the shortfall, a bracket under the bar from the count to the threshold, with its words
        if (need > v && L.short_words) {
          var bx0 = xs(v), bx1 = xs(need), bt = by + bh + 8;
          c.line(bx0, bt, bx1, bt, { stroke: 'label', width: c.t('line-hairline'), mark: false });
          c.line(bx0, bt - 4, bx0, bt, { stroke: 'label', width: c.t('line-hairline'), mark: false });
          c.line(bx1, bt - 4, bx1, bt, { stroke: 'label', width: c.t('line-hairline'), mark: false });
          var sw = fmt(L.short_words, need - v), ww = c.measure(sw, 'label', 700), sx = Math.max(ww / 2, Math.min(W - ww / 2, (bx0 + bx1) / 2));
          var sb = c.text(sx, bt + 6 + size * 0.95, sw, { role: 'label', weight: 700, anchor: 'middle' });
          yy = sb.bottom;
        }
      }
      // the count and the rest named under the bar, each group's share listed under its side
      var names = L.groups || {}, gw = function (r, f) { var nm = names[r[eg]] !== undefined ? names[r[eg]] : String(r[eg]); return String(L.group_words || '{name} {v}').split('{name}').join(nm).split('{v}').join(K.fmt(r[f], 'integer')); };
      var listw = function (f) {
        var its = rows.filter(function (r) { return r[f] > 0; }).map(function (r) { return gw(r, f); });
        return its.length > 1 ? its.slice(0, -1).join(', ') + ' and ' + its[its.length - 1] : its.join('');
      };
      // each side's words wrap at half the width, or, where the other side is narrower, at what it leaves free
      var side = function (x, anchor, head, f, top, max) {
        var hb = c.text(x, top + size, head, { role: 'label', weight: 700, anchor: anchor }), list = listw(f);
        if (!list) return hb.bottom;
        var lb = c.text(x, hb.bottom + 2 + size * 0.95, list, { role: 'label', anchor: anchor, max: max });
        return lb.bottom;
      };
      var h1 = fmt(L.value_words || '{v}', v), w1 = Math.max(c.measure(h1, 'label', 700), Math.min(W / 2 - 12, c.measure(listw(ev), 'label')));
      var top = yy + 12, b1 = side(0, 'start', h1, ev, top, W / 2 - 12), b2 = top;
      if (ea) b2 = side(W, 'end', fmt(L.against_words || '{v}', against), ea, top, Math.max(W / 2 - 12, W - w1 - 16));
      c.height(Math.max(b1, b2) + 4);
    }
  });
})(globalThis.OAChart);
