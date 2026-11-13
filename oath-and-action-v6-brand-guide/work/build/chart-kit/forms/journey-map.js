/* Journey map (coverage plan 3.13, core; S77). A person's path through a public service, step by step: each step a box
 * with its name, then the time the rule allows on a line of its own in the text's ink at the label size, so the limits
 * read first (the data lead's B-S3), then who acts in the tick size, joined in order by arrows; a branch some people take leaves the
 * step it starts from. At a desk the path reads across with the branch under the step it leaves; on a phone the path
 * reads down, and the branch's link runs down the right edge to its box after the last step (labels.across_from px,
 * default 600). Inks (the data lead's round 3 ruling (b)): the path's boxes edged and its arrows in the subject ink; the
 * branch's box edged and its arrow in the context ink, named; no red, since red on a step would code it.
 * encode: step (text), path (category: labels.main marks a step on the path, any other value a branch), key (id: the
 * step's order or key), who (text, optional), limit (text, optional: the rule's time limit).
 * labels: main (default "main"), branch_from (the key of the step a branch leaves; default the first step), sub ('{who}'
 * words under each step's limit; default '{who}'), limits ({key: the limit in words, in place of the limit column}),
 * names ({key: printed name}), across_from (px), branch_label (words over the branch's link).
 * Maker B, round 3. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'journey-map', name: 'Journey Map', family: 'flow',
    encode: { step: 'text', path: 'category', key: 'id', who: 'text?', limit: 'text?' },
    labels: ['main', 'branch_from', 'sub', 'limits', 'names', 'across_from', 'branch_label'],
    phone: 'differs',
    draw: function (c) {
      var P = K.parts, L = c.labels, W = c.width, across = W >= (L.across_from || 600);
      var es = c.field('step'), ep = c.field('path'), ek = c.field('key'), ew = c.field('who', false), el = c.field('limit', false);
      var mv = String(L.main || 'main'), names = L.names || {}, limits = L.limits || {}, tk = c.size('tick');
      var main = c.rows.filter(function (r) { return String(r[ep]) === mv; }), br = c.rows.filter(function (r) { return String(r[ep]) !== mv; });
      if (!main.length) { c.warn('journey-map: no step has path "' + mv + '"'); return; }
      var name = function (r) { var k = String(r[ek]); return names[k] !== undefined ? names[k] : r[es]; };
      var lim = function (r) { var k = String(r[ek]), v = limits[k] !== undefined ? limits[k] : el ? r[el] : ''; return v ? String(v) : ''; };
      var sub = function (r) { var w = String(L.sub || '{who}').split('{who}').join(ew ? r[ew] : '').replace(/^[.\s]+|[.\s]+$/g, ''); return w; };
      var from = L.branch_from === undefined ? String(main[0][ek]) : String(L.branch_from);
      // each box: its name (label, 700 on the path, 600 on a branch), the limit on its own line (label, 400, the text's
      // ink), who acts (tick, 400, the secondary ink), inside a 10 by 8 px pad
      var lb = c.size('label'), llh = Math.round(lb * 1.25), tlh = Math.round(tk * 1.25), PX = 10, PY = 8;
      var parts = function (r, w, onpath) {
        var aw = w - 2 * PX, n = c.wrap(name(r), 'label', aw, onpath ? 700 : 600).length, l = lim(r) ? c.wrap(lim(r), 'label', aw, 400).length : 0, s = sub(r) ? c.wrap(sub(r), 'tick', aw, 400).length : 0;
        return { n: n, l: l, s: s, h: Math.ceil(2 * PY + n * llh + (l ? 4 + l * llh : 0) + (s ? 4 + s * tlh : 0)) };
      };
      var sz = function (r, w, onpath) { return { w: w, h: parts(r, w, onpath).h }; };
      var draw_box = function (b) {
        var r = b.r, aw = b.w - 2 * PX, x = b.x + PX, pt = parts(r, b.w, b.on);
        c.rect(b.x, b.y, b.w, b.h, { fill: 'surface', kind: 'node', data: { key: String(r[ek]), field: es, value: r[es] } });
        c.rect(b.x + 0.5, b.y + 0.5, b.w - 1, b.h - 1, { stroke: b.on ? 'subject' : 'context', width: b.on ? 2 : 1.5, mark: false });
        var t = c.text(x, b.y + PY + 0.864 * lb, name(r), { role: 'label', weight: b.on ? 700 : 600, max: aw, leading: llh, fill: 'label' });
        var yb = b.y + PY + pt.n * llh;
        if (lim(r)) { c.text(x, yb + 4 + 0.864 * lb, lim(r), { role: 'label', weight: 400, max: aw, leading: llh, fill: 'label' }); yb += 4 + pt.l * llh; }
        if (sub(r)) c.text(x, yb + 4 + 0.864 * tk, sub(r), { role: 'tick', weight: 400, max: aw, leading: tlh });
        return t;
      };
      var boxes = {}, gap = across ? 30 : 26, y = 0, bottom = 0;
      if (across) {
        // across: equal boxes on one row, the branch under the step it leaves
        var bw = Math.floor((W - gap * (main.length - 1)) / main.length), bh = 0;
        main.forEach(function (r) { var s = sz(r, bw, true); bh = Math.max(bh, s ? s.h : 80); });
        main.forEach(function (r, i) { boxes[String(r[ek])] = { x: i * (bw + gap), y: y, w: bw, h: bh, r: r, on: true }; });
        var fb = boxes[from] || boxes[String(main[0][ek])], by = y + bh + 44;
        br.forEach(function (r) { var s = sz(r, bw, false), h = s ? s.h : 80; boxes[String(r[ek])] = { x: fb.x, y: by, w: bw, h: h, r: r, on: false }; by += h + gap; });
        main.forEach(function (r, i) { if (i) P.link(c, boxes[String(main[i - 1][ek])], boxes[String(r[ek])], { stroke: 'subject', width: 2, arrow: true }); });
        br.forEach(function (r) { var b = boxes[String(r[ek])]; P.link(c, { x: fb.x + 24, y: fb.y + fb.h, w: 0, h: 0 }, { x: b.x + 24, y: b.y, w: 0, h: 0 }, { stroke: 'context', width: 1.5, arrow: true }); });
        if (L.branch_label && br.length) P.clear_label(c, fb.x + 34, fb.y + fb.h + 26, L.branch_label, { role: 'tick', weight: 600, max: W - fb.x - 40 });
      } else {
        // down: the path in a column, its arrows between; the branch's link down the right edge to its box at the end
        var cw = W - 24;
        main.forEach(function (r) { var s = sz(r, cw, true), h = s ? s.h : 80; boxes[String(r[ek])] = { x: 0, y: y, w: cw, h: h, r: r, on: true }; y += h + gap; });
        var lead = L.branch_label && br.length ? Math.ceil(c.wrap(L.branch_label, 'tick', cw, 600).length * tk * 1.25) + 8 : 0;
        y += lead;
        br.forEach(function (r) { var s = sz(r, cw, false), h = s ? s.h : 80; boxes[String(r[ek])] = { x: 0, y: y, w: cw, h: h, r: r, on: false }; y += h + gap; });
        main.forEach(function (r, i) { if (i) { var a = boxes[String(main[i - 1][ek])], b = boxes[String(r[ek])]; P.link(c, { x: 24, y: a.y + a.h, w: 0, h: 0 }, { x: 24, y: b.y, w: 0, h: 0 }, { stroke: 'subject', width: 2, arrow: true }); } });
        var f2 = boxes[from] || boxes[String(main[0][ek])];
        br.forEach(function (r) {
          var b = boxes[String(r[ek])], gx = W - 8;
          P.link(c, { x: f2.x + f2.w, y: f2.y + 18, w: 0, h: 0 }, { x: gx, y: b.y + 18, w: 0, h: 0 }, { shape: 'elbow', dir: 'right', bend: gx, stroke: 'context', width: 1.5 });
          P.link(c, { x: gx, y: b.y + 18, w: 0, h: 0 }, { x: b.x + b.w, y: b.y + 18, w: 0, h: 0 }, { stroke: 'context', width: 1.5, arrow: true });
        });
        if (lead) c.text(0, br.length ? boxes[String(br[0][ek])].y - lead + tk * 0.9 : y, L.branch_label, { role: 'tick', weight: 600, max: cw });
        c.arrange('phone');
      }
      Object.keys(boxes).forEach(function (k) {
        var b = boxes[k];
        draw_box(b);
        bottom = Math.max(bottom, b.y + b.h);
      });
      c.height(bottom + 2);
    }
  });
})(globalThis.OAChart);
