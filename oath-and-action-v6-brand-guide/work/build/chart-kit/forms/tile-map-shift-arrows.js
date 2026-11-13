/* Tile-grid map with shift arrows (coverage plan 3.14, core; S12). One tile per state with a flat arrow whose length follows
 * the shift on one scale, the figure printed in the tile (DR-64); a frame marks a tile the spec singles out; gray steps on a
 * phone, where an arrow is too short to read (DR-64). DR-261 (round 4): at a desk each tile stacks the state's code over its
 * figure with the arrow beneath, and each tile is a cell (c.cell) that must hold all three with 1 px to spare; where the
 * stacked tile has no room (tiles under 46 px, drawings under 618 px) the gray steps draw instead. S12 sets stage_min 618, so a
 * desk column under 618 px draws at 618 in a frame that scrolls.
 * encode: code (code), shift (number), from (number, optional), to (number, optional).
 * labels: frame ("sign" frames a tile whose from and to differ in sign), key_title, key_steps ([1, 5, 10]), key_unit,
 * frame_label, steps ([lo, mid, hi] for the phone's three gray steps), steps_labels. formats: shift. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'tile-map-shift-arrows', name: 'Tile Grid Map With Shift Arrows', family: 'maps',
    encode: { code: 'code', shift: 'number', from: 'number?', to: 'number?' },
    labels: ['frame', 'key_title', 'key_steps', 'key_unit', 'frame_label', 'steps', 'steps_labels', 'nation_label', 'nation_code', 'lists'],
    phone: 'differs',
    draw: function (c) {
      var G = globalThis.OAChartGeo, rows = c.rows, ec = c.field('code'), es = c.field('shift'), ef = c.field('from', false), et = c.field('to', false);
      var L = c.labels, f = c.spec.formats || {}, W = c.width;
      var tm = K.parts.tiles(c), gap = tm.gap, size = tm.size, pitch = tm.pitch;
      // the phone's shaded tiles wherever a tile is too small for its code, figure and arrow (D3-93)
      // DR-261: code on line 1 (baseline 16), figure on line 2 (baseline 32, the kit's 16 px leading for 13 px text), the arrow
      // beneath with its head 2 px clear of the figure's box; the stacked tile fits where the head ends 1 px or more inside
      // the tile and the widest code or figure ends 2 px or more inside its right edge
      var hw = c.t('arrow-head-half-width'), fb2 = c.text_box(0, 32, '88.8', { role: 'tick' });
      var AY = K.snap(fb2.y + fb2.h + 2 + hw, c.t('arrow-shaft'));
      var wide = Math.max.apply(null, rows.filter(function (r) { return G.tiles[r[ec]]; }).map(function (r) {
        return Math.max(c.measure(r[ec], 'tick', 700), c.measure(K.fmt(Math.abs(r[es]), f.shift || 'number:1'), 'tick', 400)); }));
      var tight = c.phone || size < AY + hw + 1 || wide + 7 > size;
      // a shaded tile too small for its code at the smallest text size draws no code, and a note says the table names
      // every state, as the categorical tile map does (D3-93; the sweep found codes across the tiles' edges at 256 to 279 px)
      // RS-5 (round 3, second pass): as S78's tiles do, each code sits in its tile where the tile holds it with 1 px to
      // spare each side, and the codes with no room are named in a note; where more than ten have none, no tile carries a
      // code and the note says the table names every state (board 1's phone drawing printed every code at 358 px)
      var fits = function (code) { return size - 2 >= c.measure(String(code), 'tick', 600) * c.t('type-tile-code-phone') / c.size('tick'); };
      var lost = c.rows.filter(function (r) { return G.tiles[r[ec]] && !fits(r[ec]); }).map(function (r) { return r[ec]; }).sort();
      var codes = !tight || lost.length <= 10;
      var max = Math.max.apply(null, rows.map(function (r) { return Math.abs(r[es]); }));
      var ky = 0;
      // key
      if (!tight && L.key_title) {
        c.text(pitch, 14, L.key_title, { role: 'eyebrow', weight: 700, fill: 'secondary' });
        var kx = pitch;
        (L.key_steps || []).forEach(function (s) {
          var len = (size - 14) * s / max;
          K.parts.arrow(c, kx, kx + len, 36, { data: {} });
          var t = c.text(kx + len + 6, 36 + 5, K.fmt(s, 'integer') + (L.key_unit ? ' ' + L.key_unit : ''), { role: 'tick' });
          kx = t.x + t.w + 18;
        });
        c.marks = c.marks.filter(function (m) { return m.kind !== 'arrow' || (m.data && m.data.key); });
      }
      var steps = L.steps || [2, 5, 8];
      var shade = function (v) { var a = Math.abs(v); return a >= steps[2] ? 'mag-4' : a >= steps[1] ? 'mag-3' : a >= steps[0] ? 'mag-2' : 'mag-1'; };
      var top = tight ? 0 : 0;
      var nation = rows.filter(function (r) { return !G.tiles[r[ec]] && (r[ec] === 'US' || r[ec] === L.nation_code); })[0];
      if (nation && L.nation_label && !tight) {
        var ny = 58, nx = pitch;
        var nt = c.text(nx, ny, String(L.nation_label).replace('{shift}', K.fmt(Math.abs(nation[es]), f.shift || 'number:1')), { role: 'tick', weight: 700 });
        K.parts.arrow(c, nt.x + nt.w + 10, nt.x + nt.w + 10 + (size - 14) * Math.abs(nation[es]) / max, ny - 4, { data: { key: nation[ec], field: es, value: nation[es] } });
      }
      rows.forEach(function (r) {
        var t = G.tiles[r[ec]];
        if (!t) return;
        var x = t[0] * pitch, y = top + t[1] * pitch;
        var framed = L.frame === 'sign' && ef && et && (r[ef] < 0) !== (r[et] < 0);
        if (tight) {
          var sh = shade(r[es]);
          c.rect(x, y, size, size, { fill: sh, data: { key: r[ec], field: es, value: r[es] } });
          // a 1 px outline keeps the lightest step apart from the ground (access S5)
          c.rect(x + 0.5, y + 0.5, size - 1, size - 1, { stroke: 'sequential-outline', width: 1, mark: false });
          if (codes && fits(r[ec])) c.text(x + size / 2, y + size / 2 + 4, r[ec], { role: 'tick', size: c.t('type-tile-code-phone'), weight: 600, anchor: 'middle', fill: sh === 'mag-4' || sh === 'mag-3' ? 'label-on-subject' : 'label' });
        } else {
          // the track ground keeps the code and figure at 4.5 to 1 or more on both grounds, in the label ink
          c.rect(x, y, size, size, { fill: 'track', mark: false });
          // DR-261: the code over its figure, then the arrow at the tile's foot where there is room (size - 10), never above AY;
          // the tile is the cell that holds the three (D3-1546)
          c.cell(x, y, size, size, { key: r[ec] });
          c.text(x + 5, y + 16, r[ec], { role: 'tick', weight: 700, fill: 'label' });
          c.text(x + 5, y + 32, K.fmt(Math.abs(r[es]), f.shift || 'number:1'), { role: 'tick', fill: 'label' });
          var len = (size - 14) * Math.abs(r[es]) / max, ay = y + Math.max(AY, size - 10);
          var dir = r[es] >= 0 ? 1 : -1, ax = dir > 0 ? x + 7 : x + size - 7;
          K.parts.arrow(c, ax, ax + dir * len, ay, { data: { key: r[ec], field: es, value: r[es] } });
          c.cell(null);
        }
        if (framed) c.rect(x - 2, y - 2, size + 4, size + 4, { stroke: 'label', width: c.t('tile-frame'), mark: false });
      });
      ky = top + 8 * pitch;
      if (tight && L.steps_labels) {
        var yy = ky + 10, kx2 = 0;
        ['mag-1', 'mag-2', 'mag-3', 'mag-4'].forEach(function (m, i) {
          if (!L.steps_labels[i]) return;
          c.rect(kx2, yy, 14, 14, { fill: m, mark: false });
          var t = c.text(kx2 + 20, yy + 12, L.steps_labels[i], { role: 'tick' });
          kx2 = t.x + t.w + 14;
          if (kx2 > W - 80) { kx2 = 0; yy += 22; }
        });
        c.key(['mag-1', 'mag-2', 'mag-3', 'mag-4'].map(function (m) { return { fill: m, ordered: true, outline: true }; }));
        ky = yy + 22;
      }
      if (L.lists) {
        var states = rows.filter(function (r) { return G.tiles[r[ec]]; }).slice().sort(function (a, b) { return Math.abs(b[es]) - Math.abs(a[es]); });
        var n = L.lists.n || 4;
        [['largest', states.slice(0, n)], ['smallest', states.slice(-n).reverse()]].forEach(function (pair) {
          if (!L.lists[pair[0]]) return;
          ky += 22;
          var lx = c.text(0, ky, L.lists[pair[0]], { role: 'eyebrow', weight: 700, fill: 'secondary' });
          var x = tight ? 0 : lx.x + Math.max(lx.w, 120) + 14;
          if (tight) ky += 20;
          pair[1].forEach(function (r) {
            var w = c.measure(G.tiles[r[ec]][3] + ' ' + K.fmt(Math.abs(r[es]), f.shift || 'number:1'), 'tick', 600) + 16;
            if (x + w > W) { x = tight ? 0 : lx.x + Math.max(lx.w, 120) + 14; ky += 20; }
            var nb = c.text(x, ky, G.tiles[r[ec]][3], { role: 'tick', weight: 600 });
            c.text(nb.x + nb.w + 4, ky, K.fmt(Math.abs(r[es]), f.shift || 'number:1'), { role: 'tick', fill: 'secondary' });
            x += w;
          });
        });
        ky += 10;
      }
      var bot = ky + 30;
      if (L.frame_label) {
        c.rect(0.5, ky + 6.5, 13, 13, { stroke: 'label', width: c.t('tile-frame'), mark: false });
        var fb = c.text(20, ky + 18, L.frame_label, { role: 'tick', max: W - 24 });
        bot = Math.max(bot, fb.bottom + 12);   // RS-5: the note under it clears the frame's words when they wrap
        if (!codes) {
          // with no codes in the tiles, the framed states are named under the frame's words, so the drawing still says
          // which states they are (the data lead's MA-F3)
          var fr = rows.filter(function (r) { return G.tiles[r[ec]] && L.frame === 'sign' && ef && et && (r[ef] < 0) !== (r[et] < 0); })
            .map(function (r) { return G.tiles[r[ec]][3]; }).sort();
          if (fr.length) {
            var fw = fr.length > 1 ? fr.slice(0, -1).join(', ') + ' and ' + fr[fr.length - 1] : fr[0];
            fb = c.text(20, fb.bottom + 4 + c.size('tick') * 0.95, fw, { role: 'tick', weight: 600, max: W - 24 });
          }
          bot = Math.max(bot, fb.bottom + 12);
        }
      }
      if (!codes) bot = c.text(0, bot + 6, K.word('unlabeled_tiles'), { role: 'note', max: W, fill: 'secondary' }).bottom + 4;
      else if (tight && lost.length) bot = c.text(0, bot + 6, K.word('unlabeled_marks').replace('{codes}', lost.join(', ')), { role: 'note', max: W, fill: 'secondary' }).bottom + 4;
      c.height(bot);
    }
  });
})(globalThis.OAChart);
