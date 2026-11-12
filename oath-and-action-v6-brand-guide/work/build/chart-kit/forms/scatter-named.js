/* Scatter plot with named points (coverage plan 3.6, core; S54), and the bubble chart's drawing (S55, through
 * forms/bubble-scatter.js, which sizes each point by a third measure). Two measures across places, one dot a place; the
 * dots the title names take the subject ink (or the red point) and carry their names, every other dot the light fill,
 * and a few more may carry their names in the light fill (labels.labeled). Names are placed by the kit's shared part
 * (K.parts.place_labels): eight places around each dot, then further out with a leader, clear of every name, text and
 * dot; a name with no clear place is listed in a line under the chart. A reference point (labels.reference, such as the
 * nation) takes the kit's open ring in the text's ink (K.parts.total_ring) with its name. Axis words sit over the value
 * axis at the left and at the right end under the bottom axis. No fitted line: the reader judges the pattern, and the
 * evidence label says what it can show.
 * encode: key (code), label (text), x (number), y (number), size (number, optional: a third measure as each circle's
 * area, largest drawn first, each with an outline of the ground).
 * labels: named (keys in the subject ink, each named), point (the one key in the red point, named), labeled (keys named
 * in the light fill), names ({key: printed name}), reference (a key drawn as an open ring and named), reference_label (its
 * words, with any column in braces), x_axis, y_axis (axis words), size_key ([values] for a key of circle sizes),
 * size_key_label (each one's words, with {value}), size_key_title (words over that key).
 * formats: x, y (ticks), size (the key). scale: x and y ([lo, hi]). On a phone the same arrangement draws narrower, with
 * smaller dots and circles. Maker B, round 2. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'scatter-named',
    name: 'Scatter Named',
    family: 'correlation',
    encode: { key: 'code', label: 'text', x: 'number', y: 'number', size: 'number?' },
    labels: ['named', 'point', 'labeled', 'names', 'reference', 'reference_label', 'x_axis', 'y_axis', 'size_key', 'size_key_label', 'size_key_title'],
    phone: 'same',
    draw: function (c) {
      var P = K.parts, L = c.labels, f = c.spec.formats || {}, W = c.width, ph = c.phone;
      var ek = c.field('key'), el = c.field('label'), ex = c.field('x'), ey = c.field('y'), ez = c.field('size', false);
      var names = L.names || {}, tick = c.size('tick'), size = c.size('label');
      var fx = f.x || 'integer', fy = f.y || 'integer';
      var ref = L.reference === undefined || L.reference === null ? null : String(L.reference);
      var refrow = ref === null ? null : c.rows.filter(function (r) { return String(r[ek]) === ref; })[0] || null;
      if (ref !== null && !refrow) c.warn('labels.reference names no row: ' + ref);
      var rows = c.rows.filter(function (r) { return r !== refrow; });
      var ink = P.named_fill(c, L.named, ek, 'subject', L.point);
      var lit = function (r) { return ink.named && ink.is_named(r) || ink.is_point(r); };
      var name = function (r) { var k = String(r[ek]); return names[k] !== undefined ? names[k] : String(r[el]); };
      // the scales: the spec's own, or nice ones from the data
      var xv = c.rows.map(function (r) { return r[ex]; }), yv = c.rows.map(function (r) { return r[ey]; });
      var sc = c.spec.scale || {}, nt = W < 300 ? 3 : ph ? 4 : 6;
      var dx = sc.x || K.nice(Math.min.apply(null, xv), Math.max.apply(null, xv), nt), dy = sc.y || K.nice(Math.min.apply(null, yv), Math.max.apply(null, yv), ph ? 4 : 5);
      var tx = K.ticks(dx[0], dx[1], 0, K.nice(dx[0], dx[1], nt).step), ty = K.ticks(dy[0], dy[1], 0, K.nice(dy[0], dy[1], ph ? 4 : 5).step);
      var y0 = 0;
      // the circles' sizes, by area, and their key over the plot
      var zmax = ez ? Math.max.apply(null, rows.map(function (r) { return r[ez]; })) : 0;   // the reference row (the nation) is no circle
      var rmax = ez ? c.t(W < 300 ? 'bubble-radius-max-small-phone' : ph ? 'bubble-radius-max-phone' : 'bubble-radius-max-mid') : 0;
      var area = ez ? K.scale.sqrt(zmax, rmax) : null, rdot = c.t(ph ? 'dot-open-radius' : 'dot-subject-radius');
      var rad = function (r) { return ez ? area(r[ez]) : rdot; };
      // the key of circle sizes: its title, then each circle with its words, in one row that wraps
      if (ez && L.size_key && L.size_key.length) {
        var kx = 0, kr = L.size_key.map(function (v) { return area(v); }), kh = 2 * Math.max.apply(null, kr), krow = y0;
        if (L.size_key_title) { var kt = c.text(0, y0 + tick, L.size_key_title, { role: 'tick', weight: 600, max: W }); krow = kt.bottom + 6; }
        L.size_key.forEach(function (v, i) {
          var words = String(L.size_key_label || '{value}').replace('{value}', K.fmt(v, f.size || 'integer')), ww = 2 * kr[i] + 6 + c.measure(words, 'tick');
          if (kx > 0 && kx + ww > W) { kx = 0; krow += kh + 8; }
          c.circle(kx + kr[i], krow + kh - kr[i], kr[i], { stroke: 'context', width: c.t('bubble-outline'), mark: false });
          c.text(kx + 2 * kr[i] + 6, krow + kh - kr[i] + tick * 0.35, words, { role: 'tick' });
          kx += ww + 18;
        });
        y0 = krow + kh + 14;
      }
      if (L.y_axis) { c.text(0, y0 + tick, L.y_axis, { role: 'tick', weight: 600, max: W }); y0 += tick + 10; }
      var gut = P.value_gutter(c, ty, fy), x0 = gut + 8, x1 = W - 6;
      var top = y0 + tick * 0.5, plotH = ph ? Math.round((x1 - x0) * 0.95) : 420, bot = top + plotH;
      var pad = ez ? 0 : rdot + 2;
      var xs = K.scale.linear([dx[0], dx[1]], [x0 + pad, x1 - pad]), ys = K.scale.linear([dy[0], dy[1]], [bot - pad, top + pad]);
      // gridlines both ways, values at the left and along the bottom
      ty.forEach(function (v) { c.line(x0, ys(v), x1, ys(v), { stroke: 'gridline', width: c.t('line-hairline'), mark: false }); c.text(gut, ys(v) + tick * 0.35, K.fmt(v, fy), { role: 'tick', anchor: 'end', tnum: true }); });
      tx.forEach(function (v) { c.line(xs(v), top, xs(v), bot, { stroke: 'gridline', width: c.t('line-hairline'), mark: false }); });
      c.line(x0, bot, x1, bot, { stroke: 'baseline', width: c.t('line-hairline'), mark: false });
      var ay = bot + tick + 8;
      // the bottom ticks' values, every other one dropped until they sit apart
      var tb2 = tx.map(function (v) { var w = K.fmt(v, fx), tw = c.measure(w, 'tick'), x = xs(v), an = x + tw / 2 > W ? 'end' : 'middle'; return { v: v, w: w, x: x, an: an, l: an === 'end' ? W - tw : x - tw / 2, r: an === 'end' ? W : x + tw / 2 }; });
      var keepx = tb2;
      for (var kk = 1; kk <= tb2.length; kk++) {
        keepx = tb2.filter(function (b, i) { return (tb2.length - 1 - i) % kk === 0; });
        if (keepx.every(function (b, j) { return !j || keepx[j - 1].r + 10 <= b.l; })) break;
      }
      tx.forEach(function (v) { c.line(xs(v), bot, xs(v), bot + 4, { stroke: 'baseline', width: c.t('line-hairline'), mark: false }); });
      keepx.forEach(function (b) { c.text(b.an === 'end' ? W : b.x, ay, b.w, { role: 'tick', anchor: b.an }); });
      // the dots: the light fill first, largest first, then the named ones, so a name's dot sits on top
      var pts = rows.map(function (r) { return { r: r, x: xs(r[ex]), y: ys(r[ey]), rad: rad(r) }; });
      var draw_order = pts.slice().sort(function (a, b) { return (lit(a.r) ? 1 : 0) - (lit(b.r) ? 1 : 0) || b.rad - a.rad; });
      draw_order.forEach(function (p) {
        var role = ink(p.r), o = { fill: role, data: { key: p.r[ek], field: ey, value: p.r[ey], x: p.r[ex] } };
        if (ez) o.area_of = { value: p.r[ez], max_value: zmax, max_radius: rmax };
        c.circle(p.x, p.y, p.rad, Object.assign(o, ink.keyline(p.r)));
        // dots keep an outline of the ground so overlapping ones stay apart; circles sized by a measure take a 1 px outline
        // in the context ink, so overlaps read (the data lead's ruling (e))
        if (ez) c.circle(p.x, p.y, p.rad, { stroke: lit(p.r) ? 'surface' : 'context', width: c.t('bubble-outline'), mark: false });
        else if (!lit(p.r)) c.circle(p.x, p.y, p.rad, { stroke: 'surface', width: c.t('bubble-outline'), mark: false });
        c.datum(p.x, p.y, { data: { key: p.r[ek], field: ex, value: p.r[ex] } });
      });
      // the nation as an open ring in the text's ink (the data lead's ruling (b))
      if (refrow) {
        var rx = xs(refrow[ex]), ry = ys(refrow[ey]);
        P.total_ring(c, rx, ry, rdot + 1, { data: { key: refrow[ek], field: ey, value: refrow[ey], x: refrow[ex] } });
        pts.push({ r: refrow, x: rx, y: ry, rad: rdot + 2, ref: true });
      }
      // the names, through the kit's shared placing (R2-C2): the named points first, then the points labeled in the light
      // fill, then the reference; every dot drawn is a box no name may cover. A name with no clear place is named in a
      // line under the chart, and the table names every point
      var labeled = [].concat(L.labeled || []).map(String);
      var order = function (p) { return p.ref ? 2 : lit(p.r) ? 0 : 1; };
      var lab = pts.filter(function (p) { return p.ref ? !!L.reference_label : lit(p.r) || labeled.indexOf(String(p.r[ek])) >= 0; })
        .sort(function (a, b) { return order(a) - order(b) || a.x - b.x; });
      var avoid = pts.filter(function (p) { return lab.indexOf(p) < 0; }).map(function (p) { return { x: p.x - p.rad, y: p.y - p.rad, w: 2 * p.rad, h: 2 * p.rad }; });
      var pl = P.place_labels(c, lab.map(function (p) {
        return { x: p.x, y: p.y, r: p.rad, words: p.ref ? P.fill(c, L.reference_label, p.r) : name(p.r), weight: lit(p.r) && !p.ref ? 700 : p.ref ? 400 : 600, key: p.r[ek] };
      }), { top: 0, bottom: bot, avoid: avoid });
      var end = ay + 4;
      if (L.x_axis) { var xb = c.text(W, ay + tick + 10, L.x_axis, { role: 'tick', weight: 600, anchor: 'end', max: W - x0 }); end = xb.bottom; }
      if (pl.unplaced.length) {
        var ub = c.text(0, end + c.size('note') + 8, K.word('unlabeled_marks').replace('{codes}', pl.unplaced.map(function (it) { return it.words; }).join(', ')), { role: 'note', max: W, fill: 'secondary' });
        end = ub.bottom;
      }
      c.height(end + 2);
    }
  });
})(globalThis.OAChart);
