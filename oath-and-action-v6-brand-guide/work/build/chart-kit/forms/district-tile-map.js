/* District tile map (coverage plan 3.14, extended; S82). One square for each House seat, on Oath & Action's own tile
 * layout (a derived table built from the Census Bureau's district centers), drawn twice: one panel for each party, named
 * with its seats, a seat filled in its winner's panel and a ghost outline in the other, so position carries party and no
 * hue does (DR-58). The margin takes four gray steps, closer races lighter; a dot marks a seat unopposed on the ballot and
 * a ring a seat decided another way. A line runs between states, and each state's code sits in its block where the
 * block leaves room over outlines or light squares. Where a square is under 10 px the dots and rings drop and a note
 * names those seats (phone: differs).
 * encode: state (code), district (text), party (category), margin (number), kind (category).
 * labels: layout (the layout dataset: state, district, col, row), panels ([{value, label}] in order; {n} gives the
 * party's seats), steps ([5, 10, 20]), step_labels (four words), key_title, marks ({kind: 'dot' | 'ring'}),
 * mark_labels ({dot, ring}), ghost_label, small ({dot, ring}: the note's words where marks drop; {seats} fills). */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'district-tile-map', name: 'District Tile Map', family: 'maps',
    encode: { state: 'code', district: 'text', party: 'category', margin: 'number?', kind: 'category' },
    labels: ['layout', 'panels', 'steps', 'step_labels', 'key_title', 'marks', 'mark_labels', 'ghost_label', 'small'],
    phone: 'differs', extra: true,
    draw: function (c) {
      var L = c.labels, W = c.width, es = c.field('state'), ed = c.field('district'), ep = c.field('party');
      var em = c.field('margin'), ek = c.field('kind');
      var lay = (c.extra || {})[L.layout];
      if (!lay) throw new Error('labels.layout names no dataset this spec carries');
      var at = {}, cols = 0, nrows = 0;
      lay.forEach(function (r) { at[r.state + '|' + r.district] = r; cols = Math.max(cols, r.col + 1); nrows = Math.max(nrows, r.row + 1); });
      var steps = L.steps || [5, 10, 20], marks = L.marks || {};
      // a seat's class follows its margin as printed, to one decimal (ruling (f))
      var step = function (m) {
        if (m === null || m === undefined || m === '') return 4;
        var v = Math.round(m * 10) / 10;
        return v < steps[0] ? 1 : v < steps[1] ? 2 : v < steps[2] ? 3 : 4;
      };
      var seats = c.rows.map(function (r) {
        var t = at[r[es] + '|' + r[ed]];
        if (!t) { c.warn('no square for ' + r[es] + ' ' + r[ed]); return null; }
        return { r: r, col: t.col, row: t.row, st: step(r[em]), mk: marks[r[ek]] || null };
      }).filter(Boolean);
      var gap = W >= 560 ? 2 : 1, pitch = Math.floor((W + gap) / cols * 10) / 10, size = pitch - gap;
      var big = size >= 10;   // dots and rings only where a square holds them (ruling (b))
      var y = 0, ink = function (s) { return 'mag-' + s; };
      // the key: the four steps, then the marks and the outline
      if (L.key_title) { var kt = c.text(0, y + 13, L.key_title, { role: 'eyebrow', weight: 700, fill: 'secondary', max: W }); y = kt.bottom + 6; }
      var sw = 14, kx = 0, ky = y + 14, row_h = 22;
      var swatch = function (x, yb, s, mk) {
        c.rect(x, yb - 11, sw, sw, { fill: ink(s), mark: false });
        if (s === 1) c.rect(x + 0.5, yb - 10.5, sw - 1, sw - 1, { stroke: 'context', width: 1, mark: false });
        if (mk) mark_at(x + sw / 2, yb - 11 + sw / 2, sw, s, mk);
      };
      var mark_at = function (cx, cy, sz, s, mk) {
        var on = s >= 3 ? 'label-on-subject' : 'label';
        if (mk === 'dot') c.circle(cx, cy, Math.max(1.75, sz * 0.14), { fill: on, mark: false });
        else { c.circle(cx, cy, Math.max(2.5, sz * 0.27), { fill: on, mark: false }); c.circle(cx, cy, Math.max(2.5, sz * 0.27) - 1.5, { fill: ink(s), mark: false }); }
      };
      var entries = (L.step_labels || []).map(function (w, i) { return { w: w, s: i + 1 }; });
      if (big && L.mark_labels) { if (L.mark_labels.dot) entries.push({ w: L.mark_labels.dot, s: 4, mk: 'dot' }); if (L.mark_labels.ring) entries.push({ w: L.mark_labels.ring, s: 2, mk: 'ring' }); }
      if (L.ghost_label) entries.push({ w: L.ghost_label, ghost: true });
      entries.forEach(function (e) {
        var tw = c.measure(e.w, 'tick'), need = sw + 6 + tw;
        if (kx > 0 && kx + need > W) { kx = 0; ky += row_h; }
        if (e.ghost) c.rect(kx + 0.5, ky - 10.5, sw - 1, sw - 1, { stroke: 'ghost', width: 1, mark: false });
        else swatch(kx, ky, e.s, e.mk);
        var tb = c.text(kx + sw + 6, ky, e.w, { role: 'tick', max: W - kx - sw - 6 });
        kx = tb.x + tb.w + 18;
        if (tb.lines > 1) { kx = 0; ky = tb.bottom + 14; }
      });
      c.key([1, 2, 3, 4].map(function (s) { return { fill: ink(s), ordered: true, outline: s === 1 }; }));
      y = ky + 18;
      // one panel for each party, Democrats first (S48's order)
      (L.panels || []).forEach(function (pn, pi) {
        var n = seats.filter(function (s) { return String(s.r[ep]) === String(pn.value); }).length;
        var nb = c.text(0, y + 15, String(pn.label).replace('{n}', K.fmt(n, 'integer')), { role: 'label', weight: 700, max: W });
        var top = nb.bottom + 8, own = {};
        seats.forEach(function (s) { own[s.col + ',' + s.row] = s; });
        var X = function (col) { return col * pitch; }, Y = function (row) { return top + row * pitch; };
        seats.forEach(function (s) {
          var x = X(s.col), yy = Y(s.row), key = s.r[es] + ' ' + s.r[ed];
          if (String(s.r[ep]) === String(pn.value)) {
            c.rect(x, yy, size, size, { fill: ink(s.st), data: { key: key, field: em, value: s.r[em] === null ? '' : s.r[em], party: s.r[ep] } });
            if (s.st === 1) c.rect(x + 0.5, yy + 0.5, size - 1, size - 1, { stroke: 'context', width: 1, mark: false });
            if (big && s.mk) mark_at(x + size / 2, yy + size / 2, size, s.st, s.mk);
          } else c.rect(x + 0.5, yy + 0.5, size - 1, size - 1, { stroke: 'ghost', width: 1, mark: false });
        });
        // lines between states and round the map, in the gaps between squares
        var d = '', half = gap / 2;
        seats.forEach(function (s) {
          var x = X(s.col), yy = Y(s.row), st = s.r[es];
          var other = function (dc, dr) { var o = own[(s.col + dc) + ',' + (s.row + dr)]; return !o || o.r[es] !== st; };
          if (other(1, 0)) d += 'M' + K.round(x + size + half) + ',' + K.round(yy - half) + 'V' + K.round(yy + size + half);
          if (other(-1, 0)) d += 'M' + K.round(x - half) + ',' + K.round(yy - half) + 'V' + K.round(yy + size + half);
          if (other(0, 1)) d += 'M' + K.round(x - half) + ',' + K.round(yy + size + half) + 'H' + K.round(x + size + half);
          if (other(0, -1)) d += 'M' + K.round(x - half) + ',' + K.round(yy - half) + 'H' + K.round(x + size + half);
        });
        c.path(d, { stroke: 'baseline', width: W >= 560 ? 1.5 : 1 });
        // each state's code in its block, over outlines or light squares only, nearest the block's middle
        var by = {};
        seats.forEach(function (s) { (by[s.r[es]] = by[s.r[es]] || []).push(s); });
        Object.keys(by).sort().forEach(function (st) {
          var cells = by[st], mx = 0, my = 0;
          cells.forEach(function (s) { mx += X(s.col) + size / 2; my += Y(s.row) + size / 2; });
          mx /= cells.length; my /= cells.length;
          var b0 = c.text_box(0, 0, st, { role: 'tick', weight: 700 }), cands = [];
          cells.forEach(function (s) {
            [[0, 0], [0.5, 0], [0, 0.5], [0.5, 0.5]].forEach(function (o) { cands.push([X(s.col) + size / 2 + o[0] * pitch, Y(s.row) + size / 2 + o[1] * pitch]); });
          });
          cands.sort(function (a, b) { return Math.hypot(a[0] - mx, a[1] - my) - Math.hypot(b[0] - mx, b[1] - my) || a[1] - b[1] || a[0] - b[0]; });
          for (var i = 0; i < cands.length; i++) {
            var bx = cands[i][0] - b0.w / 2, byy = cands[i][1] - b0.h / 2, ok = bx >= 0 && bx + b0.w <= W;
            // every square the words touch is this state's, and an outline or one of the two light steps here
            for (var col = Math.floor(bx / pitch); ok && col <= Math.floor((bx + b0.w) / pitch); col++) {
              for (var row = Math.floor((byy - top) / pitch); ok && row <= Math.floor((byy + b0.h - top) / pitch); row++) {
                var o = own[col + ',' + row];
                var touches = X(col) < bx + b0.w && X(col) + size > bx && Y(row) < byy + b0.h && Y(row) + size > byy;
                if (!touches) continue;
                if (!o || o.r[es] !== st) ok = false;
                else if (String(o.r[ep]) === String(pn.value) && (o.st >= 3 || (big && o.mk))) ok = false;
              }
            }
            if (ok) { c.text(cands[i][0], byy - b0.y + b0.y, st, { role: 'tick', weight: 700, anchor: 'middle', halo: true }); break; }
          }
        });
        y = Y(nrows - 1) + size + (pi < (L.panels || []).length - 1 ? 26 : 8);
      });
      // where the squares are too small for dots and rings, the note names those seats
      if (!big && L.small) {
        ['dot', 'ring'].forEach(function (mk) {
          if (!L.small[mk]) return;
          var list = seats.filter(function (s) { return s.mk === mk; }).map(function (s) { return s.r[es] + ' ' + s.r[ed]; });
          if (!list.length) return;
          var nt = c.text(0, y + 16, String(L.small[mk]).replace('{seats}', list.join(', ')), { role: 'note', fill: 'secondary', max: W });
          y = nt.bottom + 4;
        });
      }
      c.height(y + 4);
    }
  });
})(globalThis.OAChart);
