/* Heat table (coverage plan 3.15, extended; S37). Many cells with tints and printed values: rows down the left, columns
 * across, each filled cell tinted by its step on an ordered scale with its word printed in it, empty cells left blank.
 * Rows sit under group heads, each group gathered once (in labels.groups' order, else the order groups first appear),
 * keeping the data's order inside a group. A cell whose flag column holds a value takes a 6 px dot on a keyline of the
 * ground, explained in the key. The column heads sit on one row, each over its own column, on up to four lines. The
 * column the title names (labels.named) sets its head in bold ink and takes a hairline frame in ink; the other heads are
 * in the secondary ink. Row names sit in a column at the left where each cell's word fits on one line; above each row,
 * with words on up to two lines, where only the longest single word fits; else, or where a head's line cannot fit its
 * column, each row becomes its name with a run of tinted chips naming the column and the word (as on a phone).
 * encode: row (category: the row's key), row_label (text), group (category, optional), column (category), value
 * (category: the step), flag (optional: a column whose non-empty value marks the cell).
 * labels: columns ([{value, label, lines}]: the columns in order, with their heads; lines, optional, the head's lines as
 * set, such as ["Enforce-", "ment and", "litigation"], else the label wrapped to its column), steps ([{value, label}]: the
 * scale from the lowest step to the highest, each with its printed word), named (the column the title names), groups
 * (the group values in order), flag_key (the key's words for the dot), key_title. */
(function (K) {
  'use strict';
  var TINT = ['seq-2', 'seq-3', 'seq-4', 'seq-5'], DARK = { 'seq-4': 1, 'seq-5': 1 };
  K.register_chart({
    form: 'heat-table',
    name: 'Heat Table',
    family: 'tables-and-plain-words',
    encode: { row: 'category', row_label: 'text', group: 'category?', column: 'category', value: 'category', flag: 'text?' },
    labels: ['columns', 'steps', 'named', 'groups', 'flag_key', 'key_title'],
    phone: 'differs',
    draw: function (c) {
      var P = K.parts, rows = c.rows, er = c.field('row'), erl = c.field('row_label'), eg = c.field('group', false);
      var ec = c.field('column'), ev = c.field('value'), ef = c.field('flag', false);
      var W = c.width, L = c.labels, cols = L.columns || [], steps = L.steps || [];
      var named = L.named === undefined || L.named === null ? null : String(L.named);
      var size = c.size('label'), tick = c.size('tick'), lh3 = Math.round(tick * 1.3);
      var si = {}; steps.forEach(function (s, i) { si[String(s.value)] = i; });
      if (steps.length > TINT.length) c.warn('more steps than the sequential tints the form carries');
      var tint = function (v) { var i = si[String(v)]; return i === undefined ? null : TINT[Math.max(0, TINT.length - steps.length) + i]; };
      var word = function (v) { var i = si[String(v)]; return i === undefined ? String(v) : steps[i].label; };
      // rows in the data's order, each with its cells; then each group gathered under one head
      var order = [], by = {}, gseen = [];
      rows.forEach(function (r) {
        var k = String(r[er]);
        if (!by[k]) { by[k] = { label: r[erl], group: eg ? r[eg] : null, cells: {} }; order.push(k); }
        by[k].cells[String(r[ec])] = r;
        if (eg && gseen.indexOf(String(r[eg])) < 0) gseen.push(String(r[eg]));
      });
      if (eg) {
        var gl = (L.groups || []).map(String).filter(function (g) { return gseen.indexOf(g) >= 0; });
        gseen.forEach(function (g) { if (gl.indexOf(g) < 0) gl.push(g); });
        order = [].concat.apply([], gl.map(function (g) { return order.filter(function (k) { return String(by[k].group) === g; }); }));
      }
      // the checked mark: a 6 px dot in the subject ink on a keyline of the ground, the same in the key and every cell
      var dot = function (x, y) {
        c.circle(x, y, 3 + c.t('keyline'), { fill: 'surface', mark: false });
        c.circle(x, y, 3, { fill: 'subject', mark: false });
      };
      // the key: each step's tint and word in order, then the dot
      var y = size + 2;
      var ks = steps.map(function (s) { return { label: s.label, fill: tint(s.value), ordered: true, direct: true }; });
      if (L.key_title) { c.text(0, y, L.key_title, { role: 'tick', weight: 600, fill: 'label' }); y += tick + 10; }
      y += P.key(c, ks, 0, y, W) - 4;
      if (L.flag_key && ef) {
        dot(5, y + 4);
        var fk = c.text(16, y + 4 + tick * 0.35, L.flag_key, { role: 'tick', max: W - 16 });
        y = fk.bottom + 12;
      } else y += 8;
      var pad = 6, ch = Math.round(tick * 1.25) + 2 * pad - 2;
      // three arrangements: names in a column at the left where every word fits its cell on one line; names above each
      // row, cells across the full width and words on up to two lines, where the longest single word fits; else chips.
      // The grid also needs every head's lines to fit over their own column.
      var n = Math.max(1, cols.length), wmax = 0, wword = 0;
      steps.forEach(function (s2) {
        wmax = Math.max(wmax, c.measure(s2.label, 'tick', 600));
        String(s2.label).split(' ').forEach(function (wd) { wword = Math.max(wword, c.measure(wd, 'tick', 600)); });
      });
      var hw = function (col) { return String(col.value) === named ? 700 : 400; };
      var heads = function (cw) {
        return cols.map(function (col) { return col.lines ? col.lines.map(String) : c.wrap(col.label, 'tick', cw - 6, hw(col)); });
      };
      var fits = function (cw) {
        return heads(cw).every(function (ls, i) { return ls.every(function (ln) { return c.measure(ln, 'tick', hw(cols[i])) <= cw - 4; }); });
      };
      var left = !c.phone && (W - Math.floor(W * 0.28)) / n >= wmax + 10 && fits((W - Math.floor(W * 0.28)) / n);
      var above = !c.phone && !left && W / n >= wword + 8 && fits(W / n);
      var chips = !left && !above;
      var nw = left ? Math.floor(W * 0.28) : 0, cw = (W - nw) / n;
      var lastg = null;
      if (chips) {
        // a row's name, then its chips; the named column's chip takes the hairline frame in ink
        order.forEach(function (k) {
          var R = by[k];
          if (eg && R.group !== lastg) { y += 10; var gb = c.text(0, y + tick, String(R.group), { role: 'tick', weight: 700, fill: 'label', max: W }); y = gb.bottom + 8; lastg = R.group; }
          var nb = c.text(0, y + size, String(R.label), { role: 'label', weight: 600, max: W });
          y = nb.bottom + 6;
          var x = 0;
          cols.forEach(function (col) {
            var r = R.cells[String(col.value)];
            if (!r) return;
            var on = String(col.value) === named;
            var t = col.label + ': ' + word(r[ev]), w = c.measure(t, 'tick', on ? 700 : 600) + 2 * pad + (ef && r[ef] ? 12 : 0);
            if (x && x + w > W) { x = 0; y += ch + 4; }
            var f = tint(r[ev]);
            c.rect(x, y, w, ch, { fill: f, data: { key: k + '|' + col.value, field: ev, value: r[ev] } });
            if (on) c.rect(x + 0.5, y + 0.5, w - 1, ch - 1, { stroke: 'label', width: c.t('line-hairline'), mark: false });
            c.text(x + pad, y + ch / 2 + tick * 0.35, t, { role: 'tick', weight: on ? 700 : 600, fill: DARK[f] ? 'label-on-subject' : 'label' });
            if (ef && r[ef]) dot(x + w - pad - 3, y + ch / 2);
            x += w + 4;
          });
          y += ch + 12;
        });
        c.height(y);
        return;
      }
      // the table: a name column (at the left, or above each row), then one column per route, each head over its column
      var hl = heads(cw), hn = Math.max.apply(null, hl.map(function (ls) { return ls.length; }).concat([1]));
      var top = y, hb = top + (hn - 1) * lh3 + tick + 6;
      var ni = -1;
      cols.forEach(function (col, i) {
        var on = String(col.value) === named, cx = nw + cw * i + cw / 2;
        if (on) ni = i;
        // line by line, as set, and bottom-aligned, so every head's last line sits on one baseline over the grid
        hl[i].forEach(function (ln, j) {
          c.text(cx, top + tick + (hn - hl[i].length + j) * lh3, ln, { role: 'tick', weight: hw(col), anchor: 'middle', fill: on ? 'label' : 'secondary' });
        });
      });
      y = hb + 4;
      c.line(0, y, W, y, { stroke: 'baseline', width: c.t('line-hairline'), mark: false });
      // the named column's frame: spans where nothing is printed across it, joined into runs
      var spans = [[top - 4, y]];
      order.forEach(function (k) {
        var R = by[k];
        if (eg && R.group !== lastg) {
          var g0 = y;
          y += 12;
          var gt = c.text(0, y + tick, String(R.group), { role: 'tick', weight: 700, fill: 'label' });
          y += tick + 8;
          c.line(0, y, W, y, { stroke: 'gridline', width: c.t('line-hairline'), mark: false });
          if (left && gt.x + gt.w < nw - 4) spans.push([g0, y]);
          lastg = R.group;
        }
        var h, r0 = y;
        if (left) {
          var lines = c.wrap(String(R.label), 'tick', nw - 12, 400);
          h = Math.max(ch + 4, lines.length * lh3 + 8);
          c.text(0, y + (h - (lines.length - 1) * lh3) / 2 + tick * 0.35, String(R.label), { role: 'tick', max: nw - 12, fill: 'label' });
        } else {
          var nb3 = c.text(0, y + 6 + tick, String(R.label), { role: 'tick', weight: 600, max: W, fill: 'label' });
          y = nb3.bottom + 4;
          r0 = y;
          var two = cols.some(function (col) { var r = R.cells[String(col.value)]; return r && c.wrap(word(r[ev]), 'tick', cw - 6, 600).length > 1; });
          h = (two ? 2 : 1) * lh3 + 10;
        }
        cols.forEach(function (col, i) {
          var r = R.cells[String(col.value)];
          if (!r) return;
          var f = tint(r[ev]), x = nw + cw * i + 1, tp = y + 2;
          c.rect(x, tp, cw - 2, h - 4, { fill: f, data: { key: k + '|' + col.value, field: ev, value: r[ev] } });
          var wl = c.wrap(word(r[ev]), 'tick', cw - 6, 600).length;
          c.text(x + (cw - 2) / 2, tp + (h - 4) / 2 + tick * 0.35 - (wl - 1) * lh3 / 2, word(r[ev]), { role: 'tick', weight: 600, anchor: 'middle', max: cw - 6, leading: lh3, fill: DARK[f] ? 'label-on-subject' : 'label' });
          if (ef && r[ef]) dot(x + cw - 2 - 5, tp + 4.5);   // in the corner, above the word
        });
        y += h;
        c.line(0, y, W, y, { stroke: 'gridline', width: c.t('line-hairline'), mark: false });
        spans.push([r0, y]);
      });
      if (ni >= 0) {
        // the frame: a hairline in ink down each side of the named column, broken only where a name or group head
        // crosses it, with a cap at the top of the heads and at the foot of the grid
        var runs = [];
        spans.forEach(function (s) { var l = runs[runs.length - 1]; if (l && s[0] <= l[1] + 0.5) l[1] = Math.max(l[1], s[1]); else runs.push(s.slice()); });
        var fx0 = nw + cw * ni + 0.5, fx1 = nw + cw * (ni + 1) - 0.5, fw = c.t('line-hairline');
        runs.forEach(function (s) {
          c.line(fx0, s[0], fx0, s[1], { stroke: 'label', width: fw, mark: false });
          c.line(fx1, s[0], fx1, s[1], { stroke: 'label', width: fw, mark: false });
        });
        c.line(fx0, runs[0][0], fx1, runs[0][0], { stroke: 'label', width: fw, mark: false });
        c.line(fx0, y, fx1, y, { stroke: 'label', width: fw, mark: false });
      }
      c.height(y + 2);
    }
  });
})(globalThis.OAChart);
