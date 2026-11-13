/* Venn diagram (coverage plan 3.8, extended; S87). Two groups that overlap, as two equal circles inside a frame for everyone,
 * so four regions: the first group alone, both, the second alone, and neither (the frame outside both circles). Each region
 * prints its name and count inside it. The circles are one size whatever the counts, and the spec's note says so; the
 * Euler diagram draws the same regions at true area (Rule 14.82).
 * encode: region (text), value (number).
 * labels: regions ({a, ab, b, none}: the region each row is, by its stored name), names ({stored: printed}), sets ([the
 * first circle's name, the second's]), frame (the frame's name, {total} the sum of every row), fills ({a, ab, b, none}: color
 * roles, none by default), named ([regions] set in 700), edge (the circles' ink, default subject). formats: value. */
(function (K) {
  'use strict';
  var ON = { subject: 'label-on-subject', point: 'label-on-subject', 'cat-1': 'on-cat-1', 'cat-2': 'on-cat-2', 'cat-3': 'on-cat-3' };
  // a circular arc as points, for the checks: from angle a0 to a1 (radians, y down), n steps
  var arc_pts = function (cx, cy, r, a0, a1, n) { var p = []; for (var i = 0; i <= n; i++) { var t = a0 + (a1 - a0) * i / n; p.push([cx + r * Math.cos(t), cy + r * Math.sin(t)]); } return p; };
  var R1 = function (v) { return Math.round(v * 10) / 10; };
  K.register_chart({
    form: 'venn-diagram', name: 'Venn Diagram', family: 'proportion-and-overlap',
    encode: { region: 'text', value: 'number' },
    labels: ['regions', 'names', 'sets', 'frame', 'fills', 'named', 'edge'],
    phone: 'same',
    draw: function (c) {
      var L = c.labels, W = c.width, er = c.field('region'), ev = c.field('value'), f = c.spec.formats || {};
      var RG = L.regions || {}, FI = L.fills || {}, rows = c.all_rows || c.rows, by = {};
      ['a', 'ab', 'b', 'none'].forEach(function (k) { by[k] = rows.filter(function (r) { return r[er] === RG[k]; })[0]; if (!by[k]) c.warn('labels.regions.' + k + ' names no row'); });
      if (!by.a || !by.ab || !by.b || !by.none) { c.height(10); return; }
      var nm = function (r) { return (L.names || {})[r[er]] || r[er]; }, fv = function (v) { return K.fmt(v, f.value || 'integer'); };
      var named = function (r) { return (L.named || []).indexOf(r[er]) >= 0; };
      var tot = rows.reduce(function (t, r) { return t + (+r[ev] || 0); }, 0);
      var tick = c.size('tick'), lab = c.size('label'), pad = c.phone ? 10 : 16, y = 0;
      // the frame's name, then the two circles' names, then the circles
      var fr = String(L.frame || '').split('{total}').join(fv(tot));
      var ft = fr ? c.text(pad, pad + tick * 0.86, fr, { role: 'tick', weight: 600, max: W - 2 * pad }) : null;
      var inner = W - 2 * pad, r = Math.min(c.phone ? 92 : 118, Math.floor(inner / 3.1)), d = 1.1 * r;
      var cx1 = W / 2 - d / 2, cx2 = W / 2 + d / 2;
      var sets = L.sets || ['', ''], nmax = Math.max(80, (2 * r + d) / 2 - 6);
      var sy = (ft ? ft.bottom : pad) + 12 + lab * 0.86;
      var s1 = c.text(cx1 - r, sy, sets[0], { role: 'label', weight: 600, max: nmax });
      var s2 = c.text(cx2 + r, sy, sets[1], { role: 'label', weight: 600, anchor: 'end', max: nmax });
      var cy = Math.max(s1.bottom, s2.bottom) + 8 + r;
      // the circles meet at two points on the line between their centers' halves
      var a = d / 2, h = Math.sqrt(r * r - a * a), px = cx1 + a, pt = [px, cy - h], pb = [px, cy + h];
      var A = Math.atan2(-h, a), B = Math.atan2(-h, -a);   // angle of the top point from each center
      var M = 'M' + R1(pt[0]) + ',' + R1(pt[1]), Pb = R1(pb[0]) + ',' + R1(pb[1]), Pt = R1(pt[0]) + ',' + R1(pt[1]), rr = R1(r);
      var reg = {
        // the first circle less the overlap: its left arc, then the second circle's left arc back up
        a: { d: M + 'A' + rr + ',' + rr + ' 0 1 0 ' + Pb + 'A' + rr + ',' + rr + ' 0 0 1 ' + Pt + 'Z', p: arc_pts(cx1, cy, r, A, -A - 2 * Math.PI, 40).concat(arc_pts(cx2, cy, r, -B, 2 * Math.PI + B, 12)) },
        ab: { d: M + 'A' + rr + ',' + rr + ' 0 0 0 ' + Pb + 'A' + rr + ',' + rr + ' 0 0 0 ' + Pt + 'Z', p: arc_pts(cx2, cy, r, 2 * Math.PI + B, -B, 12).concat(arc_pts(cx1, cy, r, -A, A, 12)) },
        b: { d: M + 'A' + rr + ',' + rr + ' 0 1 1 ' + Pb + 'A' + rr + ',' + rr + ' 0 0 0 ' + Pt + 'Z', p: arc_pts(cx2, cy, r, B, -B, 40).concat(arc_pts(cx1, cy, r, -A, A, 12)) }
      };
      var top = cy - r, bot = cy + r;
      // the frame for everyone, its words in the corner that the circles leave
      var none = by.none, nw = [nm(none), fv(none[ev])], nwid = Math.max(c.measure(nw[0], 'label', named(none) ? 700 : 600), c.measure(nw[1], 'label', named(none) ? 700 : 400, true));
      var nh = lab * 1.25 + lab, corner_x = W - pad - nwid, corner_top = bot + pad - nh;
      // the corner's top left must sit outside the second circle, or the frame grows a band under the circles for it
      var ddx = Math.max(0, corner_x - cx2), ddy = Math.max(0, corner_top - cy), clear = ddx * ddx + ddy * ddy > (r + 6) * (r + 6) && corner_x > cx2;
      var fb = clear ? bot + pad : bot + 10 + nh + pad;
      c.rect(0.5, 0.5, W - 1, fb - 0.5, Object.assign({ fill: FI.none || 'none', kind: 'region', data: { key: none[er], field: ev, value: none[ev] } }, {}));
      c.rect(0.5, 0.5, W - 1, fb - 0.5, { stroke: 'context', width: 1, mark: false });
      // the circles' ground knocks the frame's fill out, then each region takes its own
      if (FI.none) { c.circle(cx1, cy, r, { fill: 'surface', mark: false }); c.circle(cx2, cy, r, { fill: 'surface', mark: false }); }
      ['a', 'ab', 'b'].forEach(function (k) {
        var row = by[k], g = reg[k], xs = g.p.map(function (q) { return q[0]; }), ys = g.p.map(function (q) { return q[1]; });
        var x0 = Math.min.apply(null, xs), y0 = Math.min.apply(null, ys);
        c.path(g.d, { fill: FI[k] || 'none', pts: [g.p], closed: true, kind: 'region', data: { key: row[er], field: ev, value: row[ev] } }, [x0, y0, Math.max.apply(null, xs) - x0, Math.max.apply(null, ys) - y0]);
      });
      var edge = L.edge || 'subject';
      c.circle(cx1, cy, r, { stroke: edge, width: c.t('line-baseline'), mark: false });
      c.circle(cx2, cy, r, { stroke: edge, width: c.t('line-baseline'), mark: false });
      // each region's words: its name and its count, on as few lines as fit inside it
      var words = function (k, x, mid, room) {
        var row = by[k], nmw = named(row) ? 700 : 600, vw = named(row) ? 700 : 400, ink = ON[FI[k]] || 'label';
        var roles = ['label', 'tick'];
        for (var i = 0; i < roles.length; i++) {
          var sz = c.size(roles[i]), lh = Math.round(sz * 1.25);
          var l1 = c.wrap(nm(row), roles[i], room(0), nmw), l2 = c.wrap(fv(row[ev]), roles[i], room(0), vw), n = l1.length + l2.length;
          var hh = sz + (n - 1) * lh, wide = 0;
          l1.forEach(function (s) { wide = Math.max(wide, c.measure(s, sz, nmw)); });
          l2.forEach(function (s) { wide = Math.max(wide, c.measure(s, sz, vw, true)); });
          if (wide > Math.min(room(-hh / 2), room(hh / 2)) || n > 4) continue;
          var t = c.text(x, mid - hh / 2 + sz * 0.86, nm(row), { role: roles[i], weight: nmw, anchor: 'middle', max: room(0) + 0.5, leading: lh, fill: ink });
          c.text(x, t.bottom + sz * 0.86 - sz * 0.241 + (lh - sz), fv(row[ev]), { role: roles[i], weight: vw, anchor: 'middle', max: room(0) + 0.5, leading: lh, tnum: true, fill: ink });
          return true;
        }
        c.warn('the words for ' + nm(row) + ' do not fit inside its region at ' + W + ' px');
        return false;
      };
      var half = function (dy) { return Math.sqrt(Math.max(0, r * r - dy * dy)); };
      words('a', cx1 - r + d / 2, cy, function () { return d - 10; });
      words('ab', px, cy, function (dy) { return 2 * half(dy) - d - 8; });
      words('b', cx2 + r - d / 2, cy, function () { return d - 10; });
      var nb = c.text(W - pad, fb - pad - lab * 1.25 - lab * 0.24 + 0, nw[0], { role: 'label', weight: named(none) ? 700 : 600, anchor: 'end', fill: ON[FI.none] || 'label' });
      c.text(W - pad, nb.bottom + lab * 0.86 - lab * 0.241 + lab * 0.25, nw[1], { role: 'label', weight: named(none) ? 700 : 400, anchor: 'end', tnum: true, fill: ON[FI.none] || 'label' });
      c.height(fb + 2);
      void top;
    }
  });
})(globalThis.OAChart);
