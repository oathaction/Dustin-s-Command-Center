/* Venn diagram (coverage plan 3.8, extended; S87). Two groups that overlap, as two equal circles inside a frame for everyone,
 * so four regions: the first group alone, both, the second alone, and neither (the frame outside both circles). The circles
 * are one size whatever the counts, and the spec's note says so; the Euler diagram draws the same regions at true area (Rule
 * 14.82). Each set's name stands centered over its circle. Each region prints its name, count and share in the label size,
 * every region inside the circles in one line structure from one top line, with 4 px to spare at every line; a region that
 * cannot take that structure sits under the circles, in the frame, on a leader straight down from it.
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
      var fv = function (v) { return K.fmt(v, f.value || 'integer'); }, lab = c.size('label'), LH = Math.round(lab * 1.25);
      // a region's words at a level: 0, name, count and share a line each; 1, the count's figure and unit apart; 2, the name's
      // words apart too
      var lines = function (r, lv) {
        var nm = (L.names || {})[r[er]] || r[er], v = fv(r[ev]), out = [];
        (lv > 1 ? nm.split(' ') : [nm]).forEach(function (s) { out.push([s, 600]); });
        (lv > 0 ? v.split(' ') : [v]).forEach(function (s) { out.push([s, 400]); });
        if (es) out.push([K.fmt(r[es], f.share || 'percent:1'), 400]);
        return out.map(function (q) { return [q[0], q[1], c.measure(q[0], 'label', q[1], q[1] === 400)]; });
      };
      var set_lines = function (ls, x, top, anchor, ink) {
        var b = null;
        ls.forEach(function (ln, j) { b = c.text(x, top + j * LH + lab * 0.86, ln[0], { role: 'label', weight: ln[1], anchor: anchor, tnum: ln[1] === 400, fill: ink }); });
        return b.bottom;
      };
      var tot = rows.reduce(function (t, r) { return t + (+r[ev] || 0); }, 0);
      var tick = c.size('tick'), pad = c.phone ? 10 : 16;
      // the frame's name, then the two circles' names, each centered over its circle, then the circles
      var ft = L.frame ? c.text(pad, pad + tick * 0.86, String(L.frame).split('{total}').join(fv(tot)), { role: 'tick', weight: 600, max: W - 2 * pad }) : null;
      var k = c.phone ? 1.12 : 1.2, r = Math.min(c.phone ? 96 : 132, Math.floor((W - 2 * pad) / (2 + k))), d = k * r;
      var cx1 = W / 2 - d / 2, cx2 = W / 2 + d / 2, sets = L.sets || ['', ''], nmax = d - 12;
      var nh = function (s) { return c.wrap(s, 'label', nmax, 600).length; }, sl = Math.max(nh(sets[0]), nh(sets[1]));
      var sy = (ft ? ft.bottom : pad) + 12 + lab * 0.86;
      c.text(cx1, sy + (sl - nh(sets[0])) * LH, sets[0], { role: 'label', weight: 600, anchor: 'middle', max: nmax });
      c.text(cx2, sy + (sl - nh(sets[1])) * LH, sets[1], { role: 'label', weight: 600, anchor: 'middle', max: nmax });
      var cy = sy + (sl - 1) * LH + lab * 0.241 + 10 + r;
      // the circles meet at two points on the line halfway between their centers
      var a = d / 2, h = Math.sqrt(r * r - a * a), px = cx1 + a, A = Math.atan2(-h, a), B = Math.atan2(-h, -a);
      var M = 'M' + R1(px) + ',' + R1(cy - h), Pb = R1(px) + ',' + R1(cy + h), Pt = R1(px) + ',' + R1(cy - h), rr = R1(r) + ',' + R1(r);
      var reg = {
        a: { d: M + 'A' + rr + ' 0 1 0 ' + Pb + 'A' + rr + ' 0 0 1 ' + Pt + 'Z', p: arc_pts(cx1, cy, r, A, -A - 2 * Math.PI, 40).concat(arc_pts(cx2, cy, r, -B, 2 * Math.PI + B, 12)) },
        ab: { d: M + 'A' + rr + ' 0 0 0 ' + Pb + 'A' + rr + ' 0 0 0 ' + Pt + 'Z', p: arc_pts(cx2, cy, r, 2 * Math.PI + B, -B, 12).concat(arc_pts(cx1, cy, r, -A, A, 12)) },
        b: { d: M + 'A' + rr + ' 0 1 1 ' + Pb + 'A' + rr + ' 0 0 0 ' + Pt + 'Z', p: arc_pts(cx2, cy, r, B, -B, 40).concat(arc_pts(cx1, cy, r, -A, A, 12)) }
      };
      // the words inside: the fewest breaks at which both lone groups fit from one top line; the overlap takes the same
      // structure from the same top line, or leaves on its leader
      var half = function (dy) { return Math.sqrt(Math.max(0, r * r - dy * dy)); };
      var BD = {
        a: [function (dy) { return cx1 - half(dy); }, function (dy) { return cx2 - half(dy); }],
        ab: [function (dy) { return cx2 - half(dy); }, function (dy) { return cx1 + half(dy); }],
        b: [function (dy) { return cx1 + half(dy); }, function (dy) { return cx2 + half(dy); }]
      };
      var test = function (key, lv, T) {
        var ls = lines(by[key], lv), x0 = -1e9, x1 = 1e9, w = 0;
        ls.forEach(function (ln, j) { w = Math.max(w, ln[2]); var y0 = T + j * LH - cy; [y0, y0 + lab].forEach(function (dy) { x0 = Math.max(x0, BD[key][0](dy)); x1 = Math.min(x1, BD[key][1](dy)); }); });
        return w + 8 <= x1 - x0 ? { ls: ls, x: (x0 + x1) / 2, top: T } : null;
      };
      var P = {};
      for (var lv = 0; lv < 3 && !P.a; lv++) {
        var n = Math.max(lines(by.a, lv).length, lines(by.b, lv).length), T = cy - (lab + (n - 1) * LH) / 2, pa = test('a', lv, T), pb = test('b', lv, T);
        if (pa && pb) { P.a = pa; P.b = pb; if (lines(by.ab, lv).length <= n) P.ab = test('ab', lv, T); }
      }
      var AT = { a: [cx1 - r / 2, cy + r * 0.5], ab: [px, cy], b: [cx2 + r / 2, cy + r * 0.5] };
      var y = cy + r + 12, out = [];
      ['a', 'ab', 'b'].forEach(function (key) {
        if (P[key]) return;
        var ls = lines(by[key], 0), w = 0;
        ls.forEach(function (ln) { w = Math.max(w, ln[2]); });
        out.push({ k: key, ls: ls, x: Math.max(pad + w / 2, Math.min(W - pad - w / 2, AT[key][0])), top: y });
        y += lab + (ls.length - 1) * LH + 12;
      });
      // no coverage: in the frame beside the second circle where it fits, else in the band under the circles
      var nl = lines(by.none, 0), nhh = lab + (nl.length - 1) * LH, nw = 0;
      nl.forEach(function (ln) { nw = Math.max(nw, ln[2]); });
      var side = W - pad - (cx2 + r + 16) >= nw && nhh <= 2 * r, ntop = y, fb = side ? Math.max(cy + r + pad, y - 12 + pad) : y + nhh + pad;
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
      out.forEach(function (o) { c.line(AT[o.k][0], AT[o.k][1], AT[o.k][0], o.top - 3, { stroke: 'leader', width: c.t('line-hairline'), mark: false }); });
      ['a', 'ab', 'b'].forEach(function (key) { if (P[key]) set_lines(P[key].ls, P[key].x, P[key].top, 'middle', ON[FI[key]] || 'label'); });
      out.forEach(function (o) { set_lines(o.ls, o.x, o.top, 'middle', 'label'); });
      if (side) set_lines(nl, cx2 + r + 16 + (W - pad - cx2 - r - 16 - nw) / 2, cy - nhh / 2, 'start', ON[FI.none] || 'label');
      else set_lines(nl, W - pad, ntop, 'end', ON[FI.none] || 'label');
      c.height(fb + 2);
    }
  });
})(globalThis.OAChart);
