/* Population pyramid (coverage plan 3.5, extended; S53). A population by single year of age and by sex: one thin bar a
 * year of age for each side, the youngest at the bottom, one side growing left from the center and the other right on one
 * scale, ages labeled down the center, both sides in one ink with sex carried by position and named over each half (the
 * data lead's ruling (e)). A band of ages the title names takes the red point on both sides as one job (labels.point, a
 * range of ages), or the subject ink (labels.named), its words in the empty upper left; every other age takes the light
 * fill. Ages a story needs, such as 65, may be marked as hairlines in the secondary ink, named at the right edge. The
 * scale runs along the bottom of each half, mirrored.
 * encode: age (number), sex (category), value (number).
 * labels: left (the sex value drawn on the left), right (the one drawn on the right), sides ({value: printed name}),
 * point or named ({from, to}: the band of ages), band_words (the band's words), marks ([{age, words}]: hairlines at the
 * age's lower edge), age_step (ages labeled every this many years; default 10), top (words for the top age, such as
 * "100+"), axis (words under the scale).
 * formats: tick. On a phone the same arrangement draws narrower. Maker B, round 2. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'population-pyramid',
    name: 'Population Pyramid',
    family: 'distribution-and-density',
    encode: { age: 'number', sex: 'category', value: 'number' },
    labels: ['left', 'right', 'sides', 'point', 'named', 'band_words', 'marks', 'age_step', 'top', 'axis'],
    phone: 'same',
    draw: function (c) {
      var P = K.parts, L = c.labels, f = c.spec.formats || {}, W = c.width, ph = c.phone;
      var ea = c.field('age'), es = c.field('sex'), ev = c.field('value');
      var tick = c.size('tick'), size = c.size('label'), ft = f.tick || 'millions-value:1';
      var left = String(L.left), right = String(L.right), sides = L.sides || {};
      var rowsL = c.rows.filter(function (r) { return String(r[es]) === left; }), rowsR = c.rows.filter(function (r) { return String(r[es]) === right; });
      if (!rowsL.length || !rowsR.length) c.warn('labels.left and labels.right must each name a sex value in the rows');
      var ages = c.rows.map(function (r) { return r[ea]; }), amin = Math.min.apply(null, ages), amax = Math.max.apply(null, ages);
      var vmax = Math.max.apply(null, rowsL.concat(rowsR).map(function (r) { return r[ev]; }));
      // the band of ages the title names: labels.point gives it the red point on both sides as one job (ruling (a)),
      // labels.named the subject ink; every other age takes the light fill
      var band = L.point || L.named || null, inband = function (r) { return band && r[ea] >= band.from && r[ea] <= band.to; };
      var bandRole = L.point ? 'point' : 'subject', other = c.ground === 'charcoal' ? 'context' : 'light-fill';
      if (band) band = { from: band.from, to: band.to, words: L.band_words };
      // the center column for the ages, and the two halves
      var aw = Math.ceil(Math.max(c.measure(String(amax), 'tick'), L.top ? c.measure(L.top, 'tick') : 0)) + (ph ? 12 : 20);
      var cx = W / 2, half = cx - aw / 2;
      // the scale ends at the next half step past the largest bar, so the bars fill their halves
      var nk = K.nice(0, vmax, ph ? 2 : 3), hi = Math.ceil(vmax / (nk.step / 2) - 1e-9) * nk.step / 2, ticks = K.ticks(0, hi, 0, nk.step);
      var sc = K.scale.linear([0, hi], [0, half - 4]);
      var y = 0;
      // the sides' names over their halves
      var nl = sides[left] !== undefined ? sides[left] : left, nr = sides[right] !== undefined ? sides[right] : right;
      c.text(cx - aw / 2 - 4, size, nl, { role: 'label', weight: 700, anchor: 'end' });
      c.text(cx + aw / 2 + 4, size, nr, { role: 'label', weight: 700 });
      y = size + 10;
      var n = amax - amin + 1, bh = ph ? 3 : 4, top = y, bot = top + n * bh;
      var ay = function (a) { return bot - (a - amin + 1) * bh; };
      // gridlines at the scale's ticks, on both halves
      ticks.forEach(function (t) {
        if (!t) return;
        c.line(cx - aw / 2 - sc(t), top, cx - aw / 2 - sc(t), bot, { stroke: 'gridline', width: c.t('line-hairline'), mark: false });
        c.line(cx + aw / 2 + sc(t), top, cx + aw / 2 + sc(t), bot, { stroke: 'gridline', width: c.t('line-hairline'), mark: false });
      });
      // the bars: the left side grows left from the center column's edge, the right side right
      var draw = function (r, dir) {
        var role = inband(r) ? bandRole : other, w = sc(r[ev]), x = dir < 0 ? cx - aw / 2 - w : cx + aw / 2;
        var kl = {};   // the band's keyline is one outline round each side's bars, drawn after them, never a stripe a bar
        // the band's bars on both sides are one job, so they count as one working red (ED-E15)
        c.rect(x, ay(r[ea]), w, bh, Object.assign({ fill: role, kind: 'bar', axis: 'x', zero: dir < 0 ? cx - aw / 2 : cx + aw / 2, job: inband(r) ? 'band' : undefined, data: { key: r[es] + '|' + r[ea], field: ev, value: r[ev] } }, kl));
      };
      rowsL.forEach(function (r) { draw(r, -1); });
      rowsR.forEach(function (r) { draw(r, 1); });
      c.line(cx - aw / 2, top, cx - aw / 2, bot, { stroke: 'baseline', width: c.t('line-hairline'), mark: false });
      c.line(cx + aw / 2, top, cx + aw / 2, bot, { stroke: 'baseline', width: c.t('line-hairline'), mark: false });
      // age marks: a hairline in the secondary ink across the right half at the age's lower edge, named at the right end
      var mtexts = [];
      (L.marks || []).forEach(function (m) {
        var my = ay(m.age) + bh;
        c.line(cx + aw / 2, my, W, my, { stroke: 'secondary', width: c.t('line-hairline'), mark: false });
        mtexts.push({ y: my, words: m.words });
      });
      // the ages down the center
      var step = L.age_step || 10;
      for (var a = amin; a <= amax; a += step) {
        var words = a === amax && L.top ? L.top : String(a);
        c.text(cx, ay(a) + bh / 2 + tick * 0.35, words, { role: 'tick', anchor: 'middle' });
      }
      // the red band's keyline on Newsprint: one outline round each side's bars, so the band reads as one shape
      if (band && bandRole === 'point' && c.ground !== 'charcoal') {
        [[rowsL, -1], [rowsR, 1]].forEach(function (sd) {
          var bars = sd[0].filter(inband).sort(function (a, b) { return a[ea] - b[ea]; }), dir = sd[1], e0 = dir < 0 ? cx - aw / 2 : cx + aw / 2;
          if (!bars.length) return;
          var d = 'M' + K.round(e0) + ',' + K.round(ay(bars[0][ea]) + bh);
          bars.forEach(function (r) { var xe = e0 + dir * sc(r[ev]); d += 'L' + K.round(xe) + ',' + K.round(ay(r[ea]) + bh) + 'L' + K.round(xe) + ',' + K.round(ay(r[ea])); });
          d += 'L' + K.round(e0) + ',' + K.round(ay(bars[bars.length - 1][ea])) + 'Z';
          c.path(d, { fill: 'none', stroke: 'point-keyline', width: c.t('keyline'), mark: false });
        });
      }
      // the band's words in the empty corner over the left half's oldest ages, where every width has room
      // the band's words in the empty corner over the left half's oldest ages, where every width has room; with no halo, so the
      // kit clears the gridlines behind them with a knockout of the ground (BC S1)
      if (band && band.words) {
        var lh2 = Math.round(size * 1.2), blines = c.wrap(band.words, 'label', Math.max(60, half - 24), 700);
        blines.forEach(function (ln, i) { c.text(0, top + size + i * lh2, ln, { role: 'label', weight: 700 }); });
      }
      mtexts.forEach(function (m) {
        var mw = c.measure(m.words, 'tick'), x = W;
        if (mprev && Math.abs(mprev.y - m.y) < tick + 2) x = mprev.x - mprev.w - 8;
        c.text(x, m.y - 4, m.words, { role: 'tick', anchor: 'end', fill: 'secondary', halo: true });
        mprev = { x: x, y: m.y, w: mw };
      });
      // the scale along the bottom of each half, mirrored
      var sy = bot + tick + 8;
      ticks.forEach(function (t) {
        if (!t) return;
        var w = K.fmt(t, ft);
        [cx - aw / 2 - sc(t), cx + aw / 2 + sc(t)].forEach(function (x, i) {
          c.line(x, bot, x, bot + 4, { stroke: 'baseline', width: c.t('line-hairline'), mark: false });
          var tw = c.measure(w, 'tick'), an = x - tw / 2 < 0 ? 'start' : x + tw / 2 > W ? 'end' : 'middle';
          c.text(an === 'start' ? 0 : an === 'end' ? W : x, sy, w, { role: 'tick', anchor: an });
        });
      });
      var end = sy + 4;
      if (L.axis) { var xb = c.text(cx, sy + tick + 10, L.axis, { role: 'tick', weight: 600, anchor: 'middle', max: W }); end = xb.bottom; }
      c.height(end + 2);
    }
  });
})(globalThis.OAChart);
