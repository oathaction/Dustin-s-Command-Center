/* Scatter plot with named points (coverage plan 3.6, core; S54), and the bubble chart's drawing (S55, through
 * forms/bubble-scatter.js, which sizes each point by a third measure). Two measures across places, one dot a place; a
 * few dots the spec names take the subject ink (or the red point) and carry their names, every other dot the light fill.
 * Names are placed by trying the eight spots around their dot in a fixed order and keeping the first that touches no
 * other name, no dot and no edge, then the same spots further out with a leader; so the placing is the same in Node and
 * every browser. A reference point (labels.reference, such as the nation) takes an open ring in the text's ink with its
 * name. Axis words sit over the value axis at the left and under the time-free axis at the bottom. No fitted line: the
 * reader judges the pattern, and the evidence label says what it can show.
 * encode: key (code), label (text), x (number), y (number), size (number, optional: a third measure as each circle's
 * area, largest drawn first).
 * labels: named (keys in the subject ink, each named), point (the one key in the red point, named), names ({key: printed
 * name}), reference (a key drawn as an open ring and named), reference_label (its words, with {label}, {x} and {y}),
 * place ({key: "right", "left", "above", "below"}: the spot to try first), x_axis, y_axis (axis words), size_key ([values]
 * for a key of circle sizes; words from size_key_label with {value}), size_key_title (words over that key).
 * formats: x, y (ticks and words), size. scale: x and y ([lo, hi]). On a phone the same arrangement draws narrower, with
 * smaller dots and circles. Maker B, round 2. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'scatter-named',
    name: 'Scatter Named',
    family: 'correlation',
    encode: { key: 'code', label: 'text', x: 'number', y: 'number', size: 'number?' },
    labels: ['named', 'point', 'names', 'reference', 'reference_label', 'place', 'x_axis', 'y_axis', 'size_key', 'size_key_label', 'size_key_title'],
    phone: 'same',
    draw: function (c) {
      var P = K.parts, L = c.labels, f = c.spec.formats || {}, W = c.width, ph = c.phone;
      var ek = c.field('key'), el = c.field('label'), ex = c.field('x'), ey = c.field('y'), ez = c.field('size', false);
      var names = L.names || {}, place = L.place || {}, tick = c.size('tick'), size = c.size('label');
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
        // circles keep an outline of the ground, so overlapping ones stay apart
        if (ez || !lit(p.r)) c.circle(p.x, p.y, p.rad, { stroke: 'surface', width: c.t('bubble-outline'), mark: false });
        c.datum(p.x, p.y, { data: { key: p.r[ek], field: ex, value: p.r[ex] } });
      });
      if (refrow) {
        var rx = xs(refrow[ex]), ry = ys(refrow[ey]);
        c.circle(rx, ry, rdot + 1, { stroke: 'surface', width: c.t('line-context') + 2, mark: false });
        c.circle(rx, ry, rdot + 1, { stroke: 'label', width: c.t('line-context'), data: { key: refrow[ek], field: ey, value: refrow[ey], x: refrow[ex] } });
        pts.push({ r: refrow, x: rx, y: ry, rad: rdot + 2, ref: true });
      }
      // the names: the eight spots around a dot, then further out with a leader
      var boxes = [], leads = [], asc = size * 0.75, desc = size * 0.25;
      var others = c.texts.slice();   // the axis words and values drawn so far
      var hits = function (b, self) {
        if (b.x < 0 || b.x + b.w > W || b.y < 0 || b.y + b.h > bot) return true;
        if (boxes.concat(others).some(function (o) { return b.x < o.x + o.w + 3 && o.x < b.x + b.w + 3 && b.y < o.y + o.h + 2 && o.y < b.y + b.h + 2; })) return true;
        return pts.some(function (p) {
          if (p === self) return false;
          var nx = Math.max(b.x, Math.min(p.x, b.x + b.w)), ny = Math.max(b.y, Math.min(p.y, b.y + b.h));
          return Math.pow(nx - p.x, 2) + Math.pow(ny - p.y, 2) < Math.pow(p.rad + 1.5, 2);
        });
      };
      var spots = ['right', 'left', 'above', 'below', 'above-right', 'above-left', 'below-right', 'below-left'];
      var lab = pts.filter(function (p) { return p.ref ? !!L.reference_label : lit(p.r); });
      lab.sort(function (a, b) { return a.x - b.x; });
      lab.forEach(function (p) {
        var words = p.ref ? P.fill(c, L.reference_label, p.r) : name(p.r), w = c.measure(words, 'label', p.ref ? 600 : 700), h = asc + desc;
        var first = place[String(p.r[ek])], order = first ? [first].concat(spots.filter(function (s) { return s !== first; })) : spots;
        var at = function (s, d) {
          var gx = p.rad + d, gy = p.rad + d;
          var bx = s.indexOf('right') >= 0 ? p.x + gx : s.indexOf('left') >= 0 ? p.x - gx - w : p.x - w / 2;
          var by = s.indexOf('above') === 0 ? p.y - gy - h : s.indexOf('below') === 0 ? p.y + gy : p.y - h / 2;
          if (s === 'above-right' || s === 'above-left' || s === 'below-right' || s === 'below-left') { bx = s.slice(-5) === 'right' ? p.x + p.rad * 0.6 : p.x - p.rad * 0.6 - w; }
          return { x: bx, y: by, w: w, h: h };
        };
        // a spot further out takes a leader from the dot's edge to the name's nearest point, which may cross no name
        var leader_of = function (b) {
          var lx = Math.max(b.x, Math.min(p.x, b.x + b.w)), ly2 = Math.max(b.y, Math.min(p.y, b.y + b.h));
          var dd = Math.sqrt(Math.pow(lx - p.x, 2) + Math.pow(ly2 - p.y, 2)) || 1;
          return [p.x + (lx - p.x) * (p.rad + 1) / dd, p.y + (ly2 - p.y) * (p.rad + 1) / dd, lx, ly2];
        };
        var clear = function (b, far) {
          if (hits(b, p)) return false;
          if (leads.some(function (s2) { return K.seg_hits_box(s2[0], s2[1], s2[2], s2[3], b.x - 1, b.y - 1, b.x + b.w + 1, b.y + b.h + 1); })) return false;
          if (!far) return true;
          var s1 = leader_of(b);
          return !boxes.concat(others).some(function (o) { return K.seg_hits_box(s1[0], s1[1], s1[2], s1[3], o.x - 1, o.y - 1, o.x + o.w + 1, o.y + o.h + 1); });
        };
        var got = null, far = false;
        [3, 14, 28, 44, 62, 84, 110, 140].some(function (d, j) { return order.some(function (s) { var b = at(s, d); if (clear(b, j > 0)) { got = b; far = j > 0; return true; } return false; }); });
        if (!got) { got = at(order[0], 3); c.warn('a name could not be placed clear of the dots: ' + words); }
        boxes.push(got);
        if (far) {
          var sg = leader_of(got);
          leads.push(sg);
          c.line(sg[0], sg[1], sg[2], sg[3], { stroke: 'leader', width: c.t('line-hairline'), mark: false });
        }
        c.text(got.x, got.y + asc, words, { role: 'label', weight: p.ref ? 600 : 700, halo: true });
      });
      var end = ay + 4;
      if (L.x_axis) { var xb = c.text(W, ay + tick + 10, L.x_axis, { role: 'tick', weight: 600, anchor: 'end', max: W - x0 }); end = xb.bottom; }
      c.height(end + 2);
    }
  });
})(globalThis.OAChart);
