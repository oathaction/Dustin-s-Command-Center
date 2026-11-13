/* Decision tree (coverage plan 3.11, core; S67). A question a reader answers in turn: the question in a box with an
 * edge in the subject ink, and each answer in a box with a fine edge under it, joined by a fine line with an arrowhead.
 * An answer box opens with the answer and the count of places it holds (counted from the rows its where keeps), then
 * what it means, then those places by name; an answer may ask a further question, whose answers sit under it, set in.
 * Desk: the first answers side by side where each column holds 190 px, their own answers stacked in the column;
 * narrower, every answer runs down the page, set in from a line at the left. The table groups the rows by answer, in
 * the drawing's order (sort by the answer's field with its values).
 * encode: place (text: the name listed under an answer).
 * labels: tree ({q: question, sub: a line under it, branches: [{answer, where: {field: value, [values], null for
 * empty, or {not: values}}, count (words with {n}), leaf (what it means), list (true: name the places), then: a
 * further {q, branches}}]}). */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'decision-tree', name: 'Decision Tree', family: 'structure',
    encode: { place: 'text' },
    labels: ['tree'],
    phone: 'differs',
    draw: function (c) {
      var W = c.width, ep = c.field('place'), T = c.labels.tree || {}, pad = 10, gap = 12, ind = 28, spine = 15, cg = 16;
      // words set here once, by the spec's typography or the guide's own (curly quotes, held dates), so Node and the page,
      // whose rows may arrive unset, print and measure the same words
      var ty = function (w) { return K.typeset({ typography: c.spec.typography || { curl_quotes: true, nbsp: true } }, String(w).replace(/[ \t\n]+/g, ' ')); };
      var keeps = function (r, wh) {
        return Object.keys(wh || {}).every(function (k) {
          var v = wh[k], x = r[k] === null || r[k] === undefined ? null : String(r[k]);
          if (v && typeof v === 'object' && !Array.isArray(v)) return [].concat(v.not).map(String).indexOf(x) < 0;
          return [].concat(v).map(function (q) { return q === null ? null : String(q); }).indexOf(x) >= 0;
        });
      };
      var lines = function (b) {
        var p = [];
        if (b.q !== undefined) { p.push({ w: b.q, role: 'label', wt: 700 }); if (b.sub) p.push({ w: b.sub, role: 'tick', wt: 400, fill: 'secondary' }); return p; }
        var rows = c.rows.filter(function (r) { return keeps(r, b.where); });
        p.push({ w: b.answer + (b.count ? ': ' + String(b.count).split('{n}').join(String(rows.length)) : ''), role: 'label', wt: 700 });
        if (b.leaf) p.push({ w: b.leaf, role: 'label', wt: 400 });
        if (b.list) p.push({ w: rows.map(function (r) { return r[ep]; }).join(', '), role: 'tick', wt: 400, fill: 'secondary' });
        return p;
      };
      var fit = function (p, w) {
        var y = pad;
        p.forEach(function (q) { q.w = ty(q.w); });
        p.forEach(function (q, i) {
          var s = c.size(q.role), lh = Math.round(s * 1.3), n = c.wrap(ty(q.w), q.role, w - 2 * pad, q.wt).length;
          if (i) y += 5;
          q.base = y + s * 0.93; q.lh = lh;
          y = q.base + (n - 1) * lh + s * 0.3;
        });
        return Math.ceil(y + pad);
      };
      var box = function (x, y, w, p, ask, key) {
        var h = fit(p, w);
        c.rect(x + 0.5, y + 0.5, w - 1, h - 1, { fill: ask ? 'surface' : 'track', stroke: ask ? 'subject' : 'context', width: 1, data: { key: key, field: ask ? 'question' : 'answer', value: p[0].w } });
        p.forEach(function (q) { c.text(x + pad, y + q.base, q.w, { role: q.role, weight: q.wt, max: w - 2 * pad, leading: q.lh, fill: q.fill }); });
        return h;
      };
      // a run of the kit's link part (R3-5); arrow: a head at its end
      var ln = function (x1, y1, x2, y2, arrow) { K.parts.link(c, { x: x1, y: y1 }, { x: x2, y: y2 }, { stroke: 'subject', arrow: !!arrow, head: [7, 4] }); };
      // a further question under an answer at x, its top 16 px under the answer's bottom y, joined by an arrow from the
      // line at the answer's left, and its own answers under it, set in
      var ask = function (q, x, y, w, key) {
        var qy = y + 16, qh = box(x, qy, w, lines(q), true, key + '.q');
        ln(x + spine, y, x + spine, qy, true);
        return down(q.branches || [], x, qy + qh, w, qy + qh, key + '.q');
      };
      // the answers of one question, down the page from a line at the parent box's left, set in
      var down = function (bs, x, y, w, top, key) {
        var sx = x + spine, last = top;
        bs.forEach(function (b, i) {
          var by = y + (i ? gap : 16), bh = box(x + ind, by, w - ind, lines(b), false, key + '.' + i), ly = by + Math.min(22, bh / 2);
          ln(sx, last, sx, ly); ln(sx, ly, x + ind, ly, true);
          last = ly;
          y = by + bh;
          if (b.then) y = ask(b.then, x + ind, y, w - ind, key + '.' + i);
        });
        return y;
      };
      var rh = box(0, 0, W, lines(T), true, 'root'), bs = T.branches || [], k = bs.length;
      var cw = (W - (k - 1) * cg) / k, y;
      if (k > 1 && cw >= 190) {
        var bus = rh + 14, cx = function (i) { return i * (cw + cg) + cw / 2; };
        ln(W / 2, rh, W / 2, bus);
        ln(cx(0), bus, cx(k - 1), bus);
        y = 0;
        bs.forEach(function (b, i) {
          var x = i * (cw + cg), top = bus + 22;
          ln(cx(i), bus, cx(i), top, true);
          var bh = box(x, top, cw, lines(b), false, 'b' + i), yy = top + bh;
          if (b.then) yy = ask(b.then, x, yy, cw, 'b' + i);
          y = Math.max(y, yy);
        });
      } else {
        c.arrange('phone');
        y = down(bs, 0, rh, W, rh, 'b');
      }
      c.height(y + 1);
    }
  });
})(globalThis.OAChart);
