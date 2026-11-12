/* Scatter plot with named points (coverage plan 3.6, core; S54), and the bubble chart's drawing (S55, through
 * forms/bubble-scatter.js, which sizes each point by a third measure). Two measures across places, one dot a place; the
 * dots the title names take the subject ink (or the red point) and carry their names in bold, every other dot the light
 * fill, and a few more may carry their names in regular weight in the light fill (labels.labeled). Names are placed by the kit's shared part
 * (K.parts.place_labels): eight places around each dot, then further out with a leader, clear of every name, text and
 * dot and circle; a name with no clear place is listed in a line under the chart. A reference point (labels.reference, such as the
 * nation) takes the kit's open ring in the text's ink (K.parts.total_ring) with its name. Axis words sit over the value
 * axis at the left and at the right end under the bottom axis. No fitted line: the reader judges the pattern, and the
 * evidence label says what it can show.
 * encode: key (code), label (text), x (number), y (number), size (number, optional: a third measure as each circle's
 * area, largest drawn first, each with an outline of the ground).
 * labels: named (keys in the subject ink, each named), point (the one key in the red point, named), labeled (keys named
 * in the light fill), names ({key: printed name}), reference (a key drawn as an open ring and named), reference_label (its
 * words, with any column in braces), x_axis, y_axis (axis words), size_key ([values] for a key of circle sizes),
 * size_key_label (each one's words, with {value}), size_key_title (words over that key), sub ({key: words}: a second
 * line in regular weight under a named point's bold name, or over it, such as the figure the title gives; round 2 fix
 * pass, BC S9); sub_short ({key: words}: the shorter line where the first finds no place); sub_under (a sentence with
 * {name} and {sub} under the chart for a figure that finds no place beside its mark, on two lines or on one). The key's circles take the field's fill and outline, as the circles they stand for (BC S17); the
 * reference's name keeps off every circle where it can (BC S9).
 * formats: x, y (ticks), size (the key). scale: x and y ([lo, hi]). On a phone the same arrangement draws narrower, with
 * smaller dots and circles. Maker B, round 2. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'scatter-named',
    name: 'Scatter Named',
    family: 'correlation',
    encode: { key: 'code', label: 'text', x: 'number', y: 'number', size: 'number?' },
    labels: ['named', 'point', 'labeled', 'names', 'reference', 'reference_label', 'x_axis', 'y_axis', 'size_key', 'size_key_label', 'size_key_title', 'sub', 'sub_short', 'sub_under'],
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
          c.circle(kx + kr[i], krow + kh - kr[i], kr[i], { fill: c.ground === 'charcoal' ? 'context' : 'light-fill', mark: false });
          c.circle(kx + kr[i], krow + kh - kr[i], kr[i], { stroke: c.ground === 'charcoal' ? 'surface' : 'context', width: c.t('bubble-outline'), mark: false });
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
        // on Charcoal the field's fill is the context ink itself, so its outline takes the ground's color there (MB-11)
        if (ez) c.circle(p.x, p.y, p.rad, { stroke: lit(p.r) || c.ground === 'charcoal' ? 'surface' : 'context', width: c.t('bubble-outline'), mark: false });
        else if (!lit(p.r)) c.circle(p.x, p.y, p.rad, { stroke: 'surface', width: c.t('bubble-outline'), mark: false });
        c.datum(p.x, p.y, { data: { key: p.r[ek], field: ex, value: p.r[ex] } });
      });
      // the nation as an open ring in the text's ink (the data lead's ruling (b))
      if (refrow) {
        var rx = xs(refrow[ex]), ry = ys(refrow[ey]);
        // a 2 px halo of the ground outside the ring, so it reads as its own mark on a dark circle under it (the data lead's
        // MB-F1; the brand reviewer's second-pass N2 found 1 px read as a hole in that circle)
        c.circle(rx, ry, rdot + 1 + c.t('line-context') / 2 + 2, { fill: 'surface', mark: false });
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
      var item = function (p) { return { x: p.x, y: p.y, r: p.rad, words: p.ref ? P.fill(c, L.reference_label, p.r) : name(p.r), weight: lit(p.r) && !p.ref ? 700 : 400, key: p.r[ek] }; };
      var reach = W < 330 ? [14, 30, 48] : [14, 30, 48, 70, 96];   // a narrow column keeps the other names' leaders short
      var reach2 = [14, 30, 48, 70, 96, 124];   // a named point's block may reach further, so the title's marks keep their names
      // every dot and circle, for the tests below: a box meets a circle where its nearest point lies inside the circle
      var circ = pts.map(function (p) { return { x: p.x, y: p.y, r: p.rad, p: p }; });
      var meets = function (b, q, pad) { var nx = Math.max(b.x, Math.min(q.x, b.x + b.w)), ny = Math.max(b.y, Math.min(q.y, b.y + b.h)); return Math.pow(nx - q.x, 2) + Math.pow(ny - q.y, 2) < Math.pow(q.r + pad, 2); };
      // a named point with a second line (labels.sub, BC S9 and RF-18): its bold name and the regular line under it set as one
      // block, beside its circle or further out on a leader, clear of every word, dot and circle (round 2 fix pass)
      var subs = L.sub || {}, lh = Math.round(size * 1.2), unplaced2 = [];
      // a block on two lines (the bold name over its figure), or on one where two find no place: the name and its figure
      // side by side (the statistics reviewer's second-pass N2: New York lost its figure at every phone width)
      var plan2 = function (p, sb, taken, one) {
        var nm = name(p.r), wn = c.measure(nm, 'label', 700), w = one ? wn + 5 + c.measure(sb, 'label', 400) : Math.max(wn, c.measure(sb, 'label', 400)), h = one ? size : size + lh;
        var dirs = [[1, 0], [-1, 0], [0, -1], [0, 1], [0.75, -0.75], [0.75, 0.75], [-0.75, -0.75], [-0.75, 0.75]];
        var near = function (bx2) { return function (t) { return bx2.x < t.x + t.w + 3 && t.x < bx2.x + bx2.w + 3 && bx2.y < t.y + t.h + 2 && t.y < bx2.y + bx2.h + 2; }; };
        for (var ri = 0; ri < reach2.length + 1; ri++) {
          var d = p.rad + 4 + (ri ? reach2[ri - 1] : 0);
          for (var k = 0; k < dirs.length; k++) {
            var ax = dirs[k][0], ay2 = dirs[k][1], an = ax > 0 ? 'start' : ax < 0 ? 'end' : 'middle';
            var x = p.x + ax * d, t0 = ay2 < 0 ? p.y + ay2 * d - h : ay2 > 0 ? p.y + ay2 * d : p.y - h / 2;
            var bx = an === 'start' ? x : an === 'end' ? x - w : x - w / 2, box = { x: bx, y: t0, w: w, h: h };
            if (box.x < 0 || box.x + box.w > W || box.y < 0 || box.y + box.h > bot) continue;
            if (c.texts.some(near(box)) || taken.some(function (t) { return near(box)(t.box); })) continue;
            if (circ.some(function (q) { return meets(box, q, 2); })) continue;
            var L0 = null;
            if (ri) {
              var lx = Math.max(box.x, Math.min(p.x, box.x + box.w)), ly = Math.max(box.y, Math.min(p.y, box.y + box.h));
              var vx = lx - p.x, vy = ly - p.y, len = Math.sqrt(vx * vx + vy * vy) || 1;
              L0 = [p.x + vx / len * (p.rad + 1), p.y + vy / len * (p.rad + 1), lx - vx / len * 2, ly - vy / len * 2];
              var segbox = function (t) { return K.seg_hits_box(L0[0], L0[1], L0[2], L0[3], t.x - 1, t.y - 1, t.x + t.w + 1, t.y + t.h + 1); };
              if (c.texts.some(segbox) || taken.some(function (t) { return segbox(t.box); })) continue;
              if (circ.some(function (q) { return q.p !== p && K.seg_hits_box(L0[0], L0[1], L0[2], L0[3], q.x - q.r, q.y - q.r, q.x + q.r, q.y + q.r); })) continue;
            }
            if (taken.some(function (t) { return t.L && K.seg_hits_box(t.L[0], t.L[1], t.L[2], t.L[3], box.x - 1, box.y - 1, box.x + box.w + 1, box.y + box.h + 1); })) continue;
            return { p: p, nm: nm, sb: sb, an: an, tx: an === 'start' ? bx : an === 'end' ? bx + w : bx + w / 2, t0: t0, L: L0, box: box, one: !!one, wn: wn };
          }
        }
        return null;
      };
      var withsub = lab.filter(function (p) { return !p.ref && subs[String(p.r[ek])] !== undefined; });
      var subs_short = L.sub_short || {};
      // the blocks claim room in the order that places the most of them (a few named points, so every order is tried)
      var perms = function (xs) { return xs.length < 2 ? [xs] : xs.reduce(function (acc, x, i) { return acc.concat(perms(xs.slice(0, i).concat(xs.slice(i + 1))).map(function (pp) { return [x].concat(pp); })); }, []); };
      var tryorder = function (ord) {
        var taken = [];
        ord.forEach(function (p) {
          var k = String(p.r[ek]), sh = subs_short[k];
          var pl2 = plan2(p, subs[k], taken) || (sh ? plan2(p, sh, taken) : null) || plan2(p, subs[k], taken, true) || (sh ? plan2(p, sh, taken, true) : null);
          if (pl2) taken.push(pl2);
        });
        return taken;
      };
      var best = [];
      (withsub.length <= 5 ? perms(withsub) : [withsub]).some(function (ord) { var t = tryorder(ord); if (t.length > best.length) best = t; return best.length === withsub.length; });
      best.forEach(function (q) {
        if (q.one) {
          c.text(q.box.x, q.t0 + 0.864 * size, q.nm, { role: 'label', weight: 700, halo: true });
          c.text(q.box.x + q.wn + 5, q.t0 + 0.864 * size, q.sb, { role: 'label', weight: 400, halo: true });
        } else {
          c.text(q.tx, q.t0 + 0.864 * size, q.nm, { role: 'label', weight: 700, anchor: q.an, halo: true });
          c.text(q.tx, q.t0 + 0.864 * size + lh, q.sb, { role: 'label', weight: 400, anchor: q.an, halo: true });
        }
        if (q.L) c.line(q.L[0], q.L[1], q.L[2], q.L[3], { stroke: 'leader', width: c.t('line-hairline'), mark: false });
      });
      withsub.forEach(function (p) { if (!best.some(function (q) { return q.p === p; })) unplaced2.push(p); });
      // the other names through the kit's shared placing, the reference last, each clear of every dot and circle; a named
      // point whose block found no place takes its name alone here
      var rest = lab.filter(function (p) { return withsub.indexOf(p) < 0 || unplaced2.indexOf(p) >= 0; });
      var boxes = function (skip) { return pts.filter(function (p) { return skip.indexOf(p) < 0; }).map(function (p) { return { x: p.x - p.rad, y: p.y - p.rad, w: 2 * p.rad, h: 2 * p.rad }; }); };
      var pl = { placed: [], unplaced: [] };
      rest.forEach(function (p) {
        var r1 = P.place_labels(c, [item(p)], { top: 0, bottom: bot, avoid: boxes([p]), reach: !p.ref && lit(p.r) ? reach2 : reach });
        pl.placed = pl.placed.concat(r1.placed); pl.unplaced = pl.unplaced.concat(r1.unplaced);
      });
      var end = ay + 4;
      if (L.x_axis) { var xb = c.text(W, ay + tick + 10, L.x_axis, { role: 'tick', weight: 600, anchor: 'end', max: W - x0 }); end = xb.bottom; }
      if (pl.unplaced.length) {
        var ub = c.text(0, end + c.size('note') + 8, K.word('unlabeled_marks').replace('{codes}', pl.unplaced.map(function (it) { return it.words; }).join(', ')), { role: 'note', max: W, fill: 'secondary' });
        end = ub.bottom;
      }
      // a named point whose figure found no place beside it carries the figure in a line under the chart (labels.sub_under,
      // with {name} and {sub}), so the drawing gives every figure its chart note promises
      if (L.sub_under && unplaced2.length) {
        var sw2 = unplaced2.map(function (p) { return String(L.sub_under).replace('{name}', name(p.r)).replace('{sub}', subs[String(p.r[ek])]); }).join(' ');
        var sb2 = c.text(0, end + c.size('note') + 8, sw2, { role: 'note', max: W, fill: 'secondary' });
        end = sb2.bottom;
      }
      c.height(end + 2);
    }
  });
})(globalThis.OAChart);
