/* Euler diagram (coverage plan 3.8, extended; S88). Overlaps drawn at true size: two groups as circles whose areas, and the
 * area they share, are in proportion to their counts on one area scale, and a group in neither as a third circle apart, at
 * least its own radius away. Each region prints its name, count and share, inside it where the words fit with 4 px to spare,
 * else under the drawing on a leader. No frame: two circles cannot fill a rectangle at true area (Rule 14.82).
 * encode: region (text), value (number), share (number, optional).
 * labels: regions ({a, ab, b, none}: the region each row is, by its stored name), names ({stored: printed}), sets ([the
 * first circle's name, the second's]), fills ({a, ab, b, none}: color roles, none by default), edge (the circles' ink,
 * default subject), value_words ("{v}, {p}": the count and share). formats: value, share. */
(function (K) {
  'use strict';
  var ON = { subject: 'label-on-subject', 'cat-1': 'on-cat-1', 'cat-2': 'on-cat-2', 'cat-3': 'on-cat-3' };
  var R1 = function (v) { return Math.round(v * 10) / 10; };
  var arc_pts = function (cx, cy, r, a0, a1, n) { var p = []; for (var i = 0; i <= n; i++) { var t = a0 + (a1 - a0) * i / n; p.push([cx + r * Math.cos(t), cy + r * Math.sin(t)]); } return p; };
  // the area two circles share, their centers d apart
  var lens = function (a, b, d) {
    if (d >= a + b) return 0;
    if (d <= Math.abs(a - b)) return Math.PI * Math.min(a, b) * Math.min(a, b);
    return a * a * Math.acos((d * d + a * a - b * b) / (2 * d * a)) + b * b * Math.acos((d * d + b * b - a * a) / (2 * d * b)) -
      0.5 * Math.sqrt((-d + a + b) * (d + a - b) * (d - a + b) * (d + a + b));
  };
  K.register_chart({
    form: 'euler-diagram', name: 'Euler Diagram', family: 'proportion-and-overlap',
    encode: { region: 'text', value: 'number', share: 'number?' },
    labels: ['regions', 'names', 'sets', 'fills', 'edge', 'value_words'],
    phone: 'same',
    draw: function (c) {
      var L = c.labels, W = c.width, er = c.field('region'), ev = c.field('value'), es = c.field('share', false), f = c.spec.formats || {};
      var RG = L.regions || {}, FI = L.fills || {}, rows = c.all_rows || c.rows, by = {};
      ['a', 'ab', 'b', 'none'].forEach(function (k) { by[k] = rows.filter(function (r) { return r[er] === RG[k]; })[0]; if (!by[k]) c.warn('labels.regions.' + k + ' names no row'); });
      if (!by.a || !by.ab || !by.b || !by.none) { c.height(10); return; }
      var nm = function (r) { return (L.names || {})[r[er]] || r[er]; };
      var vw = function (r) { return String(L.value_words || '{v}').split('{v}').join(K.fmt(r[ev], f.value || 'integer')).split('{p}').join(es ? K.fmt(r[es], f.share || 'percent:1') : ''); };
      // one area scale: the first circle's radius sets it; the others, and the distance that gives the shared area, follow
      var tA = +by.a[ev] + +by.ab[ev], tB = +by.b[ev] + +by.ab[ev], tC = +by.none[ev];
      var u = { b: Math.sqrt(tB / tA), c: Math.sqrt(tC / tA) }, want = Math.PI * +by.ab[ev] / tA, lo = Math.abs(1 - u.b), hi = 1 + u.b;
      for (var it = 0; it < 60; it++) { var m = (lo + hi) / 2; if (lens(1, u.b, m) > want) lo = m; else hi = m; }
      var dd = (lo + hi) / 2, lab = c.size('label');
      var span = 1 + dd + u.b, gapC = Math.max(u.c, 0);
      var rA = c.phone ? Math.min(96, (W - 2) / span) : Math.min(124, (W - 2) / (span + 3 * u.c + 0.2));
      var rB = rA * u.b, rC = rA * u.c, d = rA * dd;
      if (Math.abs(lens(rA, rB, d) / (Math.PI * rA * rA) * tA - +by.ab[ev]) > 0.01 * +by.ab[ev]) c.warn('the shared area is off its count by more than 1 percent');
      var sets = L.sets || ['', ''];
      var xA = rA + 1, xB = xA + d, s1 = c.text(0, lab * 0.86, sets[0], { role: 'label', weight: 600, max: Math.max(80, d) });
      var s2 = c.text(xB + rB, lab * 0.86, sets[1], { role: 'label', weight: 600, anchor: 'end', max: Math.max(80, rB * 2 - 10) });
      var cy = Math.max(s1.bottom, s2.bottom) + 10 + rA;
      var a = (d * d + rA * rA - rB * rB) / (2 * d), h = Math.sqrt(rA * rA - a * a), px = xA + a;
      var A = Math.atan2(-h, a), B = Math.atan2(-h, a - d);
      var M = 'M' + R1(px) + ',' + R1(cy - h), Pb = R1(px) + ',' + R1(cy + h), Pt = R1(px) + ',' + R1(cy - h), ra = R1(rA) + ',' + R1(rA), rb = R1(rB) + ',' + R1(rB);
      var bigB = a > d ? 1 : 0;
      var reg = {
        a: { d: M + 'A' + ra + ' 0 1 0 ' + Pb + 'A' + rb + ' 0 ' + bigB + ' 1 ' + Pt + 'Z', p: arc_pts(xA, cy, rA, A, -A - 2 * Math.PI, 40).concat(arc_pts(xB, cy, rB, -B, 2 * Math.PI + B, 12)) },
        ab: { d: M + 'A' + rb + ' 0 ' + bigB + ' 0 ' + Pb + 'A' + ra + ' 0 0 0 ' + Pt + 'Z', p: arc_pts(xB, cy, rB, 2 * Math.PI + B, -B, 12).concat(arc_pts(xA, cy, rA, -A, A, 12)) },
        b: { d: M + 'A' + rb + ' 0 ' + (1 - bigB) + ' 1 ' + Pb + 'A' + ra + ' 0 0 0 ' + Pt + 'Z', p: arc_pts(xB, cy, rB, B, -B, 40).concat(arc_pts(xA, cy, rA, -A, A, 12)) }
      };
      ['a', 'ab', 'b'].forEach(function (k) {
        var g = reg[k], xs = g.p.map(function (q) { return q[0]; }), ys = g.p.map(function (q) { return q[1]; }), x0 = Math.min.apply(null, xs), y0 = Math.min.apply(null, ys);
        c.path(g.d, { fill: FI[k] || 'none', pts: [g.p], closed: true, kind: 'region', data: { key: by[k][er], field: ev, value: by[k][ev] } }, [x0, y0, Math.max.apply(null, xs) - x0, Math.max.apply(null, ys) - y0]);
      });
      // the third circle: beside the pair at a desk, under it on a phone
      var xC, cyC, below = cy + rA;
      var edge = { stroke: L.edge || 'subject', width: c.t('line-baseline') };
      c.circle(xA, cy, rA, Object.assign({ fill: 'none', kind: 'set', area_of: { value: tA, max_value: tA, max_radius: rA }, data: { key: sets[0], field: ev, value: tA } }, edge));
      c.circle(xB, cy, rB, Object.assign({ fill: 'none', kind: 'set', area_of: { value: tB, max_value: tA, max_radius: rA }, data: { key: sets[1], field: ev, value: tB } }, edge));
      // each region's words: the largest role that fits inside with 4 px to spare, else under the drawing on a leader
      var placed = [];
      var block = function (r, role) {
        var sz = c.size(role), lh = Math.round(sz * 1.25);
        return { sz: sz, lh: lh, n: c.wrap(nm(r), role, 999, 600).length + 1, w: Math.max(c.measure(nm(r), role, 600), c.measure(vw(r), role, 400, true)) };
      };
      var put = function (r, x, top, role, anchor, max, ink) {
        var sz = c.size(role), lh = Math.round(sz * 1.25);
        var t = c.text(x, top + sz * 0.86, nm(r), { role: role, weight: 600, anchor: anchor, max: max, leading: lh, fill: ink });
        var v = c.text(x, t.bottom - sz * 0.241 + lh, vw(r), { role: role, weight: 400, anchor: anchor, max: max, leading: lh, tnum: true, fill: ink });
        placed.push(t, v);
        return v.bottom;
      };
      var inside = function (k, x, room) {
        var r = by[k], roles = ['label', 'tick'];
        for (var i = 0; i < roles.length; i++) {
          var sz = c.size(roles[i]), lh = Math.round(sz * 1.25), w0 = room(0) - 8;
          var n = c.wrap(nm(r), roles[i], w0, 600).length + c.wrap(vw(r), roles[i], w0, 400).length, hh = sz + (n - 1) * lh;
          var wide = 0;
          c.wrap(nm(r), roles[i], w0, 600).forEach(function (s) { wide = Math.max(wide, c.measure(s, roles[i], 600)); });
          c.wrap(vw(r), roles[i], w0, 400).forEach(function (s) { wide = Math.max(wide, c.measure(s, roles[i], 400, true)); });
          if (n > 4 || wide > Math.min(room(-hh / 2), room(hh / 2)) - 8) continue;
          put(r, x, cy - hh / 2, roles[i], 'middle', w0 + 0.5, ON[FI[k]] || 'label');
          return true;
        }
        return false;
      };
      var halfA = function (dy) { return Math.sqrt(Math.max(0, rA * rA - dy * dy)); }, halfB = function (dy) { return Math.sqrt(Math.max(0, rB * rB - dy * dy)); };
      var out = [];
      if (!inside('a', (xA - rA + xB - rB) / 2, function (dy) { return (xB - halfB(dy)) - (xA - halfA(dy)); })) out.push(['a', xA - rA / 2]);
      if (!inside('ab', (xA + rA + xB - rB) / 2, function (dy) { return (xA + halfA(dy)) - (xB - halfB(dy)); })) out.push(['ab', (xA + rA + xB - rB) / 2]);
      if (!inside('b', (xA + rA + xB + rB) / 2, function (dy) { return (xB + halfB(dy)) - (xA + halfA(dy)); })) out.push(['b', xB + rB / 2]);
      var y = below + 14;
      out.forEach(function (o) {
        var r = by[o[0]], bl = block(r, 'label'), x = Math.max(bl.w / 2, Math.min(W - bl.w / 2, o[1]));
        var top = y + 8, bot = put(r, x, top, 'label', 'middle', W, 'label');
        c.line(o[1], o[0] === 'ab' ? cy : cy + rA * 0.4, o[1], top - 3, { stroke: 'leader', width: c.t('line-hairline'), mark: false });
        y = bot + 6;
      });
      if (c.phone) { xC = rC + 1; cyC = y + 14 + rC; }
      else { xC = xB + rB + gapC * rA + rC; cyC = cy; }
      c.circle(xC, cyC, rC, Object.assign({ fill: FI.none || 'none', kind: 'set', area_of: { value: tC, max_value: tA, max_radius: rA }, data: { key: by.none[er], field: ev, value: tC } }, edge));
      var nb = block(by.none, 'label'), endy;
      if (c.phone || xC + rC + 12 + nb.w > W) {
        if (c.phone) endy = Math.max(cyC + rC, put(by.none, 2 * rC + 14, cyC - (nb.lh + nb.sz) / 2, 'label', 'start', W - 2 * rC - 14, 'label'));
        else endy = put(by.none, Math.min(W - nb.w / 2, xC), cyC + rC + 10, 'label', 'middle', W, 'label');
      } else endy = Math.max(cyC + rC, put(by.none, xC + rC + 12, cyC - (nb.lh + nb.sz) / 2, 'label', 'start', W - xC - rC - 12, 'label'));
      c.height(Math.max(y, endy, cy + rA) + 6);
    }
  });
})(globalThis.OAChart);
