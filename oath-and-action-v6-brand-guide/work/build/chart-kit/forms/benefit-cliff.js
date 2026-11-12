/* Benefit-cliff line (coverage plan 3.3, extended; S35). What a household keeps as its earnings rise: the household's
 * resources after taxes and benefits as a Charcoal line against its earnings, beside a thin diagonal of earnings alone. The
 * largest drop between two steps is the cliff: a light band runs from it to the earnings where the household is back to
 * what it had before the drop, and words name the drop and the climb back.
 * encode: x (number: earnings), y (number: resources). labels: ref (words on the diagonal of earnings alone; no diagonal
 * when left out), line (words on the resources line), cliff (words at the drop, with {drop}, {from_x}, {to_x}), band (words
 * in the band, with {from_x} and {back_x}), x_title (words under the earnings axis). formats: x, y, drop (in the words),
 * tick. Maker B, round 1. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'benefit-cliff',
    name: 'Benefit Cliff Line',
    family: 'change-over-time',
    encode: { x: 'number', y: 'number' },
    labels: ['ref', 'line', 'cliff', 'band', 'x_title'],
    phone: 'same',
    draw: function (c) {
      var P = K.parts, L = c.labels, f = c.spec.formats || {}, W = c.width, ex = c.field('x'), ey = c.field('y');
      var rows = c.rows.slice().sort(function (a, b) { return a[ex] - b[ex]; }), n = rows.length;
      var xlo = rows[0][ex], xhi = rows[n - 1][ex];
      var vmax = Math.max(Math.max.apply(null, rows.map(function (r) { return r[ey]; })), L.ref ? xhi : 0);
      var vs = P.value_scale(c, 0, vmax, 5), ticks = vs.ticks;
      // on a phone the two lines' words cannot sit on the lines without crossing them, so they become a key (Rule 14.3)
      var keyh = 0;
      if (c.phone && (L.line || L.ref)) {
        var ke = [];
        if (L.line) ke.push({ label: L.line, shape: 'line', stroke: 'subject', width: c.t('line-subject'), direct: true });
        if (L.ref) ke.push({ label: L.ref, shape: 'line', stroke: 'context', width: c.t('line-context'), dash: '4 3', direct: true });
        keyh = P.key(c, ke, 0, c.size('label') + 2, W) + 10;
      }
      var top = keyh + c.size('tick') + 6, plotH = c.t(c.phone ? 'columns-phone-height' : 'columns-height'), bot = top + plotH;
      var gut = P.value_gutter(c, ticks, f.tick || 'integer');
      var x0 = gut + 8, x1 = W - (c.phone ? 8 : 16);
      var ys = K.scale.linear([vs.lo, vs.hi], [bot, top]), xs = K.scale.linear([xlo, xhi], [x0, x1]);
      // the cliff: the largest drop from one step to the next, and the first step back at or above the level before it
      var ci = -1, best = 0;
      for (var i = 1; i < n; i++) { var d = rows[i - 1][ey] - rows[i][ey]; if (d > best) { best = d; ci = i; } }
      var back = null;
      if (ci > 0) for (var j = ci; j < n; j++) if (rows[j][ey] >= rows[ci - 1][ey]) { back = rows[j]; break; }
      var fill = function (t) {
        return String(t).replace('{drop}', K.fmt(best, f.drop || f.y || 'integer')).replace('{from_x}', K.fmt(rows[ci - 1][ex], f.x || 'integer'))
          .replace('{to_x}', K.fmt(rows[ci][ex], f.x || 'integer')).replace('{back_x}', back ? K.fmt(back[ex], f.x || 'integer') : '');
      };
      // the band from the drop to the climb back, under everything
      if (ci > 0) {
        var bx0 = xs(rows[ci - 1][ex]), bx1 = back ? xs(back[ex]) : x1;
        c.rect(bx0, top, bx1 - bx0, bot - top, { fill: 'band', mark: false });
      }
      // the x axis's ticks share the value axis's steps where the two scales match
      P.value_grid(c, ys, ticks, f.tick || 'integer', x0, x1, gut);
      P.zero_line(c, ys, x0, x1);
      // the earnings axis: as many round steps as fit side by side
      var xt, cnt = 6, wmax = c.measure(K.fmt(xhi, f.tick || 'integer'), 'tick') + 14, ay = bot + c.size('tick') + 10;
      do { xt = K.ticks(xlo, xhi, cnt); cnt--; } while (cnt > 1 && xt.length > 1 && xs(xt[1]) - xs(xt[0]) < wmax);
      var boxes = xt.map(function (t) {
        var s2 = K.fmt(t, f.tick || 'integer'), w = c.measure(s2, 'tick'), x = xs(t), anchor = x + w / 2 > W ? 'end' : x - w / 2 < x0 - gut ? 'start' : 'middle';
        return { t: t, s: s2, x: x, anchor: anchor, l: anchor === 'end' ? x - w : anchor === 'start' ? x : x - w / 2, r: anchor === 'end' ? x : anchor === 'start' ? x + w : x + w / 2 };
      });
      // the first and last keep their figures; one between them keeps its own only where it touches neither
      var keep = [boxes[0]].concat(boxes.length > 1 ? [boxes[boxes.length - 1]] : []);
      boxes.slice(1, -1).forEach(function (b) { if (!keep.some(function (k) { return b.l < k.r + 8 && k.l < b.r + 8; })) keep.push(b); });
      boxes.forEach(function (b) { c.line(b.x, bot + 1, b.x, bot + 5, { stroke: 'baseline', width: c.t('line-hairline'), mark: false }); });
      keep.forEach(function (b) { c.text(b.x, ay, b.s, { role: 'tick', anchor: b.anchor }); });
      var hgt = ay + 4;
      if (L.x_title) { var xb = c.text(x1, ay + c.size('tick') + 8, L.x_title, { role: 'tick', weight: 600, anchor: 'end', max: x1 - x0 }); hgt = xb.bottom + 2; }
      // earnings alone, a thin diagonal
      if (L.ref) {
        c.line(xs(xlo), ys(xlo), xs(xhi), ys(xhi), { stroke: 'context', width: c.t('line-context'), dash: '4 3', mark: false });
        // its words sit above the diagonal's upper end, on the side the other line never reaches
        var rx = xs(xlo + (xhi - xlo) * 0.9), ry = ys(xlo + (xhi - xlo) * 0.9);
        if (!c.phone) c.text(rx - 8, ry - 8, L.ref, { role: 'label', fill: 'secondary', halo: true, anchor: 'end' });
      }
      // the resources line
      var dpath = rows.map(function (r, k) { return (k ? 'L' : 'M') + K.round(xs(r[ex])) + ',' + K.round(ys(r[ey])); }).join('');
      c.path(dpath, { stroke: 'surface', width: c.t('line-subject') + 2 * c.t('keyline'), mark: false });
      c.path(dpath, { stroke: 'subject', width: c.t('line-subject'), data: { field: ey } }, [x0, top, x1 - x0, plotH]);
      rows.forEach(function (r) { c.datum(xs(r[ex]), ys(r[ey]), { data: { key: r[ex], field: ey, value: r[ey] } }); });
      // the line's words high in the empty upper left, with a leader down to the line
      if (L.line) {
        var lr = rows[Math.max(1, Math.floor(n * 0.12))], py = ys(lr[ey]);
                if (!c.phone) P.note(c, xs(lr[ex]), py, L.line, { place: 'above', anchor: 'start', dx: -(xs(lr[ex]) - x0) + 4, dy: -(py - ys(vs.hi * 0.8)) + 20, max: Math.min(220, (x1 - x0) * 0.5), weight: 700 });
      }
      // the drop and the climb back, in words
      if (ci > 0 && L.cliff) {
        var a = rows[ci - 1];
        c.circle(xs(a[ex]), ys(a[ey]), c.t('dot-vertex-radius'), { fill: 'subject', mark: false });
        c.circle(xs(rows[ci][ex]), ys(rows[ci][ey]), c.t('dot-vertex-radius'), { fill: 'subject', mark: false });
        P.note(c, xs(a[ex]), ys(a[ey]), fill(L.cliff), { place: 'above', anchor: 'end', dx: 4, dy: c.phone ? -(ys(a[ey]) - top) + 36 : 0, max: Math.min(250, W * 0.45), weight: 600 });
      }
      if (ci > 0 && L.band) {
        var bx = xs(rows[ci][ex]) + 8, bw = (back ? xs(back[ex]) : x1) - bx - 6;
        c.text(bx, ys(rows[ci][ey]) + c.size('label') + 26, fill(L.band), { role: 'label', max: Math.max(90, bw), halo: true });
      }
      c.height(hgt);
    }
  });
})(globalThis.OAChart);
