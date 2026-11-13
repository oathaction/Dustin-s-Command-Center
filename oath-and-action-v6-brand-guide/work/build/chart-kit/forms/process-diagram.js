/* Process diagram (coverage plan 3.11, core; S66). The steps every case takes, numbered in order down a heavy line in
 * the subject ink, and beside them the branches some cases take or the ways in and out, each in a box with a fine edge
 * and a short line that says when it applies, joined to the step it leaves or enters by a fine line with an arrowhead.
 * Desk: the steps in a column at the left, each step's branches stacked beside it at the right. Narrower than two
 * columns of 200 px, one column: a step's ways in sit above it and its branches below it, set in from the line.
 * The table lists the steps in this reading order (sort by the key with its values), each link named in a column.
 * encode: key (integer: the step's key), path (category: main steps take labels.main), step (text: the name),
 * who (text, optional: who acts), limit (text, optional: the time the law sets).
 * labels: main (the path value of the steps every case takes, default "main"), branches ({key: {at: the main step's
 * key, dir: "out" or "in", words: the line that says when it applies}}), named (branch keys the title names: a 2 px
 * edge and link in the subject ink). */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'process-diagram', name: 'Process Diagram', family: 'structure',
    encode: { key: 'integer', path: 'category', step: 'text', who: 'text?', limit: 'text?' },
    labels: ['main', 'branches', 'named'],
    phone: 'differs',
    draw: function (c) {
      var L = c.labels, W = c.width, ek = c.field('key'), ep = c.field('path'), es = c.field('step');
      var ew = c.field('who', false), el = c.field('limit', false), B = L.branches || {}, named = (L.named || []).map(String);
      var main = c.rows.filter(function (r) { return String(r[ep]) === String(L.main || 'main'); }).sort(function (a, b) { return a[ek] - b[ek]; });
      var pad = 10, chip = 22, gap = 12, lane = 40, wide = W >= 2 * 200 + lane, sz = c.size('label');
      // words set here once, by the spec's typography or the guide's own (curly quotes, held dates), so Node and the page,
      // whose rows may arrive unset, print and measure the same words
      var ty = function (w) { return K.typeset({ typography: c.spec.typography || { curl_quotes: true, nbsp: true } }, String(w).replace(/[ \t\n]+/g, ' ')); };
      // a box's words: the branch's line, the name in bold (after the step's number), who acts, and the time limit
      var parts = function (r, n) {
        var p = [], b = B[String(r[ek])];
        if (b && b.words) p.push({ w: b.words, role: 'tick', wt: 600, fill: 'secondary' });
        p.push({ w: r[es], role: 'label', wt: 700, ind: n ? chip + 8 : 0 });
        if (ew && r[ew]) p.push({ w: r[ew], role: 'tick', wt: 400, fill: 'secondary' });
        if (el && r[el]) p.push({ w: r[el], role: 'tick', wt: 400, fill: 'label' });
        p.forEach(function (q) { q.w = ty(q.w); });
        return p;
      };
      var fit = function (p, w) {
        var y = pad;
        p.forEach(function (q, i) {
          var s = c.size(q.role), lh = Math.round(s * 1.3), lines = c.wrap(ty(q.w), q.role, w - 2 * pad - (q.ind || 0), q.wt);
          if (i) y += 4;
          q.base = y + s * 0.93; q.lh = lh; q.max = w - 2 * pad - (q.ind || 0);
          if (q.ind) q.base = Math.max(q.base, pad + chip / 2 + 5);
          y = q.base + (lines.length - 1) * lh + s * 0.3;
        });
        return Math.ceil(y + pad);
      };
      var heavy = function (r) { return String(r[ep]) === String(L.main || 'main') || named.indexOf(String(r[ek])) >= 0; };
      var box = function (r, x, y, w, h, n, p) {
        var hv = heavy(r);
        c.rect(x + 0.5, y + 0.5, w - 1, h - 1, { fill: 'surface', stroke: hv ? 'subject' : 'context', width: 1, data: { key: String(r[ek]), field: 'step', value: r[es] } });
        if (n) {
          c.rect(x + pad, y + pad, chip, chip, { fill: 'subject', data: { key: String(r[ek]), field: 'number', value: n } });
          c.text(x + pad + chip / 2, y + pad + chip / 2 + 4.6, String(n), { role: 'tick', weight: 700, anchor: 'middle', fill: 'label-on-subject' });
        }
        p.forEach(function (q) {
          c.text(x + pad + (q.ind || 0), y + q.base, q.w, { role: q.role, weight: q.wt, max: q.max, leading: q.lh, fill: q.fill });
        });
      };
      // a link along its points through the kit's link part, one straight run a segment, the head on the last (R3-5)
      var link = function (pts, r) {
        var hv = r ? heavy(r) : true, o = { stroke: hv ? 'subject' : 'context', width: hv ? 2 : 1, head: [7, 4] };
        for (var i = 1; i < pts.length; i++) {
          K.parts.link(c, { x: pts[i - 1][0], y: pts[i - 1][1] }, { x: pts[i][0], y: pts[i][1] }, Object.assign({ arrow: i === pts.length - 1 }, o));
        }
      };
      var n = 0, y = 0, prev = null, spine = 15;
      main.forEach(function (m) {
        n++;
        var mk = String(m[ek]);
        var brs = c.rows.filter(function (r) { var b = B[String(r[ek])]; return b && String(b.at) === mk; }).sort(function (a, b) {
          var da = B[String(a[ek])].dir === 'in' ? 0 : 1, db = B[String(b[ek])].dir === 'in' ? 0 : 1; return da - db || a[ek] - b[ek];
        });
        var ins = brs.filter(function (r) { return B[String(r[ek])].dir === 'in'; }), outs = brs.filter(function (r) { return B[String(r[ek])].dir !== 'in'; });
        if (wide) {
          var mw = Math.floor((W - lane) / 2), bx = mw + lane, bw = W - bx, mp = parts(m, n), mh = fit(mp, mw);
          var bp = brs.map(function (r) { return parts(r, 0); }), bh = bp.map(function (p) { return fit(p, bw); });
          var top = y;
          if (prev) link([[spine, prev], [spine, top]], null);
          box(m, 0, top, mw, mh, n, mp);
          var by = top, ys = [];
          brs.forEach(function (r, i) { box(r, bx, by, bw, bh[i], 0, bp[i]); ys.push(by + Math.min(22, bh[i] / 2)); by += bh[i] + gap; });
          ins.forEach(function (r, i) { link([[bx, ys[i]], [mw, ys[i]]], r); });
          if (outs.length) {
            var oi = ins.length, sy = Math.max(top + 14, Math.min(ys[oi], top + mh - 14)), lx = mw + lane / 2;
            outs.forEach(function (r, i) {
              var yb = ys[oi + i];
              link(Math.abs(yb - sy) < 0.5 ? [[mw, sy], [bx, yb]] : [[mw, sy], [lx, sy], [lx, yb], [bx, yb]], r);
            });
          }
          prev = top + mh;
          y = Math.max(top + mh, by - gap) + 28;
        } else {
          // one column: ways in above the step, branches below it, set in from the line
          var ind = 28, iw = W - ind;
          ins.forEach(function (r) {
            var p = parts(r, 0), h = fit(p, iw);
            box(r, ind, y, iw, h, 0, p);
            var ly = y + Math.min(22, h / 2);
            if (prev) link([[spine, prev], [spine, y + h + 6]], null);
            prev = null;
            link([[ind, ly], [spine, ly], [spine, y + h + 20]], r);
            y += h + 20;
          });
          var mp2 = parts(m, n), mh2 = fit(mp2, W);
          if (prev) link([[spine, prev], [spine, y]], null);
          box(m, 0, y, W, mh2, n, mp2);
          var yy = y + mh2;
          outs.forEach(function (r, i) {
            var p = parts(r, 0), h = fit(p, iw), top2 = yy + (i ? gap : 16), ly = top2 + Math.min(22, h / 2);
            box(r, ind, top2, iw, h, 0, p);
            K.parts.link(c, { x: spine, y: yy }, { x: spine, y: ly }, { stroke: 'subject', width: 2 });
            link([[spine, ly], [ind, ly]], r);
            yy = top2 + h;
          });
          prev = y + mh2;
          y = yy + 28;
        }
      });
      c.height(y - 28);
    }
  });
})(globalThis.OAChart);
