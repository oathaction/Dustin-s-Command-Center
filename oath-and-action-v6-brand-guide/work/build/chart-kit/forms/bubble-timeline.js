/* Bubble timeline (coverage plan 3.3, extended; S34). Events or periods along one time axis, each a circle whose area is in
 * proportion to a count (D2-124), centered on one line. Circles overlap where periods sit close; each takes a light fill and
 * an outline, drawn oldest first, so every edge stays visible. A period with nothing to count takes a short tick on the
 * line; a period still under way takes a dashed outline. A key of round sizes sits above.
 * encode: key (id), x (year, month or date), size (number), complete (boolean, optional: false marks a period under way).
 * labels: key_title (words over the size key), key_values (round sizes for the key), key_unit (words after each key value,
 * with {value}), partial (words in the key for a period under way), phone_from (on a phone, the x from which each period
 * takes its own row, with its circle and count; the earlier periods are summed in words), phone_before (those words, with
 * {first_x}, {last_x}, {from_x}, {n}, {sum} and {max}), phone_value and phone_partial (each row's count, with {value}).
 * formats: size (in the words), x.
 * annotations: [{at: {x}, text, value, place, dx, dy, max, anchor, phone}]: a note with a leader to the top of that
 * circle; "value": true prints the count before the text.
 * With labels.phone_from on a wide drawing (round 1 fix pass, CD B-S1): the earlier periods are summed in the same words
 * as on a phone, and from phone_from on the circles sit alternately above and below the line, each touching it, with the
 * largest radius set so no two circles on one side meet; on one line, the circles of busy decades merged into one mass.
 * Maker B, round 1. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'bubble-timeline',
    name: 'Bubble Timeline',
    family: 'change-over-time',
    encode: { key: 'id', x: 'time', size: 'number', complete: 'boolean?' },
    labels: ['key_title', 'key_values', 'key_unit', 'partial', 'phone_from', 'phone_before', 'phone_value', 'phone_partial'],
    phone: 'differs',
    draw: function (c) {
      // an outline drawn as a path, so it can take a dash
      var ring = function (x, y, r, dash) { c.path('M' + K.round(x - r) + ',' + K.round(y) + 'a' + K.round(r) + ',' + K.round(r) + ' 0 1,0 ' + K.round(2 * r) + ',0a' + K.round(r) + ',' + K.round(r) + ' 0 1,0 ' + K.round(-2 * r) + ',0', { stroke: 'subject', width: c.t('bubble-outline'), dash: dash, mark: false }); };
      var P = K.parts, L = c.labels, f = c.spec.formats || {}, W = c.width;
      var ek = c.field('key'), ex = c.field('x'), es = c.field('size'), ec = c.field('complete', false);
      var rows = c.rows.slice().sort(function (a, b) { return K.time(a[ex]) - K.time(b[ex]); });
      var vmax = Math.max.apply(null, rows.map(function (r) { return r[es] || 0; }));
      var rmax = c.t(c.phone ? 'bubble-radius-max-phone' : 'bubble-radius-max-mid');
      var from = L.phone_from !== undefined ? K.time(L.phone_from) : null;
      var early = from === null ? [] : rows.filter(function (r) { return K.time(r[ex]) < from; });
      var late = from === null ? rows : rows.filter(function (r) { return K.time(r[ex]) >= from; });
      var stagger = !c.phone && from !== null && late.length > 2, sx = null, rgap = 3;
      if (stagger) {
        // the largest radius at which no two circles on one side of the line meet, and the line's ends inside the drawing
        var lt = late.map(function (r) { return K.time(r[ex]); }), q = late.map(function (r) { return Math.sqrt((r[es] || 0) / vmax); });
        var fit = function (R) {
          var x0s = Math.max(4, q[0] * R + 1), x1s = W - Math.max(8, q[q.length - 1] * R + 8);
          var xf = K.scale.linear([lt[0], lt[lt.length - 1]], [x0s, x1s]), best = R;
          for (var i = 0; i + 2 < lt.length; i++) if (q[i] + q[i + 2] > 0) best = Math.min(best, (xf(lt[i + 2]) - xf(lt[i]) - rgap) / (q[i] + q[i + 2]));
          return { R: best, xs: xf };
        };
        var ft = fit(rmax); ft = fit(Math.min(rmax, ft.R)); ft = fit(Math.min(rmax, ft.R));
        rmax = Math.floor(Math.min(rmax, ft.R) * 10) / 10; sx = fit(rmax).xs;
      }
      var rs = K.scale.sqrt(vmax, rmax);
      var size = c.size('label'), y = 0;
      // the size key: round sizes side by side on one baseline, each with its figure
      var kv = (L.key_values || []).filter(function (v) { return v <= vmax * 1.2; });
      if (L.key_title) { var kt = c.text(0, size, L.key_title, { role: 'label', weight: 600, max: W }); y = kt.bottom + 6; }
      if (kv.length) {
        var kr = Math.max.apply(null, kv.map(function (v) { return Math.sqrt(v / vmax) * rmax; })), kx = 0, base = y + 2 * kr;
        kv.forEach(function (v) {
          var r = Math.sqrt(v / vmax) * rmax;
          c.circle(kx + r, base - r, r, { fill: 'band', mark: false });
          c.circle(kx + r, base - r, r, { stroke: 'subject', width: c.t('bubble-outline'), mark: false });
          var words = String(L.key_unit || '{value}').replace('{value}', K.fmt(v, f.size || 'integer'));
          var tb = c.text(kx + 2 * r + 6, base - 2, words, { role: 'tick' });
          kx = tb.x + tb.w + 18;
        });
        if (L.partial && ec && rows.some(function (r) { return r[ec] === false; })) {
          var pr = Math.min(kr, 9), pw = c.measure(L.partial, 'tick');
          // the partial key goes to its own line where the row has no room left for it
          if (kx + 2 * pr + 6 + pw > W) { kx = 0; base += 2 * pr + 10; }
          ring(kx + pr, base - pr, pr, '3 2');
          var pb = c.text(kx + 2 * pr + 6, base - 2, L.partial, { role: 'tick', max: W - kx - 2 * pr - 6 });
          base = Math.max(base, pb.bottom);
        }
        y = base + 18;
      }
      // the periods before labels.phone_from are summed in a line of words, on a phone and on a staggered wide drawing
      if (from !== null && early.length && L.phone_before && (c.phone || stagger)) {
        var sum = 0, emax = 0;
        early.forEach(function (r) { sum += r[es] || 0; emax = Math.max(emax, r[es] || 0); });
        var ew = String(L.phone_before).replace('{first_x}', K.fmt(early[0][ex], f.x || 'year')).replace('{last_x}', K.fmt(early[early.length - 1][ex], f.x || 'year'))
          .replace('{from_x}', K.fmt(L.phone_from, f.x || 'year')).replace('{n}', K.fmt(early.length, 'integer')).replace('{sum}', K.fmt(sum, f.size || 'integer')).replace('{max}', K.fmt(emax, f.size || 'integer'));
        var eb = c.text(0, y + size, ew, { role: 'label', max: W });
        early.forEach(function (r) { c.datum(0, eb.y, { data: { key: r[ek], field: es, value: r[es] || 0 } }); });
        y = eb.bottom + 14;
      }
      // on a phone the circles of busy decades would merge into one mass, so the form changes (DR-64, Rule 14.12): each
      // later period takes its own row, its circle and count
      if (c.phone && from !== null) {
        var lmax = Math.max.apply(null, late.map(function (r) { return r[es] || 0; })), yw = 0;
        late.forEach(function (r) { yw = Math.max(yw, c.measure(K.fmt(r[ex], f.x || 'year'), 'tick', 400, true)); });
        var pcx = Math.ceil(yw + 12 + rmax);
        late.forEach(function (r) {
          var v = r[es] || 0, rad = rs(v), h = Math.max(22, Math.ceil(2 * rad) + 6), pcy = y + h / 2, under = ec && r[ec] === false, big = v === lmax || under;
          c.text(0, pcy + c.size('tick') * 0.35, K.fmt(r[ex], f.x || 'year'), { role: 'tick', tnum: true });
          if (!v) c.line(pcx - 3, pcy, pcx + 3, pcy, { stroke: 'context', width: c.t('line-hairline'), data: { key: r[ek], field: es, value: 0 } });
          else {
            c.circle(pcx, pcy, rad, { fill: under ? 'surface' : 'band', data: { key: r[ek], field: es, value: v }, area_of: { value: v, max_value: vmax, max_radius: rmax } });
            if (under) ring(pcx, pcy, rad, '3 2'); else c.circle(pcx, pcy, rad, { stroke: 'subject', width: c.t('bubble-outline'), mark: false });
          }
          var pw = String(under && L.phone_partial ? L.phone_partial : (L.phone_value || '{value}')).replace('{value}', K.fmt(v, f.size || 'integer'));
          c.text(pcx + rmax + 10, pcy + size * 0.35, pw, { role: 'label', weight: big ? 700 : 400, tnum: true });
          y += h;
        });
        c.height(y + 4);
        return;
      }
      if (stagger) {
        // notes go above the upper circles, so the line sits low enough to leave them room
        var scy = y + 2 * rmax + (c.annotations.length ? 2 * size + 24 : 8), sbot = scy + 2 * rmax;
        var stl = K.time(late[0][ex]), sth = K.time(late[late.length - 1][ex]), dstep = 10;
        while (sx(stl + dstep) - sx(stl) < c.measure('0000', 'tick') + 16) dstep *= 2;
        var decades = [];
        for (var dy0 = Math.ceil(stl / dstep) * dstep; dy0 <= sth; dy0 += dstep) decades.push(dy0);
        // a hairline from the top of the upper circles to the axis at each round year, under the circles
        decades.forEach(function (yr) { c.line(sx(yr), scy - 2 * rmax, sx(yr), sbot + 4, { stroke: 'gridline', width: c.t('line-hairline'), mark: false }); });
        c.line(0, scy, W, scy, { stroke: 'baseline', width: c.t('line-hairline'), mark: false });
        var tops = {};
        late.forEach(function (r, i) {
          var v = r[es] || 0, x = sx(K.time(r[ex])), rad = rs(v), up = i % 2 === 0;
          if (!v) { c.line(x, scy - 3, x, scy + 3, { stroke: 'context', width: c.t('line-hairline'), data: { key: r[ek], field: es, value: 0 } }); tops[String(r[ex])] = scy; return; }
          var ccy = up ? scy - rad : scy + rad, under = ec && r[ec] === false;
          c.circle(x, ccy, rad, { fill: under ? 'surface' : 'band', data: { key: r[ek], field: es, value: v }, area_of: { value: v, max_value: vmax, max_radius: rmax } });
          if (under) ring(x, ccy, rad, '3 2'); else c.circle(x, ccy, rad, { stroke: 'subject', width: c.t('bubble-outline'), mark: false });
          tops[String(r[ex])] = ccy - rad;
        });
        var say = sbot + c.size('tick') + 10;
        decades.forEach(function (yr) {
          var hw = c.measure(String(yr), 'tick') / 2;
          c.text(Math.max(hw, Math.min(W - hw, sx(yr))), say, String(yr), { role: 'tick', anchor: 'middle' });
        });
        c.annotations.forEach(function (a) {
          if (tops[String(a.at.x)] === undefined) { c.warn('annotation at ' + JSON.stringify(a.at) + ' matches no row drawn on the line'); return; }
          var r = late.filter(function (q2) { return String(q2[ex]) === String(a.at.x); })[0];
          var words = a.value ? K.fmt(r[es], f.size || 'integer') + (a.text || '') : a.text;
          P.note(c, sx(K.time(r[ex])), tops[String(a.at.x)], words, { place: a.place || 'above', dx: a.dx, dy: a.dy, max: a.max, anchor: a.anchor, weight: a.value ? 700 : 400 });
        });
        c.height(say + 4);
        return;
      }
      // the line the circles sit on, and the time axis under it
      var ts = rows.map(function (r) { return K.time(r[ex]); }), tlo = ts[0], thi = ts[ts.length - 1];
      // the ends leave room for the largest circle at either end
      var rfirst = rs(rows[0][es] || 0), rlast = rs(rows[rows.length - 1][es] || 0), rbig = 0;
      rows.forEach(function (r) { rbig = Math.max(rbig, rs(r[es] || 0)); });
      var x0 = Math.max(4, rfirst + 1), x1 = W - Math.max(4, rlast + 1, rbig * 0.5);
      var xs = K.scale.linear([tlo, thi], [x0, x1]);
      rows.forEach(function (r) { var o = xs(K.time(r[ex])) + rs(r[es] || 0) - (W - 1); if (o > 0) x1 -= o; });
      xs = K.scale.linear([tlo, thi], [x0, x1]);
      // notes go above the circles, so the circles' line sits low enough to leave them room
      var cy = y + rmax * 2 + (c.annotations.length ? 2 * size + 24 : 8);
      c.line(0, cy, W, cy, { stroke: 'baseline', width: c.t('line-hairline'), mark: false });
      rows.forEach(function (r) {
        var v = r[es] || 0, x = xs(K.time(r[ex])), rad = rs(v);
        if (!v) { c.line(x, cy - 3, x, cy + 3, { stroke: 'context', width: c.t('line-hairline'), data: { key: r[ek], field: es, value: 0 } }); return; }
        var under = ec && r[ec] === false;
        c.circle(x, cy, rad, { fill: under ? 'surface' : 'band', data: { key: r[ek], field: es, value: v }, area_of: { value: v, max_value: vmax, max_radius: rmax } });
        if (under) ring(x, cy, rad, '3 2'); else c.circle(x, cy, rad, { stroke: 'subject', width: c.t('bubble-outline'), mark: false });
      });
      // the axis: a year at each round step, thinned to fit
      var ay = cy + rmax + c.size('tick') + 8, step = 10;
      while (xs(tlo + step) - xs(tlo) < c.measure('0000', 'tick') + 16) step *= 2;
      for (var yr = Math.ceil(tlo / step) * step; yr <= thi; yr += step) {
        var hw = c.measure(String(yr), 'tick') / 2, xx = Math.max(hw, Math.min(W - hw, xs(yr)));
        c.line(xs(yr), cy + rmax + 2, xs(yr), cy + rmax + 6, { stroke: 'baseline', width: c.t('line-hairline'), mark: false });
        c.text(xx, ay, String(yr), { role: 'tick', anchor: 'middle' });
      }
      // notes with leaders to the top of their circles
      c.annotations.forEach(function (a) {
        if (c.phone && a.phone && a.phone.hide) return;
        var r = rows.filter(function (q) { return String(q[ex]) === String(a.at.x); })[0];
        if (!r) { c.warn('annotation at ' + JSON.stringify(a.at) + ' matches no row'); return; }
        var o = Object.assign({}, a, c.phone && a.phone ? a.phone : {});
        var words = a.value ? K.fmt(r[es], f.size || 'integer') + (a.text || '') : a.text;
        P.note(c, xs(K.time(r[ex])), cy - rs(r[es] || 0), words, { place: o.place || 'above', dx: o.dx, dy: o.dy, max: o.max, anchor: o.anchor, weight: a.value ? 700 : 400 });
      });
      c.height(ay + 4);
    }
  });
})(globalThis.OAChart);
