/* Waterfall (coverage plan 3.4, core; S44). Steps that add to a total, read from top to bottom: each step floats from
 * the running total before it to the one after, a step that adds in diverging pair B's Verdigris end and a step that
 * takes away in its Prussian end (the sides S25 uses), every value printed with its sign beside its bar; a total runs
 * from the zero line in the context ink and resets the running total; a hairline in the secondary ink joins each step
 * to the next. On a phone each name sits over its bar.
 * encode: category (text), value (number, signed: a step's change, or a total's level), kind (category).
 * labels: names ({category: printed name}), totals (the kind values drawn as totals from zero), named (rows the title
 * names, in the subject ink; never red, which on a deficit reads as its sign), up and down (the key's words),
 * scale_head (words over the value scale). formats: value (a printed value; the form adds the sign), tick. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'waterfall', name: 'Waterfall', family: 'composition',
    encode: { category: 'text', value: 'number', kind: 'category' },
    labels: ['names', 'totals', 'named', 'up', 'down', 'scale_head'],
    phone: 'same',
    draw: function (c) {
      var P = K.parts, rows = c.rows, ek = c.field('category'), ev = c.field('value'), ekd = c.field('kind');
      var L = c.labels, f = c.spec.formats || {}, W = c.width, totals = [].concat(L.totals || []).map(String);
      var named = [].concat(L.named || []).map(String), size = c.size('label'), tick = c.size('tick'), lh = Math.round(size * 1.25);
      var names = L.names || {}, nm = function (r) { var k = String(r[ek]); return names[k] !== undefined ? names[k] : k; };
      var is_total = function (r) { return totals.indexOf(String(r[ekd])) >= 0; };
      // the running total before and after each row
      var run = 0, lo = 0, hi = 0, steps = rows.map(function (r) {
        var a = is_total(r) ? 0 : run, b = is_total(r) ? r[ev] : run + r[ev];
        run = b; lo = Math.min(lo, a, b); hi = Math.max(hi, a, b);
        return { r: r, a: a, b: b, total: is_total(r) };
      });
      var num = function (s) {
        var v = s.r[ev], t = K.fmt(Math.abs(v), f.value || 'number:1');
        return (v < 0 ? K.minus : s.total ? '' : '+') + t;
      };
      var vw = 0;
      steps.forEach(function (s) { vw = Math.max(vw, c.measure(num(s), 'label', 700, true)); });
      var lmax = c.phone ? W : Math.floor(W * 0.36), nw = 0;
      // one weight for row names and values (BC S8, D3-901): 400, and 700 for the row the title names
      var isnm = function (r) { return named.indexOf(String(r[ek])) >= 0; }, rw = function (r) { return P.row_weight(isnm(r)); };
      rows.forEach(function (r) { c.wrap(nm(r), 'label', lmax, rw(r)).forEach(function (l) { nw = Math.max(nw, c.measure(l, 'label', rw(r))); }); });
      var x0 = c.phone ? 0 : Math.ceil(nw + 16), st = K.nice(lo, hi, 4).step;
      var xs = K.scale.linear([lo, hi], [x0 + vw + 6, W - vw - 6]), ticks = K.ticks(Math.ceil(lo / st) * st, Math.floor(hi / st) * st, 0, st);
      // the key, then the scale's labels over the plot
      var y = 0;
      if (L.up || L.down) {
        y += size + 2;
        y += P.key(c, [{ label: L.up, fill: 'div-5', direct: true }, { label: L.down, fill: 'div-1', direct: true }].filter(function (e) { return e.label; }), 0, y, W) + 6;
      }
      if (L.scale_head) { c.text(xs(lo), y + tick, L.scale_head, { role: 'tick', fill: 'secondary' }); y += tick + 8; }
      y += tick;
      var lastx = -1e9;
      ticks.forEach(function (v) {
        var t = K.fmt(v, f.tick || 'number:0'), tw = c.measure(t, 'tick'), tx = Math.max(tw / 2, Math.min(W - tw / 2, xs(v)));
        if (tx - tw / 2 < lastx + 10) return;
        c.text(tx, y, t, { role: 'tick', anchor: 'middle', tnum: true });
        lastx = tx + tw / 2;
      });
      var top = y + 8, bh = c.t('bar-dense-height') - 2, by = top, prev = null, bottom = top, ys = [], pn = 1;
      var nlines = function (r) { return c.wrap(nm(r), 'label', lmax, rw(r)).length; };
      // each row's place first, so the scale's lines draw under the bars
      steps.forEach(function (s, i) {
        var n = nlines(s.r);
        if (c.phone) by += (i ? bh + 12 : 0) + n * lh;
        else if (i) by += Math.max(bh + 8, (pn + n) * lh / 2 + 4);
        pn = n;
        ys.push(by);
        bottom = by + bh;
      });
      // the scale's lines run the plot's height; on a phone they run beside each bar only, never through the names
      var vlines = function (y0, y1) {
        ticks.forEach(function (v) { if (v) c.line(xs(v), y0, xs(v), y1, { stroke: 'gridline', width: c.t('line-hairline'), mark: false }); });
        c.line(xs(0), y0, xs(0), y1, { stroke: 'baseline', width: c.t('line-baseline'), mark: false });
      };
      if (c.phone) ys.forEach(function (yy) { vlines(yy - 3, yy + bh + 3); });
      else vlines(top - 4, bottom + 4);
      steps.forEach(function (s, i) {
        var r = s.r, lines = nlines(r), by = ys[i], isn = named.indexOf(String(r[ek])) >= 0, cy = by + bh / 2 + size * 0.35;
        if (c.phone) P.row_name(c, 0, by - 6 - (lines - 1) * lh, nm(r), { named: isn, max: lmax });
        else P.row_name(c, 0, cy - (lines - 1) * lh / 2, nm(r), { named: isn, max: lmax });
        var xa = xs(Math.min(s.a, s.b)), xb = xs(Math.max(s.a, s.b)), d = { key: r[ek], field: ev, value: r[ev] };
        var fl = isn ? 'subject' : s.total ? 'context' : r[ev] >= 0 ? 'div-5' : 'div-1';
        // a total takes its own paint in forced colors, the ground with a CanvasText outline, apart from every step (AX S3)
        c.rect(xa, by, Math.max(1, xb - xa), bh, s.total ? { fill: fl, kind: 'bar', axis: 'x', zero: xs(0), data: d, fc: 'total' } : { fill: fl, kind: 'segment', data: d });
        // the value beside the bar, on the side the step moves to (a total's on its far side), or the other side where
        // the drawing ends first
        var t = num(s), tw = c.measure(t, 'label', 700, true), right = s.total ? s.b >= 0 : r[ev] >= 0;
        if (right && xb + 4 + tw > W) right = false;
        if (!right && xa - 4 - tw < (c.phone ? 0 : x0)) right = true;
        // a value that would sit across the zero line moves to the bar's other side where that side is clear (MA-9)
        var zx = xs(0), spans = function (r_) { var a = r_ ? xb + 3.5 : xa - 3.5 - tw; return zx > a - 2 && zx < a + tw + 2; };
        if (spans(right) && !spans(!right) && (right ? xa - 4 - tw >= (c.phone ? 0 : x0) : xb + 4 + tw <= W)) right = !right;
        // on a knockout of the ground, so a gridline or connector never runs through a minus sign (AX S2, BC S1)
        P.row_value(c, right ? xb + 3.5 : xa - 3.5, cy, t, { named: isn, anchor: right ? 'start' : 'end', clear: true });
        // a hairline from the last step's end to this one's start; on a phone only where it clears the name between
        var px = prev && xs(prev.x), nb = c.texts[c.texts.length - 2];
        if (prev && (!c.phone || px > nb.x + nb.w + 4)) c.line(px, prev.y, px, by, { stroke: 'secondary', width: c.t('line-hairline'), mark: false });
        prev = { x: s.b, y: by + bh };
      });
      c.height(bottom + 6);
    }
  });
})(globalThis.OAChart);
