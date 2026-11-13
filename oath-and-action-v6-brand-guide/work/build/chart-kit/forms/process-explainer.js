/* Process explainer (coverage plan 3.16, core; S89). The steps of a public process and who acts at each one. At a desk,
 * one lane a level of government (or the public), named in words at its head, and each step a box set across the lanes
 * of those who act at it, numbered in reading order down the page and joined by arrows in the subject ink, so a reader
 * scans a lane to see where its level acts. A step that some cases take in place of another sits under it, edged in the
 * context ink with a line that says when it applies, and joins the path where that step does. Steps that follow one step
 * side by side share a row (labels.together), each joined to it by its own arrow. Where the lanes cannot each hold
 * labels.lane_min px, one column: the steps down a heavy line, the step taken in place of another set in under it.
 * Actors are named in words (Rule 10.6); no symbol stands for an actor.
 * The table lists the steps in reading order (sort by the key with its values), each link named in a column (R3-6).
 * encode: key (integer: the step's key), path (category: main steps take labels.main), step (text: the name), level
 * (text: the levels that act, "; " between), who (text, optional: who acts), limit (text, optional: the time the law sets).
 * labels: main (default "main"), lanes ([{levels: [level, ...], label, share, min (px: the lane's least width)}]), branches ({key: {at: the key of the step
 * it replaces, words}}), together ([[key, key], ...]: steps in one row, left to right), lines ({key: words over the
 * step's name}), named (keys the title names: a 2 px edge in the subject ink), lane_min (px, default 150), limit_words
 * (the words a limit prints in, {limit} for the column's words; default "{limit}"). Main steps take a 1.5 px edge. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'process-explainer', name: 'Process Explainer', family: 'infographics',
    encode: { key: 'integer', path: 'category', step: 'text', level: 'text', who: 'text?', limit: 'text?' },
    labels: ['main', 'lanes', 'branches', 'together', 'lines', 'named', 'lane_min', 'limit_words'],
    phone: 'differs',
    draw: function (c) {
      var L = c.labels, W = c.width, ek = c.field('key'), ep = c.field('path'), es = c.field('step'), ev = c.field('level');
      var ew = c.field('who', false), el = c.field('limit', false), B = L.branches || {}, lines = L.lines || {};
      var named = (L.named || []).map(String), lanes = L.lanes || [], mv = String(L.main || 'main');
      var pad = 10, chip = 22, gap = 12, g = 8, rowgap = 30, k = function (r) { return String(r[ek]); };
      var ty = function (w) { return K.typeset({ typography: c.spec.typography || { curl_quotes: true, nbsp: true } }, String(w).replace(/[ \t\n]+/g, ' ')); };
      var main = c.rows.filter(function (r) { return String(r[ep]) === mv; });
      var num = {}; main.forEach(function (r, i) { num[k(r)] = i + 1; });
      // lane geometry: shares of the width less the gutters
      var tot = lanes.reduce(function (s, l) { return s + (l.share || 1); }, 0), avail = W - g * Math.max(0, lanes.length - 1), lx = [], lw = [], x = 0;
      lanes.forEach(function (l) { var w = avail * (l.share || 1) / (tot || 1); lx.push(x); lw.push(w); x += w + g; });
      var wide = lanes.length > 1 && !c.phone && lw.every(function (w, i) { return w >= (lanes[i].min || L.lane_min || 150); });
      var span = function (r) {
        var ix = [];
        String(r[ev] || '').split(/;\s*/).forEach(function (v) { lanes.forEach(function (l, i) { if ((l.levels || []).indexOf(v.trim()) >= 0) ix.push(i); }); });
        if (!ix.length) { c.warn('process-explainer: step ' + k(r) + ' names no lane'); ix = [0]; }
        var a = Math.min.apply(null, ix), b = Math.max.apply(null, ix);
        return { x: lx[a], w: lx[b] + lw[b] - lx[a] };
      };
      // a box's words: the line over the name, the name in bold after its number, who acts, then the time the law sets
      var words = function (r) {
        var p = [], key = k(r), b = B[key], n = num[key], lw2 = (b && b.words) || lines[key];
        if (lw2) p.push({ w: lw2, role: 'tick', wt: 600, fill: 'secondary' });
        p.push({ w: r[es], role: 'label', wt: 700, ind: n ? chip + 8 : 0 });
        if (ew && r[ew]) p.push({ w: r[ew], role: 'tick', wt: 400, fill: 'secondary' });
        if (el && r[el]) p.push({ w: String(L.limit_words || '{limit}').split('{limit}').join(r[el]), role: 'tick', wt: 400, fill: 'label' });
        p.forEach(function (q) { q.w = ty(q.w); });
        return p;
      };
      var fit = function (p, w) {
        var y = pad;
        p.forEach(function (q, i) {
          var s = c.size(q.role), lh = Math.round(s * 1.3), n = c.wrap(q.w, q.role, w - 2 * pad - (q.ind || 0), q.wt).length;
          if (i) y += 4;
          q.base = y + s * 0.93; q.lh = lh; q.max = w - 2 * pad - (q.ind || 0);
          if (q.ind) q.base = Math.max(q.base, pad + chip / 2 + 5);
          y = q.base + (n - 1) * lh + s * 0.3;
        });
        return Math.ceil(y + pad);
      };
      var heavy = function (r) { return String(r[ep]) === mv; };
      var box = function (r, b) {
        var hv = heavy(r), sw = named.indexOf(k(r)) >= 0 ? 2 : hv ? 1.5 : 1;
        c.rect(b.x + sw / 2, b.y + sw / 2, b.w - sw, b.h - sw, { fill: 'surface', stroke: hv ? 'subject' : 'context', width: sw, data: { key: k(r), field: 'step', value: r[es] } });
        var n = num[k(r)];
        if (n) {
          var cy = b.y + b.p.filter(function (q) { return q.ind; })[0].base - 5 - chip / 2;
          c.rect(b.x + pad, cy, chip, chip, { fill: 'subject', data: { key: k(r), field: 'number', value: n } });
          c.text(b.x + pad + chip / 2, cy + chip / 2 + 4.6, String(n), { role: 'tick', weight: 700, anchor: 'middle', fill: 'label-on-subject' });
        }
        b.p.forEach(function (q) { c.text(b.x + pad + (q.ind || 0), b.y + q.base, q.w, { role: q.role, weight: q.wt, max: q.max, leading: q.lh, fill: q.fill }); });
      };
      // a link along its points through the kit's link part, the head on the last run (R3-5)
      var link = function (pts, hv) {
        for (var i = 1; i < pts.length; i++) {
          K.parts.link(c, { x: pts[i - 1][0], y: pts[i - 1][1] }, { x: pts[i][0], y: pts[i][1] }, { arrow: i === pts.length - 1, stroke: hv ? 'subject' : 'context', width: hv ? 2 : 1, head: [7, 4] });
        }
      };
      // rows: each main step its own row unless labels.together joins it to others; a branch takes a row under its step
      var rows = [], seen = {};
      var together = (L.together || []).map(function (t) { return t.map(String); });
      main.forEach(function (r) {
        if (seen[k(r)]) return;
        var grp = together.filter(function (t) { return t.indexOf(k(r)) >= 0; })[0] || [k(r)];
        var row = grp.map(function (kk) { return main.filter(function (m) { return k(m) === kk; })[0]; }).filter(Boolean);
        row.forEach(function (m) { seen[k(m)] = true; });
        rows.push({ main: true, items: row });
        c.rows.forEach(function (br) { var b = B[k(br)]; if (b && row.some(function (m) { return String(b.at) === k(m); })) rows.push({ main: false, items: [br], at: String(b.at) }); });
      });
      var y = 0;
      if (wide) {
        // the lanes' heads, a rule under them, and a hairline between lanes the height of the steps
        // the heads share a last baseline, so a head on two lines rises above the others
        var hb = 0, hl = Math.round(c.size('tick') * 1.25), hn = lanes.map(function (l, i) { return c.wrap(ty(l.label || ''), 'tick', lw[i], 700).length; }), hm = Math.max.apply(null, hn);
        lanes.forEach(function (l, i) { hb = Math.max(hb, c.text(lx[i], c.size('tick') * 0.95 + (hm - hn[i]) * hl, ty(l.label || ''), { role: 'tick', weight: 700, fill: 'label', max: lw[i], leading: hl }).bottom); });
        y = Math.ceil(hb + 6);
        var rule_y = y;
        y += 14;
        rows.forEach(function (row) {
          var h = 0;
          row.items.forEach(function (r) { var s = span(r); r._b = { x: s.x, w: s.w, p: words(r) }; r._b.h = fit(r._b.p, s.w); h = Math.max(h, r._b.h); });
          row.items.forEach(function (r) { r._b.y = y; });
          row.y = y; row.h = h;
          y += h + rowgap;
        });
        var bottom = y - rowgap;
        lanes.forEach(function (l, i) { if (i) c.line(lx[i] - g / 2, rule_y, lx[i] - g / 2, bottom, { stroke: 'gridline', width: 1, mark: false }); });
        c.line(0, rule_y, W, rule_y, { stroke: 'label', width: 1, mark: false });
        // links: each main row to the next; a branch from the row before its step and to the row after it
        var mains = rows.filter(function (r) { return r.main; });
        var route = function (a, b, hv, avoid) {
          var A = a._b, Bb = b._b, ax0 = A.x, ax1 = A.x + A.w, bx0 = Bb.x, bx1 = Bb.x + Bb.w;
          var acx = ax0 + A.w / 2, bcx = bx0 + Bb.w / 2, ty0 = A.y + A.h, ty1 = Bb.y, ly = A.y + Math.min(22, A.h / 2);
          var nx = A.w <= Bb.w ? (acx >= bx0 && acx <= bx1 ? acx : null) : (bcx >= ax0 && bcx <= ax1 ? bcx : null);
          if (nx === null && Math.min(ax1, bx1) - Math.max(ax0, bx0) >= 20) nx = (Math.max(ax0, bx0) + Math.min(ax1, bx1)) / 2;
          var blocked = nx !== null && avoid.some(function (o) { var O = o._b; return o !== a && o !== b && nx > O.x && nx < O.x + O.w && O.y > ty0 && O.y < ty1; });
          if (nx !== null && !blocked) return link([[nx, ty0], [nx, ty1]], hv);
          if (nx !== null) {
            // down beside the box in the way, then into the step's side
            var sx = bx0 - g / 2 - 4, iy = Bb.y + Math.min(22, Bb.h / 2);
            return link([[sx, ty0], [sx, iy], [bx0, iy]], hv);
          }
          if (bcx > ax1) return link([[ax1, ly], [bcx, ly], [bcx, ty1]], hv);
          return link([[ax0, ly], [bcx, ly], [bcx, ty1]], hv);
        };
        var all = []; rows.forEach(function (r) { all = all.concat(r.items); });
        rows.forEach(function (row, i) {
          if (row.main) return;
          var at = rows.filter(function (r) { return r.main && r.items.some(function (m) { return k(m) === row.at; }); })[0], mi = mains.indexOf(at);
          if (mi > 0) mains[mi - 1].items.forEach(function (a) { route(a, row.items[0], false, all); });
          if (mi + 1 < mains.length) mains[mi + 1].items.forEach(function (b) { route(row.items[0], b, false, all); });
        });
        mains.forEach(function (row, i) {
          if (!i) return;
          mains[i - 1].items.forEach(function (a) { row.items.forEach(function (b) { route(a, b, true, all); }); });
        });
        all.forEach(function (r) { box(r, r._b); });
        c.height(bottom);
      } else {
        // one column: the steps down a heavy line at the left; a branch set in under the step it replaces
        if (!c.phone) c.arrange('phone');
        var spine = pad + chip / 2, ind = 28, prev = null;
        // steps that share a row, like a branch, are set in from the line, each joined to it by its own arrow
        rows.forEach(function (row) {
          row.items.forEach(function (r) {
            if (row.main && row.items.length < 2) {
              var p = words(r), h = fit(p, W);
              if (prev !== null) link([[spine, prev], [spine, y]], true);
              box(r, { x: 0, y: y, w: W, h: h, p: p });
              prev = y + h; y += h + rowgap;
            } else {
              var p2 = words(r), iw = W - ind, h2 = fit(p2, iw), top = y - rowgap + 16, ly = top + Math.min(22, h2 / 2);
              K.parts.link(c, { x: spine, y: prev }, { x: spine, y: ly }, { stroke: 'subject', width: 2 });
              link([[spine, ly], [ind, ly]], row.main);
              box(r, { x: ind, y: top, w: iw, h: h2, p: p2 });
              prev = ly; y = top + h2 + rowgap;
            }
          });
        });
        c.height(y - rowgap);
      }
    }
  });
})(globalThis.OAChart);
