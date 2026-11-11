/* Tile-grid map with shift arrows (coverage plan 3.14, core; S12). One tile per state with a flat arrow whose length follows
 * the shift on one scale, the figure printed in the tile (DR-64); a frame marks a tile the spec singles out; gray steps on a
 * phone, where an arrow is too short to read (DR-64).
 * encode: code (code), shift (number), from (number, optional), to (number, optional).
 * labels: frame ("sign" frames a tile whose from and to differ in sign), key_title, key_steps ([1, 5, 10]), key_unit,
 * frame_label, steps ([lo, mid, hi] for the phone's three gray steps), steps_labels. formats: shift. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'tile-map-shift-arrows', name: 'Tile Grid Map With Shift Arrows', family: 'maps',
    encode: { code: 'code', shift: 'number', from: 'number?', to: 'number?' },
    labels: ['frame', 'key_title', 'key_steps', 'key_unit', 'frame_label', 'steps', 'steps_labels'],
    phone: 'differs',
    draw: function (c) {
      var G = globalThis.OAChartGeo, rows = c.rows, ec = c.field('code'), es = c.field('shift'), ef = c.field('from', false), et = c.field('to', false);
      var L = c.labels, f = c.spec.formats || {}, W = c.width;
      var gap = c.t(c.phone ? 'tile-phone-gap' : 'tile-gap'), size = Math.min(c.t('tile-size-max'), Math.floor((W - 11 * gap) / 12)), pitch = size + gap;
      var max = Math.max.apply(null, rows.map(function (r) { return Math.abs(r[es]); }));
      var ky = 0;
      // key
      if (!c.phone && L.key_title) {
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
      var top = c.phone ? 0 : 0;
      rows.forEach(function (r) {
        var t = G.tiles[r[ec]];
        if (!t) return;
        var x = t[0] * pitch, y = top + t[1] * pitch;
        var framed = L.frame === 'sign' && ef && et && (r[ef] < 0) !== (r[et] < 0);
        if (c.phone) {
          var sh = shade(r[es]);
          c.rect(x, y, size, size, { fill: sh, data: { key: r[ec], field: es, value: r[es] } });
          c.text(x + size / 2, y + size / 2 + 4, r[ec], { role: 'tick', size: c.t('type-tile-code-phone'), weight: 600, anchor: 'middle', fill: sh === 'mag-4' || sh === 'mag-3' ? 'label-on-subject' : 'label' });
        } else {
          c.rect(x, y, size, size, { fill: 'light-fill', mark: false });
          c.text(x + 5, y + 16, r[ec], { role: 'tick', weight: 700 });
          c.text(x + 5 + c.measure(r[ec] + ' ', 'tick', 700), y + 16, K.fmt(Math.abs(r[es]), f.shift || 'number:1'), { role: 'tick', fill: 'secondary' });
          var len = (size - 14) * Math.abs(r[es]) / max, ay = y + size - 16;
          var dir = r[es] >= 0 ? 1 : -1, ax = dir > 0 ? x + 7 : x + size - 7;
          K.parts.arrow(c, ax, ax + dir * len, ay, { data: { key: r[ec], field: es, value: r[es] } });
        }
        if (framed) c.rect(x - 2, y - 2, size + 4, size + 4, { stroke: 'label', width: c.t('tile-frame'), mark: false });
      });
      ky = top + 8 * pitch;
      if (c.phone && L.steps_labels) {
        var yy = ky + 10, kx2 = 0;
        ['mag-1', 'mag-2', 'mag-3', 'mag-4'].forEach(function (m, i) {
          if (!L.steps_labels[i]) return;
          c.rect(kx2, yy, 14, 14, { fill: m, mark: false });
          var t = c.text(kx2 + 20, yy + 12, L.steps_labels[i], { role: 'tick' });
          kx2 = t.x + t.w + 14;
          if (kx2 > W - 80) { kx2 = 0; yy += 22; }
        });
        c.key(['mag-1', 'mag-2', 'mag-3', 'mag-4'].map(function (m) { return { fill: m }; }));
        ky = yy + 22;
      }
      if (L.frame_label) {
        c.rect(0.5, ky + 6.5, 13, 13, { stroke: 'label', width: c.t('tile-frame'), mark: false });
        c.text(20, ky + 18, L.frame_label, { role: 'tick', max: W - 24 });
      }
      c.height(ky + 30);
    }
  });
})(globalThis.OAChart);
