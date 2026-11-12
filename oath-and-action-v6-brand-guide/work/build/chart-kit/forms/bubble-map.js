/* Bubble map (coverage plan 3.14, core; S16). A circle at each state's center, its area in proportion to the size column
 * (D2-124), shaded by the shade column in one sequential ink (Verdigris steps), over the land; circles move apart only where
 * they would overlap; a ring marks the states the spec singles out.
 * encode: code (code), size (number), shade (number). labels: bins ([b1, b2, b3, b4]: shade steps 1 to 5), ring ([codes]),
 * ring_label, shade_title, size_title, size_steps ([values]), size_unit, nation (a shade value marked on the key),
 * nation_label. formats: shade, size. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'bubble-map', name: 'Bubble Map', family: 'maps',
    encode: { code: 'code', size: 'number', shade: 'number' },
    labels: ['bins', 'ring', 'ring_label', 'shade_title', 'size_title', 'size_steps', 'size_unit', 'size_step_words', 'nation', 'nation_label', 'offsets', 'offsets_phone'],
    phone: 'same',
    draw: function (c) {
      var G = globalThis.OAChartGeo, rows = c.rows, ec = c.field('code'), ez = c.field('size'), eh = c.field('shade');
      var L = c.labels, f = c.spec.formats || {}, W = c.width, bins = L.bins || [];
      var R = c.t(c.phone ? 'bubble-radius-max-phone' : (W >= 900 ? 'bubble-radius-max-wide' : W >= 560 ? 'bubble-radius-max-mid' : 'bubble-radius-max-phone'));
      // the size scale takes only the rows the map draws, so a national row in the table sets no circle's size (D3-96)
      var drawn = rows.filter(function (r) { return G.centers[r[ec]]; });
      var maxv = Math.max.apply(null, drawn.map(function (r) { return r[ez]; })), area = K.scale.sqrt(maxv, R);
      // the key above the map
      var y = 0, kw = c.phone ? W : W * 0.55;
      if (L.shade_title) { c.text(0, 12, L.shade_title, { role: 'eyebrow', weight: 700, fill: 'secondary', max: kw }); }
      var tb = L.shade_title ? c.texts[c.texts.length - 1] : { y: 0, h: 0 };
      var sx = 0, sy = Math.ceil(tb.y + tb.h) + (L.nation_label ? 24 : 10), sw = c.phone ? (W - 10) / 5 : Math.min(46, (kw - 10) / 5);
      for (var i = 1; i <= 5; i++) c.rect(sx + (i - 1) * sw, sy, sw, 12, { fill: 'seq-' + i, mark: false });
      bins.forEach(function (b, i) { c.text(sx + (i + 1) * sw, sy + 28, K.fmt(b, f.bins || 'integer'), { role: 'tick', anchor: 'middle' }); });
      if (L.nation !== undefined && bins.length) {
        var lo = bins[0] - (bins[1] - bins[0]), hi = bins[bins.length - 1] + (bins[1] - bins[0]);
        var nx = sx + 5 * sw * (L.nation - lo) / (hi - lo);
        c.line(nx, sy - 4, nx, sy + 16, { stroke: 'label', width: c.t('line-baseline'), mark: false });
        if (L.nation_label) c.text(Math.max(nx, c.measure(L.nation_label, 'tick', 600) / 2), sy - 8, L.nation_label, { role: 'tick', weight: 600, anchor: 'middle' });
      }
      c.key([1, 2, 3, 4, 5].map(function (i) { return { fill: 'seq-' + i, ordered: true, outline: true }; }));   // circles carry an outline
      var steps = L.size_steps || [];
      var szx = c.phone ? 0 : W * 0.62, szy = c.phone ? sy + 48 : 12;
      if (L.size_title) c.text(szx, szy, L.size_title, { role: 'eyebrow', weight: 700, fill: 'secondary' });
      var cx = szx, base = szy + 14 + 2 * area(steps.length ? steps[steps.length - 1] : maxv);
      steps.forEach(function (s, si) {
        var r = area(s), lab = (L.size_step_words || [])[si] || (K.fmt(s, f.size_step || 'integer') + (L.size_unit ? ' ' + L.size_unit : '')), lw = c.measure(lab, 'tick');
        var mid = cx + Math.max(r, lw / 2);
        c.circle(mid, base - r, r, { stroke: 'label', width: c.t('bubble-outline'), mark: false });
        c.text(mid, base + 16, lab, { role: 'tick', anchor: 'middle' });
        cx = mid + Math.max(r, lw / 2) + 14;
      });
      var ring = L.ring || [];
      if (L.ring_label) {
        var ry = c.phone ? base + 34 : sy + 50;
        c.circle(7, ry - 4, 6, { stroke: 'label', width: c.t('bubble-ring'), mark: false });
        c.text(20, ry, L.ring_label, { role: 'tick', max: c.phone ? W - 24 : kw - 24 });
        y = ry + 26;
      } else y = Math.max(sy + 48, base + 26);
      y = Math.max(y, base + 30);
      // the map in its 975 by 610 frame, scaled to the width
      var k = W / G.frame[0], top = y, mh = G.frame[1] * k;
      var tf = 'translate(0,' + K.round(top) + ') scale(' + Math.round(k * 10000) / 10000 + ')';
      var g = c.group({ transform: tf });
      c.path(G.land, { fill: 'land', mark: false });
      c.path(G.borders, { stroke: 'surface', width: 1, mark: false });
      g.end();
      // circles: start at the centers, then push apart where they overlap (a fixed number of passes, so every run matches)
      var pts = drawn.map(function (r) {
        var p = G.centers[r[ec]];
        return { r: r, x: p[0] * k, y: top + p[1] * k, rad: area(r[ez]), x0: p[0] * k, y0: top + p[1] * k };
      }).sort(function (a, b) { return b.rad - a.rad; });
      var pad = c.t('bubble-gap');
      for (var pass = 0; pass < 120; pass++) {
        var moved = false;
        for (var a = 0; a < pts.length; a++) for (var b = a + 1; b < pts.length; b++) {
          var A = pts[a], B = pts[b], dx = B.x - A.x, dy = B.y - A.y, d = Math.sqrt(dx * dx + dy * dy) || 0.01, need = A.rad + B.rad + pad;
          if (d < need) {
            var push = (need - d) / 2, ux = dx / d, uy = dy / d;
            A.x -= ux * push * 0.5; A.y -= uy * push * 0.5; B.x += ux * push * 1.5; B.y += uy * push * 1.5;
            moved = true;
          }
        }
        if (!moved) break;
      }
      // every circle stays inside the artboard
      pts.forEach(function (p) { p.x = Math.max(p.rad + 1, Math.min(W - p.rad - 1, p.x)); });
      var shade = function (v) { var s = 1; bins.forEach(function (b) { if (v >= b) s++; }); return 'seq-' + Math.min(5, s); };
      pts.forEach(function (p) {
        var sh = shade(p.r[eh]);
        c.circle(p.x, p.y, p.rad, { fill: sh, area_of: { value: p.r[ez], max_value: maxv, max_radius: R }, data: { key: p.r[ec], field: ez, value: p.r[ez], shade: p.r[eh] } });
        c.circle(p.x, p.y, p.rad, { stroke: 'sequential-outline', width: c.t('bubble-outline'), mark: false });
        if (ring.indexOf(p.r[ec]) >= 0) c.circle(p.x, p.y, p.rad + 3, { stroke: 'label', width: c.t('bubble-ring'), mark: false });
      });
      // labels: inside a circle that holds one; else the first of right, left, above, below that touches no text or circle
      var hits = function (b) {
        if (b.x < 0 || b.x + b.w > W) return true;
        if (c.texts.some(function (t) { return b.x < t.x + t.w + 1 && t.x < b.x + b.w + 1 && b.y < t.y + t.h + 1 && t.y < b.y + b.h + 1; })) return true;
        return pts.some(function (q) { var nx = Math.max(b.x, Math.min(q.x, b.x + b.w)), ny = Math.max(b.y, Math.min(q.y, b.y + b.h)); return (nx - q.x) * (nx - q.x) + (ny - q.y) * (ny - q.y) < q.rad * q.rad - 1; });
      };
      var offs = (c.phone && L.offsets_phone) || L.offsets || {};
      var fits = function (p) { return p.rad * 2 > c.measure(p.r[ec], 'tick', 700) + 6 && !offs[p.r[ec]]; };
      // a label goes inside its circle, largest circles first, unless it would touch a label already placed or leave the artboard
      var outside = [], lead = [], unlabeled = [];
      pts.slice().sort(function (a, b) { return b.rad - a.rad; }).forEach(function (p) {
        if (!fits(p)) { outside.push(p); return; }
        var s = c.size('tick'), tw = c.measure(p.r[ec], 'tick', 700), b = { x: p.x - tw / 2, y: p.y + s * 0.35 - s * 0.77, w: tw, h: s };
        var clash = b.x < 0 || b.x + b.w > W || c.texts.some(function (t) { return b.x < t.x + t.w + 1 && t.x < b.x + b.w + 1 && b.y < t.y + t.h + 1 && t.y < b.y + b.h + 1; });
        if (clash) { outside.push(p); return; }
        var sh = shade(p.r[eh]);
        c.text(p.x, p.y + s * 0.35, p.r[ec], { role: 'tick', weight: 700, anchor: 'middle', fill: sh === 'seq-4' || sh === 'seq-5' ? 'label-on-subject' : 'label' });
      });
      outside.sort(function (a, b) { return a.rad - b.rad; }).forEach(function (p) {
        var code = p.r[ec], s = c.size('tick'), tw = c.measure(code, 'tick', 700);
        var pad = c.t('bubble-label-pad') + 1, asc = s * 0.77, h = s;
        var cands = offs[code] ? [[p.x + offs[code][0], p.y + offs[code][1]]] : [[p.x + p.rad + pad, p.y + s * 0.35], [p.x - p.rad - pad - tw, p.y + s * 0.35], [p.x - tw / 2, p.y - p.rad - pad - s * 0.23], [p.x - tw / 2, p.y + p.rad + pad + asc],
          [p.x + p.rad + pad, p.y - p.rad], [p.x + p.rad + pad, p.y + p.rad + asc], [p.x - p.rad - pad - tw, p.y - p.rad], [p.x - p.rad - pad - tw, p.y + p.rad + asc]];
        for (var ring = 1; ring <= (c.phone ? 14 : 6) && !offs[code]; ring++) {
          var dd = p.rad + pad + ring * 12;
          for (var ang = 0; ang < 24; ang++) {
            var th = ang * Math.PI / 12, ex = p.x + Math.cos(th) * dd, ey = p.y + Math.sin(th) * dd;
            cands.push([Math.cos(th) < -0.1 ? ex - tw : Math.cos(th) > 0.1 ? ex : ex - tw / 2, ey + s * 0.35]);
          }
        }
        // a place is clear when its box touches no text or circle, no leader drawn so far runs through it, and its own
        // leader (when it needs one) runs through no label (D3-93)
        var leads_ok = function (b, cand) {
          if (lead.some(function (l) { return K.seg_hits_box(l[0], l[1], l[2], l[3], b.x - 1, b.y - 1, b.x + b.w + 1, b.y + b.h + 1); })) return false;
          var lx = cand[0] + tw / 2, ly = cand[1] - asc / 2;
          if (Math.sqrt(Math.pow(lx - p.x, 2) + Math.pow(ly - p.y, 2)) <= p.rad + 2 * s) return true;
          return !c.texts.some(function (t) { return K.seg_hits_box(p.x, p.y, lx, ly, t.x - 1, t.y - 1, t.x + t.w + 1, t.y + t.h + 1); });
        };
        var pick = null;
        for (var i = 0; i < cands.length && !pick; i++) { var b = { x: cands[i][0], y: cands[i][1] - asc, w: tw, h: h }; if (!hits(b) && leads_ok(b, cands[i])) pick = cands[i]; }
        // on a phone, a small state with no clear place is named under the map instead, and the table names every state
        if (!pick && c.phone && !offs[code]) { unlabeled.push(code); return; }
        if (!pick) { pick = cands[0]; c.warn('no clear place for the label ' + code + '; set labels.offsets.' + code); }
        var far = Math.sqrt(Math.pow(pick[0] + tw / 2 - p.x, 2) + Math.pow(pick[1] - asc / 2 - p.y, 2)) > p.rad + 2 * s;
        c.text(pick[0], pick[1], code, { role: 'tick', weight: 600, halo: true });
        if (far) { c.line(p.x, p.y, pick[0] + tw / 2, pick[1] - asc / 2, { stroke: 'leader', width: c.t('line-hairline'), mark: false }); lead.push([p.x, p.y, pick[0] + tw / 2, pick[1] - asc / 2]); }
      });
      c.height(top + mh + 4);
      if (unlabeled.length) {
        var uw = (K.words && K.words.unlabeled_marks) || 'Not labeled at this width: {codes}.';
        var low = top + mh;
        c.texts.forEach(function (t) { low = Math.max(low, t.y + t.h); });
        pts.forEach(function (q) { low = Math.max(low, q.y + q.rad); });
        c.text(0, low + 22, uw.replace('{codes}', unlabeled.sort().join(', ')), { role: 'note', max: W, fill: 'secondary' });
      }
    }
  });
})(globalThis.OAChart);
