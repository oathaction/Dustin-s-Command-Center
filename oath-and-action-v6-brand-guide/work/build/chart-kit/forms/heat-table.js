/* Heat table (coverage plan 3.15, extended; S37). Many cells with tints and printed values: rows down the left, columns
 * across, each filled cell tinted by its step on an ordered scale with its word printed in it, empty cells left blank.
 * Rows may sit under group heads. A cell whose flag column holds a value takes a small dot, explained in the key. On a
 * phone each row becomes its name with a run of tinted chips, one per filled cell, naming the column and the word.
 * encode: row (category: the row's key), row_label (text), group (category, optional), column (category), value
 * (category: the step), flag (optional: a column whose non-empty value marks the cell). Column heads alternate between
 * two levels with a hairline to their column; where a cell's word cannot fit its column, the rows become chips.
 * labels: columns ([{value, label}]: the columns in order, with their heads), steps ([{value, label}]: the scale from the
 * lowest step to the highest, each with its printed word), flag_key (the key's words for the dot), key_title. */
(function (K) {
  'use strict';
  var TINT = ['seq-2', 'seq-3', 'seq-4', 'seq-5'], DARK = { 'seq-4': 1, 'seq-5': 1 };
  K.register_chart({
    form: 'heat-table',
    name: 'Heat Table',
    family: 'tables-and-plain-words',
    encode: { row: 'category', row_label: 'text', group: 'category?', column: 'category', value: 'category', flag: 'text?' },
    labels: ['columns', 'steps', 'flag_key', 'key_title'],
    phone: 'differs',
    draw: function (c) {
      var P = K.parts, rows = c.rows, er = c.field('row'), erl = c.field('row_label'), eg = c.field('group', false);
      var ec = c.field('column'), ev = c.field('value'), ef = c.field('flag', false);
      var W = c.width, L = c.labels, cols = L.columns || [], steps = L.steps || [];
      var size = c.size('label'), tick = c.size('tick');
      var si = {}; steps.forEach(function (s, i) { si[String(s.value)] = i; });
      if (steps.length > TINT.length) c.warn('more steps than the sequential tints the form carries');
      var tint = function (v) { var i = si[String(v)]; return i === undefined ? null : TINT[Math.max(0, TINT.length - steps.length) + i]; };
      var word = function (v) { var i = si[String(v)]; return i === undefined ? String(v) : steps[i].label; };
      var cname = {}; cols.forEach(function (x) { cname[String(x.value)] = x.label; });
      // rows in data order, each with its cells
      var order = [], by = {};
      rows.forEach(function (r) {
        var k = String(r[er]);
        if (!by[k]) { by[k] = { label: r[erl], group: eg ? r[eg] : null, cells: {} }; order.push(k); }
        by[k].cells[String(r[ec])] = r;
      });
      // the key: each step's tint and word in order, then the dot
      var y = size + 2;
      var ks = steps.map(function (s) { return { label: s.label, fill: tint(s.value), ordered: true, direct: true }; });
      if (L.key_title) { c.text(0, y, L.key_title, { role: 'tick', weight: 600, fill: 'label' }); y += tick + 10; }
      y += P.key(c, ks, 0, y, W) - 4;
      if (L.flag_key && ef) {
        c.circle(5, y + 4, 3, { fill: 'subject', mark: false });
        var fk = c.text(16, y + 4 + tick * 0.35, L.flag_key, { role: 'tick', max: W - 16 });
        y = fk.bottom + 12;
      } else y += 8;
      var pad = 6, ch = Math.round(tick * 1.25) + 2 * pad - 2;
      // the grid needs each cell's word to fit its column; where it does not, the rows become chips, as on a phone
      var nw = Math.floor(W * 0.28), cw = (W - nw) / Math.max(1, cols.length), wmax = 0;
      steps.forEach(function (s2) { wmax = Math.max(wmax, c.measure(s2.label, 'tick', 600)); });
      var chips = c.phone || cw < wmax + 10;
      if (chips) {
        // a row's name, then its chips
        var lastg = null;
        order.forEach(function (k) {
          var R = by[k];
          if (eg && R.group !== lastg) { y += 10; var gb = c.text(0, y + tick, String(R.group), { role: 'tick', weight: 700, fill: 'label', max: W }); y = gb.bottom + 8; lastg = R.group; }
          var nb = c.text(0, y + size, String(R.label), { role: 'label', weight: 600, max: W });
          y = nb.bottom + 6;
          var x = 0;
          cols.forEach(function (col) {
            var r = R.cells[String(col.value)];
            if (!r) return;
            var t = col.label + ': ' + word(r[ev]), w = c.measure(t, 'tick', 600) + 2 * pad + (ef && r[ef] ? 10 : 0);
            if (x && x + w > W) { x = 0; y += ch + 4; }
            var f = tint(r[ev]);
            c.rect(x, y, w, ch, { fill: f, data: { key: k + '|' + col.value, field: ev, value: r[ev] } });
            c.text(x + pad, y + ch / 2 + tick * 0.35, t, { role: 'tick', weight: 600, fill: DARK[f] ? 'label-on-subject' : 'label' });
            if (ef && r[ef]) c.circle(x + w - pad - 3, y + ch / 2, 3, { fill: DARK[f] ? 'surface' : 'subject', mark: false });
            x += w + 4;
          });
          y += ch + 12;
        });
        c.height(y);
        return;
      }
      // the table: a name column, then one column per route. Heads alternate between two levels, so each may take two
      // columns' width, and a hairline runs from each head down to its column
      var lev = [[], []], lh2 = Math.round(tick * 1.3);
      cols.forEach(function (col, i) { lev[i % 2].push({ i: i, lines: c.wrap(col.label, 'tick', 2 * cw - 12, 600) }); });
      var h0 = Math.max.apply(null, lev[0].map(function (h) { return h.lines.length; }).concat([1])) * lh2;
      var h1 = Math.max.apply(null, lev[1].map(function (h) { return h.lines.length; }).concat([1])) * lh2;
      var top0 = y, top1 = y + h0 + 6, hb = top1 + h1 + 4;
      [0, 1].forEach(function (l) {
        lev[l].forEach(function (h) {
          var cx = nw + cw * h.i + cw / 2, base = (l ? top1 : top0) + tick, hw = 0;
          h.lines.forEach(function (ln) { hw = Math.max(hw, c.measure(ln, 'tick', 600)); });
          var tx = Math.min(Math.max(cx, nw + hw / 2), W - hw / 2 - 1);   // kept inside the artboard; the hairline stays on the column
          var tb = c.text(tx, base, cols[h.i].label, { role: 'tick', weight: 600, anchor: 'middle', max: 2 * cw - 12, fill: 'label' });
          c.line(cx, tb.bottom + 2, cx, hb + 4, { stroke: 'gridline', width: c.t('line-hairline'), mark: false });
        });
      });
      y = hb + 8;
      c.line(0, y, W, y, { stroke: 'baseline', width: c.t('line-hairline'), mark: false });
      var lastg2 = null, rh = ch + 4;
      order.forEach(function (k) {
        var R = by[k];
        if (eg && R.group !== lastg2) {
          y += 12;
          c.text(0, y + tick, String(R.group), { role: 'tick', weight: 700, fill: 'label' });
          y += tick + 8;
          c.line(0, y, W, y, { stroke: 'gridline', width: c.t('line-hairline'), mark: false });
          lastg2 = R.group;
        }
        var lines = c.wrap(String(R.label), 'tick', nw - 12, 400);
        var h = Math.max(rh, lines.length * Math.round(tick * 1.3) + 8);
        c.text(0, y + (h - (lines.length - 1) * Math.round(tick * 1.3)) / 2 + tick * 0.35, String(R.label), { role: 'tick', max: nw - 12, fill: 'label' });
        cols.forEach(function (col, i) {
          var r = R.cells[String(col.value)];
          if (!r) return;
          var f = tint(r[ev]), x = nw + cw * i + 1, top = y + 2;
          c.rect(x, top, cw - 2, h - 4, { fill: f, data: { key: k + '|' + col.value, field: ev, value: r[ev] } });
          c.text(x + (cw - 2) / 2, top + (h - 4) / 2 + tick * 0.35, word(r[ev]), { role: 'tick', weight: 600, anchor: 'middle', fill: DARK[f] ? 'label-on-subject' : 'label' });
          if (ef && r[ef]) c.circle(x + cw - 8, top + 5, 2.5, { fill: DARK[f] ? 'surface' : 'subject', mark: false });
        });
        y += h;
        c.line(0, y, W, y, { stroke: 'gridline', width: c.t('line-hairline'), mark: false });
      });
      c.height(y + 2);
    }
  });
})(globalThis.OAChart);
