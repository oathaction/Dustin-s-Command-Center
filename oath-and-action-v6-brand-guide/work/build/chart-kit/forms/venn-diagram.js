/* Venn diagram (coverage plan 3.8, extended; S87). Two groups that overlap, as two equal circles inside a frame for everyone,
 * so four regions: the first group alone, both, the second alone, and neither (the frame outside both circles). Each region
 * prints its name, count and share inside it, with 4 px to spare. The circles are one size whatever the counts, and the
 * spec's note says so; the Euler diagram draws the same regions at true area (Rule 14.82).
 * encode: region (text), value (number), share (number, optional).
 * labels: regions ({a, ab, b, none}: the region each row is, by its stored name), names ({stored: printed}), sets ([the
 * first circle's name, the second's]), frame (the frame's name, {total} the sum of every row), fills ({a, ab, b, none}: color
 * roles, none by default), edge (the circles' ink, default subject). formats: value, share. */
(function (K) {
  'use strict';
  var ON = { subject: 'label-on-subject', 'cat-1': 'on-cat-1', 'cat-2': 'on-cat-2', 'cat-3': 'on-cat-3' };
  var R1 = function (v) { return Math.round(v * 10) / 10; };
  // a circular arc as points, for the checks: from angle a0 to a1 (radians, y down), n steps
  var arc_pts = function (cx, cy, r, a0, a1, n) { var p = []; for (var i = 0; i <= n; i++) { var t = a0 + (a1 - a0) * i / n; p.push([cx + r * Math.cos(t), cy + r * Math.sin(t)]); } return p; };
  K.register_chart({
    form: 'venn-diagram', name: 'Venn Diagram', family: 'proportion-and-overlap',
    encode: { region: 'text', value: 'number', share: 'number?' },
    labels: ['regions', 'names', 'sets', 'frame', 'fills', 'edge'],
    phone: 'same',
    draw: function (c) {
      var L = c.labels, W = c.width, er = c.field('region'), ev = c.field('value'), es = c.field('share', false), f = c.spec.formats || {};
      var RG = L.regions || {}, FI = L.fills || {}, rows = c.all_rows || c.rows, by = {};
      ['a', 'ab', 'b', 'none'].forEach(function (k) { by[k] = rows.filter(function (r) { return r[er] === RG[k]; })[0]; if (!by[k]) c.warn('labels.regions.' + k + ' names no row'); });
      if (!by.a || !by.ab || !by.b || !by.none) { c.height(10); return; }
      var fv = function (v) { return K.fmt(v, f.value || 'integer'); };
      // a region's words: its name, count and share, each on as few lines as the room allows
      var lines = function (r, role, w) {
        var out = [];
        [[(L.names || {})[r[er]] || r[er], 600], [fv(r[ev]), 400]].concat(es ? [[K.fmt(r[es], f.share || 'percent:1'), 400]] : []).forEach(function (p) {
          c.wrap(p[0], role, w, p[1]).forEach(function (s) { out.push([s, p[1], c.measure(s, role, p[1], p[1] === 400)]); });
        });
        return out;
      };
      var set_lines = function (ls, x, top, role, anchor, ink) {
        var sz = c.size(role), lh = Math.round(sz * 1.25), b = null;
        ls.forEach(function (ln, j) { b = c.text(x, top + j * lh + sz * 0.86, ln[0], { role: role, weight: ln[1], anchor: anchor, tnum: ln[1] === 400, fill: ink }); });
        return b.bottom;
      };
      // inside a region bounded at each height dy from the circles' middle by lo(dy) and hi(dy); a fault where nothing fits
      var inside = function (r, cy, lo, hi, ink) {
        var roles = ['label', 'tick'];
        for (var i = 0; i < roles.length; i++) {
          var sz = c.size(roles[i]), lh = Math.round(sz * 1.25), ls = lines(r, roles[i], hi(0) - lo(0) - 8);
          var hh = sz + (ls.length - 1) * lh, top = cy - hh / 2, a = -1e9, b = 1e9, wide = 0;
          ls.forEach(function (ln, j) { wide = Math.max(wide, ln[2]); [top + j * lh - cy, top + j * lh + sz - cy].forEach(function (dy) { a = Math.max(a, lo(dy)); b = Math.min(b, hi(dy)); }); });
          if (ls.length > 5 || wide + 8 > b - a) continue;
          set_lines(ls, (a + b) / 2, top, roles[i], 'middle', ink);
          return true;
        }
        c.warn('the words for ' + r[er] + ' do not fit inside its region at ' + W + ' px');
        return false;
      };
      var tot = rows.reduce(function (t, r) { return t + (+r[ev] || 0); }, 0);
      var tick = c.size('tick'), lab = c.size('label'), pad = c.phone ? 10 : 16;
      // the frame's name, then the two circles' names, then the circles, centered in the frame
      var ft = L.frame ? c.text(pad, pad + tick * 0.86, String(L.frame).split('{total}').join(fv(tot)), { role: 'tick', weight: 600, max: W - 2 * pad }) : null;
      var k = c.phone ? 1.12 : 1.2, r = Math.min(c.phone ? 96 : 132, Math.floor((W - 2 * pad) / (2 + k))), d = k * r;
      var cx1 = W / 2 - d / 2, cx2 = W / 2 + d / 2, sets = L.sets || ['', ''], nmax = Math.max(80, (2 * r + d) / 2 - 6);
      var sy = (ft ? ft.bottom : pad) + 12 + lab * 0.86;
      var s1 = c.text(cx1 - r, sy, sets[0], { role: 'label', weight: 600, max: nmax });
      var s2 = c.text(cx2 + r, sy, sets[1], { role: 'label', weight: 600, anchor: 'end', max: nmax });
      var cy = Math.max(s1.bottom, s2.bottom) + 8 + r;
      // the circles meet at two points on the line halfway between their centers
      var a = d / 2, h = Math.sqrt(r * r - a * a), px = cx1 + a, A = Math.atan2(-h, a), B = Math.atan2(-h, -a);
      var M = 'M' + R1(px) + ',' + R1(cy - h), Pb = R1(px) + ',' + R1(cy + h), Pt = R1(px) + ',' + R1(cy - h), rr = R1(r) + ',' + R1(r);
      var reg = {
        a: { d: M + 'A' + rr + ' 0 1 0 ' + Pb + 'A' + rr + ' 0 0 1 ' + Pt + 'Z', p: arc_pts(cx1, cy, r, A, -A - 2 * Math.PI, 40).concat(arc_pts(cx2, cy, r, -B, 2 * Math.PI + B, 12)) },
        ab: { d: M + 'A' + rr + ' 0 0 0 ' + Pb + 'A' + rr + ' 0 0 0 ' + Pt + 'Z', p: arc_pts(cx2, cy, r, 2 * Math.PI + B, -B, 12).concat(arc_pts(cx1, cy, r, -A, A, 12)) },
        b: { d: M + 'A' + rr + ' 0 1 1 ' + Pb + 'A' + rr + ' 0 0 0 ' + Pt + 'Z', p: arc_pts(cx2, cy, r, B, -B, 40).concat(arc_pts(cx1, cy, r, -A, A, 12)) }
      };
      // no coverage: in the frame beside the second circle where it fits, else in a band under the circles
      var nl = lines(by.none, 'label', 9999), nh = lab + (nl.length - 1) * Math.round(lab * 1.25), nw = 0;
      nl.forEach(function (ln) { nw = Math.max(nw, ln[2]); });
      var side = W - pad - (cx2 + r + 16) >= nw && nh <= 2 * r, fb = side ? cy + r + pad : cy + r + 12 + nh + pad;
      c.rect(0.5, 0.5, W - 1, fb - 0.5, { fill: FI.none || 'none', kind: 'region', data: { key: by.none[er], field: ev, value: by.none[ev] } });
      c.rect(0.5, 0.5, W - 1, fb - 0.5, { stroke: 'context', width: 1, mark: false });
      // the circles' ground knocks the frame's fill out, then each region takes its own
      if (FI.none) { c.circle(cx1, cy, r, { fill: 'surface', mark: false }); c.circle(cx2, cy, r, { fill: 'surface', mark: false }); }
      ['a', 'ab', 'b'].forEach(function (key) {
        var row = by[key], g = reg[key], xs = g.p.map(function (q) { return q[0]; }), ys = g.p.map(function (q) { return q[1]; });
        var x0 = Math.min.apply(null, xs), y0 = Math.min.apply(null, ys);
        c.path(g.d, { fill: FI[key] || 'none', pts: [g.p], closed: true, kind: 'region', data: { key: row[er], field: ev, value: row[ev] } }, [x0, y0, Math.max.apply(null, xs) - x0, Math.max.apply(null, ys) - y0]);
      });
      c.circle(cx1, cy, r, { stroke: L.edge || 'subject', width: c.t('line-baseline'), mark: false });
      c.circle(cx2, cy, r, { stroke: L.edge || 'subject', width: c.t('line-baseline'), mark: false });
      var half = function (dy) { return Math.sqrt(Math.max(0, r * r - dy * dy)); };
      inside(by.a, cy, function (dy) { return cx1 - half(dy); }, function (dy) { return cx2 - half(dy); }, ON[FI.a] || 'label');
      inside(by.ab, cy, function (dy) { return cx2 - half(dy); }, function (dy) { return cx1 + half(dy); }, ON[FI.ab] || 'label');
      inside(by.b, cy, function (dy) { return cx1 + half(dy); }, function (dy) { return cx2 + half(dy); }, ON[FI.b] || 'label');
      if (side) set_lines(nl, cx2 + r + 16 + (W - pad - cx2 - r - 16 - nw) / 2, cy - nh / 2, 'label', 'start', ON[FI.none] || 'label');
      else set_lines(nl, W - pad, cy + r + 12, 'label', 'end', ON[FI.none] || 'label');
      c.height(fb + 2);
    }
  });
})(globalThis.OAChart);
