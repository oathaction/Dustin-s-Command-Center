/* Euler diagram (coverage plan 3.8, extended; S88). Overlaps drawn at true size: two groups as circles whose areas, and the
 * area they share, are in proportion to their counts on one area scale, and a group in neither as a third circle apart, at
 * least its own radius away. Each set's name stands centered over its circle. Each region prints its name, count and share
 * in the label size, the two lone groups in one line structure from one top line with 4 px to spare at every line; the
 * overlap takes the same structure or, where it cannot, sits under the circles on a leader down the overlap's own axis, the
 * line through the two points where the circles cross. No frame: two circles cannot fill a rectangle at true area. The form
 * fails a drawing whose shared area is more than 1 percent off its count; the kit checks each circle's radius.
 * encode: region (text), value (number), share (number, optional).
 * labels: regions ({a, ab, b, none}: the region each row is, by its stored name), names ({stored: printed}), sets ([the
 * first circle's name, the second's]), fills ({a, ab, b, none}: color roles, none by default), edge (the circles' ink,
 * default subject). formats: value, share. */
(function (K) {
  'use strict';
  var R1 = function (v) { return Math.round(v * 10) / 10; };
  var arc_pts = function (cx, cy, r, a0, a1, n) { var p = []; for (var i = 0; i <= n; i++) { var t = a0 + (a1 - a0) * i / n; p.push([cx + r * Math.cos(t), cy + r * Math.sin(t)]); } return p; };
  // the area two circles of radii a and b share, their centers d apart
  var lens = function (a, b, d) {
    if (d >= a + b) return 0;
    if (d <= Math.abs(a - b)) return Math.PI * Math.min(a, b) * Math.min(a, b);
    return a * a * Math.acos((d * d + a * a - b * b) / (2 * d * a)) + b * b * Math.acos((d * d + b * b - a * a) / (2 * d * b)) -
      0.5 * Math.sqrt((-d + a + b) * (d + a - b) * (d - a + b) * (d + a + b));
  };
  K.register_chart({
    form: 'euler-diagram', name: 'Euler Diagram', family: 'proportion-and-overlap',
    encode: { region: 'text', value: 'number', share: 'number?' },
    labels: ['regions', 'names', 'sets', 'fills', 'edge'],
    phone: 'same',
    draw: function (c) {
      var L = c.labels, W = c.width, er = c.field('region'), ev = c.field('value'), es = c.field('share', false), f = c.spec.formats || {};
      var RG = L.regions || {}, FI = L.fills || {}, rows = c.all_rows || c.rows, by = {};
      ['a', 'ab', 'b', 'none'].forEach(function (k) { by[k] = rows.filter(function (r) { return r[er] === RG[k]; })[0]; if (!by[k]) c.warn('labels.regions.' + k + ' names no row'); });
      if (!by.a || !by.ab || !by.b || !by.none) { c.height(10); return; }
      var lab = c.size('label'), LH = Math.round(lab * 1.25);
      // a region's words at a level: 0, name, count and share a line each; 1, the count's figure and unit apart; 2, the name's
      // words apart too
      var lines = function (r, lv) {
        var nm = (L.names || {})[r[er]] || r[er], v = K.fmt(r[ev], f.value || 'integer'), out = [];
        (lv > 1 ? nm.split(' ') : [nm]).forEach(function (q) { out.push([q, 600]); });
        (lv > 0 ? v.split(' ') : [v]).forEach(function (q) { out.push([q, 400]); });
        if (es) out.push([K.fmt(r[es], f.share || 'percent:1'), 400]);
        return out.map(function (q) { return [q[0], q[1], c.measure(q[0], 'label', q[1], q[1] === 400)]; });
      };
      var set_lines = function (ls, x, top, anchor) {
        var b = null;
        ls.forEach(function (ln, j) { b = c.text(x, top + j * LH + lab * 0.86, ln[0], { role: 'label', weight: ln[1], anchor: anchor, tnum: ln[1] === 400 }); });
        return b.bottom;
      };
      var wide = function (ls) { var w = 0; ls.forEach(function (ln) { w = Math.max(w, ln[2]); }); return w; };
      var high = function (ls) { return lab + (ls.length - 1) * LH; };
      // one area scale: the first circle's radius sets it; the others, and the distance that gives the shared area, follow
      var tA = +by.a[ev] + +by.ab[ev], tB = +by.b[ev] + +by.ab[ev], tC = +by.none[ev];
      var ub = Math.sqrt(tB / tA), uc = Math.sqrt(tC / tA), want = Math.PI * +by.ab[ev] / tA, lo = Math.abs(1 - ub), hi = 1 + ub;
      for (var it = 0; it < 60; it++) { var m = (lo + hi) / 2; if (lens(1, ub, m) > want) lo = m; else hi = m; }
      var dd = (lo + hi) / 2, span = 1 + dd + ub;
      var rA = c.phone ? Math.min(96, (W - 2) / span) : Math.min(132, (W - 2) / (span + 3 * uc + 0.15));
      var rB = rA * ub, rC = rA * uc, d = rA * dd;
      if (Math.abs(lens(rA, rB, d) / (Math.PI * rA * rA) * tA - +by.ab[ev]) > 0.01 * +by.ab[ev]) c.warn('the shared area is off its count by more than 1 percent');
      // each set's name centered over its circle, both on as many lines as the longer needs
      var sets = L.sets || ['', ''], xA = rA + 1, xB = xA + d, nmax = d - 12;
      var nh = function (q) { return c.wrap(q, 'label', nmax, 600).length; }, sl = Math.max(nh(sets[0]), nh(sets[1]));
      c.text(xA, lab * 0.86 + (sl - nh(sets[0])) * LH, sets[0], { role: 'label', weight: 600, anchor: 'middle', max: nmax });
      c.text(xB, lab * 0.86 + (sl - nh(sets[1])) * LH, sets[1], { role: 'label', weight: 600, anchor: 'middle', max: nmax });
      var cy = lab * 0.86 + (sl - 1) * LH + lab * 0.241 + 10 + rA;
      var a = (d * d + rA * rA - rB * rB) / (2 * d), h = Math.sqrt(rA * rA - a * a), px = xA + a;
      var A = Math.atan2(-h, a), B = Math.atan2(-h, a - d), bigB = a > d ? 1 : 0;
      var M = 'M' + R1(px) + ',' + R1(cy - h), Pb = R1(px) + ',' + R1(cy + h), Pt = R1(px) + ',' + R1(cy - h), ra = R1(rA) + ',' + R1(rA), rb = R1(rB) + ',' + R1(rB);
      var reg = {
        a: { d: M + 'A' + ra + ' 0 1 0 ' + Pb + 'A' + rb + ' 0 ' + bigB + ' 1 ' + Pt + 'Z', p: arc_pts(xA, cy, rA, A, -A - 2 * Math.PI, 40).concat(arc_pts(xB, cy, rB, -B, 2 * Math.PI + B, 12)) },
        ab: { d: M + 'A' + rb + ' 0 ' + bigB + ' 0 ' + Pb + 'A' + ra + ' 0 0 0 ' + Pt + 'Z', p: arc_pts(xB, cy, rB, 2 * Math.PI + B, -B, 12).concat(arc_pts(xA, cy, rA, -A, A, 12)) },
        b: { d: M + 'A' + rb + ' 0 ' + (1 - bigB) + ' 1 ' + Pb + 'A' + ra + ' 0 0 0 ' + Pt + 'Z', p: arc_pts(xB, cy, rB, B, -B, 40).concat(arc_pts(xA, cy, rA, -A, A, 12)) }
      };
      ['a', 'ab', 'b'].forEach(function (k) {
        var g = reg[k], xs = g.p.map(function (q) { return q[0]; }), ys = g.p.map(function (q) { return q[1]; }), x0 = Math.min.apply(null, xs), y0 = Math.min.apply(null, ys);
        c.path(g.d, { fill: FI[k] || 'none', pts: [g.p], closed: true, kind: 'region', data: { key: by[k][er], field: ev, value: by[k][ev] } }, [x0, y0, Math.max.apply(null, xs) - x0, Math.max.apply(null, ys) - y0]);
      });
      var edge = { stroke: L.edge || 'subject', width: c.t('line-baseline') };
      c.circle(xA, cy, rA, Object.assign({ fill: 'none', kind: 'set', area_of: { value: tA, max_value: tA, max_radius: rA }, data: { key: sets[0], field: ev, value: tA } }, edge));
      c.circle(xB, cy, rB, Object.assign({ fill: 'none', kind: 'set', area_of: { value: tB, max_value: tA, max_radius: rA }, data: { key: sets[1], field: ev, value: tB } }, edge));
      // the words inside: the fewest breaks at which both lone groups fit from one top line; the overlap takes the same
      // structure from the same top line, or leaves on its leader
      var hA = function (dy) { return Math.sqrt(Math.max(0, rA * rA - dy * dy)); }, hB = function (dy) { return Math.sqrt(Math.max(0, rB * rB - dy * dy)); };
      var inB = function (dy) { return Math.abs(dy) < rB; };
      var BD = {
        a: [function (dy) { return xA - hA(dy); }, function (dy) { return inB(dy) ? xB - hB(dy) : xA + hA(dy); }],
        ab: [function (dy) { return xB - hB(dy); }, function (dy) { return xA + hA(dy); }],
        b: [function (dy) { return xA + hA(dy); }, function (dy) { return xB + hB(dy); }]
      };
      var test = function (key, lv, T) {
        var ls = lines(by[key], lv), x0 = -1e9, x1 = 1e9;
        ls.forEach(function (ln, j) { var y0 = T + j * LH - cy; [y0, y0 + lab].forEach(function (dy) { x0 = Math.max(x0, BD[key][0](dy)); x1 = Math.min(x1, BD[key][1](dy)); }); });
        return wide(ls) + 8 <= x1 - x0 ? { ls: ls, x: (x0 + x1) / 2, top: T } : null;
      };
      var P = {};
      for (var lv = 0; lv < 3 && !P.a; lv++) {
        var n = Math.max(lines(by.a, lv).length, lines(by.b, lv).length), T = cy - (lab + (n - 1) * LH) / 2, pa = test('a', lv, T), pb = test('b', lv, T);
        if (pa && pb) { P.a = pa; P.b = pb; if (lines(by.ab, lv).length <= n) P.ab = test('ab', lv, T); }
      }
      ['a', 'ab', 'b'].forEach(function (key) { if (P[key]) set_lines(P[key].ls, P[key].x, P[key].top, 'middle'); });
      // words that do not fit sit under the circles in their own order, each on a leader straight down from its region
      var AT = { a: [xA - rA * 0.4, cy + rA * 0.5], ab: [px, cy], b: [xB + rB * 0.55, cy + rB * 0.5] }, y = cy + rA + 18;
      ['a', 'ab', 'b'].forEach(function (key) {
        if (P[key]) return;
        var ls = lines(by[key], 0), w = wide(ls), x = Math.max(w / 2, Math.min(W - w / 2, AT[key][0]));
        c.line(AT[key][0], AT[key][1], AT[key][0], y - 3, { stroke: 'leader', width: c.t('line-hairline'), mark: false });
        y = set_lines(ls, x, y, 'middle') + 14;
      });
      // no coverage: beside the pair at a desk, at least its own radius away; under them on a phone, its words beside it
      var nl = lines(by.none, 0), nw = wide(nl), nhh = high(nl), xC, cyC, end;
      if (c.phone) { xC = rC + 1; cyC = Math.max(y, cy + rA + 18) + rC; }
      else { xC = xB + rB + rC + rC; cyC = cy; }
      c.circle(xC, cyC, rC, Object.assign({ fill: FI.none || 'none', kind: 'set', area_of: { value: tC, max_value: tA, max_radius: rA }, data: { key: by.none[er], field: ev, value: tC } }, edge));
      if (c.phone || xC + rC + 12 + nw <= W) end = Math.max(cyC + rC, set_lines(nl, xC + rC + 12, cyC - nhh / 2, 'start'));
      else end = set_lines(nl, Math.min(W - nw / 2, xC), cyC + rC + 10, 'middle');
      c.height(Math.max(y - 14, end, cy + rA) + 6);
    }
  });
})(globalThis.OAChart);
