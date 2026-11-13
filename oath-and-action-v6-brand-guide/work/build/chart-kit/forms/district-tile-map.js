/* District tile map (coverage plan 3.14, extended; S82). One square for each House seat, on Oath & Action's own tile
 * layout (a derived table built from the Census Bureau's district centers), drawn twice: one panel for each party, named
 * with its seats, a seat filled in its winner's panel and a ghost outline in the other, so position carries party and no
 * hue does (DR-58). The margin takes four steps of one sequential ink, every won seat with a context edge; a dot marks a seat unopposed on the ballot and
 * a ring a seat decided another way. A line runs between states, and each state's code sits in its block where the
 * block leaves room over the other party's outlines. Where a square is under 10 px the dots and rings drop and a note
 * names those seats (phone: differs).
 * encode: state (code), district (text), party (category), cls (integer: the margin's class, 1 to 4, from a derived
 * table, so every map of these results takes one set of classes), mark (category: dot, ring or empty), col and row
 * (integer: the seat's square in the tile layout).
 * labels: panels ([{value, label}] in order; {n} gives the party's seats), step_labels (four words), key_title,
 * mark_labels ({dot, ring}), ghost_label, small ({dot, ring}: the note's words where marks drop; {seats} fills),
 * codes_note (words under the map naming states whose code found no room in either panel; {codes} fills), at_large
 * (words for an at-large seat in the note's lists, {state} the state's name: "Alaska at large", so a two-letter code
 * stands for a state only; C-S6, round 3 fix pass). */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'district-tile-map', name: 'District Tile Map', family: 'maps',
    encode: { state: 'code', district: 'text', party: 'category', cls: 'integer', mark: 'category?', col: 'integer', row: 'integer' },
    labels: ['panels', 'step_labels', 'key_title', 'mark_labels', 'ghost_label', 'small', 'codes_note', 'at_large'],
    phone: 'differs',
    draw: function (c) {
      var L = c.labels, W = c.width, es = c.field('state'), ed = c.field('district'), ep = c.field('party');
      var ek = c.field('cls'), emk = c.field('mark', false), ecol = c.field('col'), erow = c.field('row');
      var at = {}, cols = 0, nrows = 0;
      var seats = c.rows.map(function (r) {
        cols = Math.max(cols, r[ecol] + 1); nrows = Math.max(nrows, r[erow] + 1); at[r[es] + '|' + r[ed]] = 1;
        return { r: r, col: r[ecol], row: r[erow], st: r[ek], mk: (emk && r[emk]) || null };
      });
      var gap = W >= 560 ? 2 : 1, pitch = Math.floor((W + gap) / cols * 10) / 10, size = pitch - gap;
      var big = size >= 10, gi = size >= 10 ? 2 : size >= 6 ? 1 : 0;   // a ghost sits inset, so it never reads as the lightest step   // dots and rings only where a square holds them (ruling (b))
      // the margin's four classes on sequential steps 2 to 5 of one ink, every won seat with its 1 px context edge, so the
      // closest races read as filled beside the other party's empty outlines (the data lead's C-1, round 3)
      var y = 0, ink = function (s) { return 'seq-' + (s + 1); }, named = {};
      // the key: the four steps, then the marks and the outline
      if (L.key_title) { var kt = c.text(0, y + 13, L.key_title, { role: 'eyebrow', weight: 700, fill: 'secondary', max: W }); y = kt.bottom + 6; }
      var sw = 14, kx = 0, ky = y + 14, row_h = 22;
      var swatch = function (x, yb, s, mk) {
        c.rect(x, yb - 11, sw, sw, { fill: ink(s), mark: false });
        c.rect(x + 0.5, yb - 10.5, sw - 1, sw - 1, { stroke: 'context', width: 1, mark: false });
        if (mk) mark_at(x + sw / 2, yb - 11 + sw / 2, sw, s, mk);
      };
      var mark_at = function (cx, cy, sz, s, mk) {
        var on = 'on-' + ink(s);   // the step's own label ink
        if (mk === 'dot') c.circle(cx, cy, Math.max(1.75, sz * 0.14), { fill: on, mark: false });
        else { c.circle(cx, cy, Math.max(2.5, sz * 0.27), { fill: on, mark: false }); c.circle(cx, cy, Math.max(2.5, sz * 0.27) - 1.5, { fill: ink(s), mark: false }); }
      };
      var entries = (L.step_labels || []).map(function (w, i) { return { w: w, s: i + 1 }; });
      if (big && L.mark_labels) { if (L.mark_labels.dot) entries.push({ w: L.mark_labels.dot, s: 4, mk: 'dot' }); if (L.mark_labels.ring) entries.push({ w: L.mark_labels.ring, s: 2, mk: 'ring' }); }
      if (L.ghost_label) entries.push({ w: L.ghost_label, ghost: true });
      entries.forEach(function (e) {
        var tw = c.measure(e.w, 'tick'), need = sw + 6 + tw;
        if (kx > 0 && kx + need > W) { kx = 0; ky += row_h; }
        if (e.ghost) c.rect(kx + 2.5, ky - 8.5, sw - 5, sw - 5, { stroke: 'ghost', width: 1, mark: false });
        else swatch(kx, ky, e.s, e.mk);
        var tb = c.text(kx + sw + 6, ky, e.w, { role: 'tick', max: W - kx - sw - 6 });
        kx = tb.x + tb.w + 18;
        if (tb.lines > 1) { kx = 0; ky = tb.bottom + 14; }
      });
      c.key([1, 2, 3, 4].map(function (s) { return { fill: ink(s), ordered: true, outline: true }; }));
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
            c.rect(x, yy, size, size, { fill: ink(s.st), data: { key: key, field: ek, value: s.st, party: s.r[ep] } });
            c.rect(x + 0.5, yy + 0.5, size - 1, size - 1, { stroke: 'context', width: 1, mark: false });
            if (big && s.mk) mark_at(x + size / 2, yy + size / 2, size, s.st, s.mk);
          } else c.rect(x + gi + 0.5, yy + gi + 0.5, size - 2 * gi - 1, size - 2 * gi - 1, { stroke: 'ghost', width: 1, mark: false });
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
        c.path(d, { stroke: 'context', width: gap >= 2 ? 1.5 : 1 });
        // each state's code in its block, over outlines or light squares only, nearest the block's middle
        var by = {}, placed = [];
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
            if (placed.some(function (p) { return bx < p.x + p.w + 2 && p.x < bx + b0.w + 2 && byy < p.y + p.h + 2 && p.y < byy + b0.h + 2; })) ok = false;
            // every square the words touch is this state's, and an outline or one of the two light steps here
            for (var col = Math.floor(bx / pitch); ok && col <= Math.floor((bx + b0.w) / pitch); col++) {
              for (var row = Math.floor((byy - top) / pitch); ok && row <= Math.floor((byy + b0.h - top) / pitch); row++) {
                var o = own[col + ',' + row];
                var touches = X(col) < bx + b0.w && X(col) + size > bx && Y(row) < byy + b0.h && Y(row) + size > byy;
                if (!touches) continue;
                if (!o || o.r[es] !== st) ok = false;
                else if (String(o.r[ep]) === String(pn.value)) ok = false;   // a code sits over outlines only
              }
            }
            if (ok) { c.text(cands[i][0], byy - b0.y, st, { role: 'tick', weight: 700, anchor: 'middle', halo: true }); placed.push({ x: bx, y: byy, w: b0.w, h: b0.h }); named[st] = true; break; }
          }
        });
        y = Y(nrows - 1) + size + (pi < (L.panels || []).length - 1 ? 26 : 8);
      });
      // a state whose squares left no room for its code in either panel is named under the map; the table names every seat
      var none = Object.keys(at).map(function (k) { return k.split('|')[0]; }).filter(function (st, i, a) { return a.indexOf(st) === i && !named[st]; }).sort();
      if (none.length && L.codes_note) { var cn = c.text(0, y + 16, String(L.codes_note).replace('{codes}', none.join(', ')), { role: 'note', fill: 'secondary', max: W }); y = cn.bottom + 4; }
      // where the squares are too small for dots and rings, the note names those seats
      if (!big && L.small) {
        ['dot', 'ring'].forEach(function (mk) {
          if (!L.small[mk]) return;
          var seat = function (s) {
            var tl = globalThis.OAChartGeo && globalThis.OAChartGeo.tiles[s.r[es]];
            return String(s.r[ed]) === '00' && L.at_large && tl ? String(L.at_large).replace('{state}', tl[3]) : s.r[es] + ' ' + s.r[ed];
          };
          var list = seats.filter(function (s) { return s.mk === mk; }).map(seat);
          if (!list.length) return;
          var nt = c.text(0, y + 16, String(L.small[mk]).replace('{seats}', list.join(', ')), { role: 'note', fill: 'secondary', max: W });
          y = nt.bottom + 4;
        });
      }
      c.height(y + 4);
    }
  });
})(globalThis.OAChart);
