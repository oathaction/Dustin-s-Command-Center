/* Locator map (coverage plan 3.14, core; S79). Where a story takes place: the place the title names as the view's one red
 * point with its keyline, a second place in the text's ink for scale, its county in the light fill with a context edge,
 * the state's other counties in the track ink, neighboring states as ghost lines cut at the view's thin frame, a scale bar,
 * and a small United States inset in a frame with the state in the light fill and the view drawn on it.
 * encode: name (text), lon (number), lat (number).
 * labels: layer (a fitted county layer, 'counties-ca'), state (the state's two-digit code), county (the county's geoid),
 * county_label, state_label, point (the name value of the red point), names ({name value: words to print}),
 * neighbors ([{words, lon, lat}]: names of neighboring states, printed where their point falls in the view). */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'locator-map', name: 'Locator Map', family: 'maps',
    encode: { name: 'text', lon: 'number', lat: 'number' },
    labels: ['layer', 'state', 'county', 'county_label', 'state_label', 'point', 'names', 'neighbors'],
    phone: 'same',
    draw: function (c) {
      var L = c.labels, W = c.width, en = c.field('name'), elo = c.field('lon'), ela = c.field('lat');
      var C = K.geo(L.layer), S = K.geo('states'), desk = W >= 560;
      var vw = desk ? Math.round(W * 0.56) : W, vh = desk ? 560 : Math.round(W * 1.45);
      // C-S5, BC-S6 (round 3 fix pass): the view sits in a thin frame, so the neighbors' lines end at a drawn edge
      var FP = 8, T = K.parts.map_fit(c, C, { x: FP, y: FP, w: vw - 40 - FP, max_h: vh - 2 * FP });
      var box = { x0: 0, y0: 0, x1: vw, y1: T.h + 2 * FP };
      // the states layer in this view: the county layer's frame is the base projection fitted (L.fit)
      var f = C.fit || [1, 0, 0], TS = { k: T.k * f[0], ox: T.ox + T.k * f[1], oy: T.oy + T.k * f[2] };
      // neighboring states: their lines, cut at the view's edge, every line the state does not share
      var R = K.round, d = '', subs = [], st = S.index[L.state];
      S.arcs.forEach(function (pts, ai) {
        if (S.use[ai].indexOf(st) >= 0) return;
        var run = [];
        var flush = function () { if (run.length > 1) { d += 'M' + run.map(function (p) { return R(p[0]) + ',' + R(p[1]); }).join('L'); subs.push(run); } run = []; };
        var inside = function (p) { return p[0] >= box.x0 && p[0] <= box.x1 && p[1] >= box.y0 && p[1] <= box.y1; };
        var cut = function (a, b) {   // where the segment from a (inside) to b (outside) leaves the box
          var t = 1;
          if (b[0] < box.x0) t = Math.min(t, (box.x0 - a[0]) / (b[0] - a[0]));
          if (b[0] > box.x1) t = Math.min(t, (box.x1 - a[0]) / (b[0] - a[0]));
          if (b[1] < box.y0) t = Math.min(t, (box.y0 - a[1]) / (b[1] - a[1]));
          if (b[1] > box.y1) t = Math.min(t, (box.y1 - a[1]) / (b[1] - a[1]));
          return [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t];
        };
        var prev = null;
        pts.forEach(function (q) {
          var p = [TS.ox + q[0] * TS.k, TS.oy + q[1] * TS.k];
          if (inside(p)) { if (prev && !inside(prev)) run.push(cut(p, prev)); run.push(p); }
          else if (prev && inside(prev)) { run.push(cut(prev, p)); flush(); }
          prev = p;
        });
        flush();
      });
      if (d) c.path(d, { fill: 'none', stroke: 'ghost', width: 1, pts: subs, closed: false, mark: false });
      c.rect(box.x0 + 0.5, box.y0 + 0.5, box.x1 - box.x0 - 1, box.y1 - box.y0 - 1, { stroke: 'gridline', width: 1, mark: false });
      // the state's counties, its county in the light fill
      K.parts.map_shapes(c, C, T, C.ids.map(function (id) { return { id: id, fill: id === L.county ? 'light-fill' : 'track' }; }));
      K.parts.map_mesh(c, C, T, { stroke: 'surface', width: 1 });
      K.parts.map_mesh(c, C, T, { which: 'outline', stroke: 'context', width: 1 });
      K.parts.map_mesh(c, C, T, { which: 'all', between: function (a, b) { return a === L.county || b === L.county; }, stroke: 'context', width: 1 });
      // names of the state and its neighbors, in the secondary ink, where their points fall in the view
      var named = [];
      (L.neighbors || []).forEach(function (n) {
        var p = T.pt(K.geo.project(C, n.lon, n.lat));
        var b = c.text_box(p[0], p[1], n.words, { role: 'tick', anchor: 'middle' });
        if (b.x >= 0 && b.x + b.w <= box.x1 && b.y >= 0 && b.y + b.h <= box.y1) c.text(p[0], p[1], n.words, { role: 'tick', anchor: 'middle', fill: 'secondary', halo: true });
      });
      // the places: the red point with its keyline, the other in the text's ink
      var pts = c.rows.map(function (r) {
        var p = T.pt(K.geo.project(C, r[elo], r[ela])), red = r[en] === L.point;
        var o = { data: { key: r[en], field: ela, value: r[ela] } };
        if (red) { o.fill = 'point'; o.job = 'point'; if (c.ground !== 'charcoal') { o.stroke = 'point-keyline'; o.width = c.t('keyline'); } }
        else o.fill = 'label';
        c.circle(p[0], p[1], red ? 5 : 2.5, o);
        return { x: p[0], y: p[1], r: red ? 5 : 2.5, words: (L.names || {})[r[en]] || r[en], weight: red ? 700 : 400, red: red };
      });
      // the county's name inside it, at the middle of its largest ring, clear of the places
      var fi = C.index[L.county], ring = C.rings(fi).map(function (rs) { return rs[0]; }).sort(function (a, b) { return b.length - a.length; })[0];
      var cx = 0, cy = 0; ring.forEach(function (q) { cx += q[0]; cy += q[1]; }); cx /= ring.length; cy /= ring.length;
      var cp = T.pt([cx, cy]), polys = C.rings(fi).map(function (rs) { return rs.map(function (r) { return r.map(T.pt); }); });
      // the county's name inside it where its box clears every edge and the places; else under the county on the ground's halo
      var kpick = null, krole = 'label';
      ['label', 'tick'].forEach(function (role) { [[0, 0], [0, 10], [0, -10], [0, 18], [0, -18], [0, 26], [-12, 8], [12, 8], [-12, 16], [12, 16], [-12, -8], [12, -8]].forEach(function (o) {
        if (kpick) return;
        var kb = c.text_box(cp[0] + o[0], cp[1] + o[1], L.county_label, { role: role, weight: 600, anchor: 'middle' });
        var g = { x: kb.x - 2, y: kb.y - 2, w: kb.w + 4, h: kb.h + 4 };
        var corners = [[g.x, g.y], [g.x + g.w, g.y], [g.x, g.y + g.h], [g.x + g.w, g.y + g.h]];
        var fits = polys.some(function (rs) {
          if (!corners.every(function (q) { return K.in_poly(rs, q[0], q[1]); })) return false;
          return !rs.some(function (r) { for (var i = 0; i < r.length; i++) { var p1 = r[i], p2 = r[(i + 1) % r.length]; if (K.seg_hits_box(p1[0], p1[1], p2[0], p2[1], g.x, g.y, g.x + g.w, g.y + g.h)) return true; } return false; });
        });
        var clear = pts.every(function (p) { return p.x + p.r + 4 < g.x || p.x - p.r - 4 > g.x + g.w || p.y + p.r + 4 < g.y || p.y - p.r - 4 > g.y + g.h; });
        if (fits && clear) { kpick = [cp[0] + o[0], cp[1] + o[1]]; krole = role; }
      }); });
      // else anywhere inside the county clear of its edges and the places, nearest its middle (C-S5: its lower right at
      // a desk), searched on a 2 px grid
      var fits_at = function (g) {
        var corners = [[g.x, g.y], [g.x + g.w, g.y], [g.x, g.y + g.h], [g.x + g.w, g.y + g.h]];
        return polys.some(function (rs) {
          if (!corners.every(function (q) { return K.in_poly(rs, q[0], q[1]); })) return false;
          return !rs.some(function (r) { for (var i = 0; i < r.length; i++) { var p1 = r[i], p2 = r[(i + 1) % r.length]; if (K.seg_hits_box(p1[0], p1[1], p2[0], p2[1], g.x, g.y, g.x + g.w, g.y + g.h)) return true; } return false; });
        });
      };
      var kbx = [Infinity, Infinity, -Infinity, -Infinity];
      polys.forEach(function (rs) { rs[0].forEach(function (q) { kbx[0] = Math.min(kbx[0], q[0]); kbx[1] = Math.min(kbx[1], q[1]); kbx[2] = Math.max(kbx[2], q[0]); kbx[3] = Math.max(kbx[3], q[1]); }); });
      var klines = [L.county_label], ksp = String(L.county_label).lastIndexOf(' ');
      [['label', 1], ['tick', 1], ['tick', 2]].forEach(function (rl) {
        if (kpick) return;
        var role = rl[0], two = rl[1] === 2 && ksp > 0, ws = two ? [L.county_label.slice(0, ksp), L.county_label.slice(ksp + 1)] : [L.county_label];
        var bs = ws.map(function (w) { return c.text_box(0, 0, w, { role: role, weight: 600, anchor: 'middle' }); }), lh2 = Math.round(c.size(role) * 1.2);
        var kb0 = { w: Math.max.apply(null, bs.map(function (b) { return b.w; })), h: bs[0].h + (ws.length - 1) * lh2, y: bs[0].y }, best = null;
        for (var gx = kbx[0] + kb0.w / 2; gx <= kbx[2] - kb0.w / 2; gx += 2) for (var gy = kbx[1]; gy <= kbx[3]; gy += 2) {
          var g = { x: gx - kb0.w / 2 - 2, y: gy + kb0.y - 2, w: kb0.w + 4, h: kb0.h + 4 };
          if (!pts.every(function (p) { return p.x + p.r + 4 < g.x || p.x - p.r - 4 > g.x + g.w || p.y + p.r + 4 < g.y || p.y - p.r - 4 > g.y + g.h; })) continue;
          if (!fits_at(g)) continue;
          var dd = Math.hypot(gx - cp[0], gy - cp[1]);
          if (!best || dd < best[2]) best = [gx, gy, dd];
        }
        if (best) { kpick = [best[0], best[1]]; krole = role; klines = ws; kpick.lh = lh2; }
      });
      var kt;
      var kts = [];
      if (kpick) {
        klines.forEach(function (w, li) { kts.push(c.text(kpick[0], kpick[1] + li * (kpick.lh || 0), w, { role: krole, weight: 600, anchor: 'middle' })); });
        kt = kts[0];
      }
      else {
        var lowest = 0; polys.forEach(function (rs) { rs[0].forEach(function (q) { lowest = Math.max(lowest, q[1]); }); });
        kt = c.text(cp[0], lowest + 16, L.county_label, { role: 'label', weight: 600, anchor: 'middle', halo: true });
      }
      var pl = K.parts.place_labels(c, pts.map(function (p) { return { x: p.x, y: p.y, r: p.r, words: p.words, weight: p.weight }; }), { role: 'label', reach: [8, 18, 30], avoid: kts.length ? kts : [kt] });
      if (pl.unplaced.length) c.warn('places with no room for a name: ' + pl.unplaced.map(function (u) { return u.words; }).join(', '));
      if (L.state_label) {
        var sp = T.pt(K.geo.project(C, -120.6, 38.6));
        c.text(sp[0], sp[1], L.state_label, { role: 'label', weight: 600, anchor: 'middle', halo: true });
      }
      // the scale, under the state at its left
      var sb = K.parts.map_scale(c, C, T, 8 + FP, T.y + T.h - 22);
      var low = box.y1;
      // the inset: the United States in a frame, the state in the light fill, the view drawn on it
      var ix = desk ? vw + 24 : 0, iy = desk ? 0 : low + 16, iw = desk ? W - vw - 24 : Math.min(W, 240);
      var TI = K.parts.map_fit(c, S, { x: ix, y: iy, w: iw, pad: 6 });
      c.rect(ix + 0.5, iy + 0.5, TI.w - 1, TI.h - 1, { stroke: 'gridline', width: 1, mark: false });
      K.parts.map_shapes(c, S, TI, S.ids.map(function (id) { return { id: id, fill: id === L.state ? 'light-fill' : 'track' }; }));
      K.parts.map_mesh(c, S, TI, { stroke: 'surface', width: 0.5 });
      K.parts.map_mesh(c, S, TI, { which: 'outline', stroke: 'context', width: 1 });   // D3-1100: the land's edge carries on both grounds
      K.parts.map_mesh(c, S, TI, { which: 'all', between: function (a, b) { return a === L.state || b === L.state; }, stroke: 'context', width: 1 });
      var back = function (vx, vy) { var q = [((vx - T.ox) / T.k - f[1]) / f[0], ((vy - T.oy) / T.k - f[2]) / f[0]]; return [TI.ox + q[0] * TI.k, TI.oy + q[1] * TI.k]; };
      var a = back(box.x0, box.y0), b2 = back(box.x1, box.y1);
      c.rect(a[0], a[1], b2[0] - a[0], b2[1] - a[1], { stroke: 'label', width: 1, mark: false });
      low = Math.max(low, iy + TI.h);
      c.texts.forEach(function (t) { low = Math.max(low, t.y + t.h); });
      c.height(low + 4);
    }
  });
})(globalThis.OAChart);
