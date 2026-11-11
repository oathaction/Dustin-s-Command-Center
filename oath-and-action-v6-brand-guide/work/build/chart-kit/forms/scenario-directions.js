/* Scenario directions (coverage plan 3.7, core; S06) and the comparison matrix (3.15, core; S06). Rows of options against
 * columns of criteria, V7's own words in every cell. scenario-directions adds a glyph and a tint for each cell's class, a
 * reading aid labeled as the studio's (never a score: no total, count or badge); comparison-matrix prints the words alone.
 * On a phone each row becomes a card that lists its columns (DR-64).
 * encode: row (id), name (text), sub (text, optional), columns (list of word columns), classes (list of class columns, same
 * order; scenario-directions only). labels: column_titles ([words]), class_style ({class: {tint, glyph}} with tint a color
 * role such as div-4 or none and glyph one of up, up-small, flat, flat-down, down, mixed, same), key_title, key ([{class,
 * label}]), id_column (true prints the row ID). */
(function (K) {
  'use strict';
  var DARK = ['subject', 'seq-4', 'seq-5', 'div-1', 'div-5', 'mag-4', 'cat-1', 'cat-2', 'cat-3'];
  function ink(tint) { return DARK.indexOf(tint) >= 0 ? 'label-on-subject' : 'label'; }
  function glyph(c, x, y, s, kind, tint) {
    var k = ink(tint);
    c.rect(x + 0.5, y + 0.5, s - 1, s - 1, { stroke: k === 'label' ? 'label' : 'surface', mark: false });
    var m = s / 2, q = s * 0.28;
    if (kind === 'up' || kind === 'up-small') { var h = kind === 'up' ? q : q * 0.7; c.polygon([[x + m, y + m - h], [x + m - h, y + m + h * 0.8], [x + m + h, y + m + h * 0.8]], { fill: k, mark: false }); }
    else if (kind === 'down') c.polygon([[x + m, y + m + q], [x + m - q, y + m - q * 0.8], [x + m + q, y + m - q * 0.8]], { fill: k, mark: false });
    else if (kind === 'flat-down') { c.line(x + 3, y + m - 2, x + s - 3, y + m - 2, { stroke: k === 'label' ? 'label' : 'surface', width: 1.5, mark: false }); c.polygon([[x + m, y + m + q], [x + m - q * 0.7, y + m + 1], [x + m + q * 0.7, y + m + 1]], { fill: k, mark: false }); }
    else if (kind === 'mixed') c.polygon([[x + m, y + 3], [x + s - 3, y + m], [x + m, y + s - 3], [x + 3, y + m]], { stroke: k === 'label' ? 'label' : 'surface', mark: false });
    else if (kind === 'same') { c.line(x + 3, y + m - 2, x + s - 3, y + m - 2, { stroke: k === 'label' ? 'label' : 'surface', width: 1.5, mark: false }); c.line(x + 3, y + m + 2, x + s - 3, y + m + 2, { stroke: k === 'label' ? 'label' : 'surface', width: 1.5, mark: false }); }
    else c.line(x + 3, y + m, x + s - 3, y + m, { stroke: k === 'label' ? 'label' : 'surface', width: 1.5, mark: false });
  }
  function draw(c, tinted) {
    var rows = c.rows, er = c.field('row'), en = c.field('name'), esub = c.field('sub', false), cols = c.field('columns'), cls = tinted ? c.field('classes') : [];
    var L = c.labels, W = c.width, titles = L.column_titles || [], st = L.class_style || {}, small = c.size('tick'), gs = 14;
    var y = 0;
    if (tinted && L.key) {
      if (L.key_title) { var kt = c.text(0, y + small, L.key_title, { role: 'tick', weight: 700, max: W }); y = kt.y + kt.h + 10; }
      var kx = 0;
      L.key.forEach(function (k) {
        var s = st[k['class']] || {}, w = gs + 8 + c.measure(k.label, 'tick') + 12;
        if (kx + w > W) { kx = 0; y += 26; }
        if (s.tint && s.tint !== 'none') c.rect(kx, y, w - 4, 22, { fill: s.tint, mark: false });
        glyph(c, kx + 4, y + 4, gs, s.glyph, s.tint);
        c.text(kx + gs + 10, y + 15.5, k.label, { role: 'tick', fill: ink(s.tint) });
        kx += w + 4;
      });
      y += 36;
      c.key(L.key.map(function (k) { var s = st[k['class']] || {}; return { fill: s.tint && s.tint !== 'none' ? s.tint : 'surface', direct: true }; }));
    }
    if (c.phone) {
      rows.forEach(function (r) {
        var head = (L.id_column ? r[er] + '  ' : '') + r[en];
        var t = c.text(0, y + c.size('label'), head, { role: 'label', weight: 700, max: W });
        y = t.y + t.h + 8;
        var subp = (L.sub || {})[r[er]] || (esub ? r[esub] : null);
        if (subp) { var sb = c.text(0, y + small, subp, { role: 'tick', fill: 'secondary', max: W }); y = sb.y + sb.h + 8; }
        cols.forEach(function (col, j) {
          var s = tinted ? (st[r[cls[j]]] || {}) : {};
          var tt = c.text(0, y + small, titles[j] || col, { role: 'tick', weight: 700, fill: 'secondary' });
          y = tt.y + tt.h + 4;
          var tx = tinted ? gs + 8 : 0;
          var lines = K.wrap(r[col], small, W - tx - 8, 400);
          var h = lines.length * Math.round(small * 1.36) + 10;
          if (tinted && s.tint && s.tint !== 'none') c.rect(0, y - 2, W, h, { fill: s.tint, data: { key: r[er] + '|' + col, field: cls[j], value: r[cls[j]] } });
          if (tinted) glyph(c, 4, y + 2, gs, s.glyph, s.tint);
          c.text(tx + 4, y + small + 1, r[col], { role: 'tick', max: W - tx - 8, fill: tinted ? ink(s.tint) : 'label', data: { key: r[er] + '|' + col } });
          y += h + 6;
        });
        y += 12;
        c.line(0, y - 8, W, y - 8, { stroke: 'gridline', width: c.t('line-hairline'), mark: false });
      });
      c.height(y);
      return;
    }
    var idw = L.id_column ? 34 : 0, nw = Math.round((W - idw) * 0.25), cw = (W - idw - nw) / cols.length;
    var hy = y, hmax = 0;
    titles.forEach(function (t, j) { var b = c.text(idw + nw + j * cw + 6, hy + small, t, { role: 'tick', weight: 700, fill: 'secondary', max: cw - 10 }); hmax = Math.max(hmax, b.y + b.h - hy); });
    y += hmax + 8;
    c.line(0, y, W, y, { stroke: 'baseline', width: c.t('line-baseline'), mark: false });
    y += 4;
    var lh = Math.round(small * 1.36);
    rows.forEach(function (r) {
      var subw = (L.sub || {})[r[er]] || (esub ? r[esub] : null);
      var nl = K.wrap(r[en], small, nw - 12, 700), sl = subw ? K.wrap(subw, small, nw - 12, 400) : [];
      var hn = nl.length * lh + (sl.length ? sl.length * lh + 6 : 0);
      var hc = 0;
      var cs = c.size('note'), clh = Math.round(cs * 1.36);
      cols.forEach(function (col) { hc = Math.max(hc, K.wrap(r[col], cs, cw - 12 - (tinted ? gs + 6 : 0), 400).length * clh); });
      var h = Math.max(hn, hc) + 16;
      if (L.id_column) c.text(0, y + 8 + small, r[er], { role: 'tick', weight: 700 });
      c.text(idw, y + 8 + small, r[en], { role: 'tick', weight: 700, max: nw - 12 });
      if (sl.length) c.text(idw, y + 8 + small + nl.length * lh + 6, subw, { role: 'tick', fill: 'secondary', max: nw - 12 });
      cols.forEach(function (col, j) {
        var x = idw + nw + j * cw, s = tinted ? (st[r[cls[j]]] || {}) : {};
        if (tinted && s.tint && s.tint !== 'none') c.rect(x + 1, y + 1, cw - 2, h - 2, { fill: s.tint, data: { key: r[er] + '|' + col, field: cls[j], value: r[cls[j]] } });
        else c.rect(x + 1, y + 1, cw - 2, h - 2, { fill: 'none', data: { key: r[er] + '|' + col, field: col } });
        var tx = x + 6;
        if (tinted) { glyph(c, tx, y + 8, gs, s.glyph, s.tint); tx += gs + 6; }
        c.text(tx, y + 8 + cs, r[col], { role: 'note', max: x + cw - tx - 6, fill: tinted ? ink(s.tint) : 'label' });
      });
      y += h;
      c.line(0, y, W, y, { stroke: 'gridline', width: c.t('line-hairline'), mark: false });
    });
    c.height(y + 2);
  }
  K.register_chart({ form: 'scenario-directions', name: 'Scenario Directions', family: 'uncertainty-and-estimates',
    encode: { row: 'id', name: 'text', sub: 'text?', columns: 'list', classes: 'list' },
    labels: ['column_titles', 'class_style', 'key_title', 'key', 'id_column', 'sub'], phone: 'differs', draw: function (c) { draw(c, true); } });
  K.register_chart({ form: 'comparison-matrix', name: 'Comparison Matrix', family: 'tables-and-plain-words',
    encode: { row: 'id', name: 'text', sub: 'text?', columns: 'list' },
    labels: ['column_titles', 'id_column', 'sub'], phone: 'differs', draw: function (c) { draw(c, false); } });
})(globalThis.OAChart);
