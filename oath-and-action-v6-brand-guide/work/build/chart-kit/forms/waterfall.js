/* Waterfall (coverage plan 3.4, core; S44). Steps that add to a total, read from top to bottom: each step floats from
 * the running total before it to the one after, a step up in ink and a step down in the light fill, every value printed
 * with its sign; a total runs from the zero line as an outlined bar and resets the running total; a hairline joins each
 * step to the next; the values stand in a column at the right. On a phone each name sits over its bar.
 * encode: category (text), value (number, signed: a step's change, or a total's level), kind (category).
 * labels: names ({category: printed name}), totals (the kind values drawn as totals from zero), named and point (rows the title names: in ink or working
 * red; K.parts.named_fill), up and down (words for the key), scale_head (words over the value scale).
 * formats: value (each printed value, unsigned; the form adds the sign), tick (the scale's labels). */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'waterfall', name: 'Waterfall', family: 'composition',
    encode: { category: 'text', value: 'number', kind: 'category' },
    labels: ['names', 'totals', 'named', 'point', 'up', 'down', 'scale_head'],
    phone: 'same',
    draw: function (c) {
      var P = K.parts, rows = c.rows, ek = c.field('category'), ev = c.field('value'), ekd = c.field('kind');
      var L = c.labels, f = c.spec.formats || {}, W = c.width, totals = [].concat(L.totals || []).map(String);
      var pt = L.point === undefined ? null : String(L.point), named = [].concat(L.named || []).map(String);
      var size = c.size('label'), tick = c.size('tick'), lh = Math.round(size * 1.25);
      var names = L.names || {}, nm = function (r) { var k = String(r[ek]); return names[k] !== undefined ? names[k] : k; };
      var is_total = function (r) { return totals.indexOf(String(r[ekd])) >= 0; };
      // the running total before and after each row
      var run = 0, lo = 0, hi = 0, steps = rows.map(function (r) {
        var a = is_total(r) ? 0 : run, b = is_total(r) ? r[ev] : run + r[ev];
        run = b; lo = Math.min(lo, a, b); hi = Math.max(hi, a, b);
        return { r: r, a: a, b: b, total: is_total(r) };
      });
      var num = function (s) {
        var v = s.total ? s.r[ev] : Math.abs(s.r[ev]), t = K.fmt(Math.abs(v), f.value || 'number:1');
        return (s.total ? (v < 0 ? K.minus : '') : (s.r[ev] < 0 ? K.minus : '+')) + t;
      };
      var vw = 0;
      steps.forEach(function (s) { vw = Math.max(vw, c.measure(num(s), 'label', 700, true)); });
      var lmax = c.phone ? W - vw - 12 : Math.floor(W * 0.36), nw = 0;
      rows.forEach(function (r) { c.wrap(nm(r), 'label', lmax, 600).forEach(function (l) { nw = Math.max(nw, c.measure(l, 'label', 600)); }); });
      var x0 = c.phone ? 0 : Math.ceil(nw + 16);
      var st = K.nice(lo, hi, 4).step, dlo = lo, dhi = hi;
      var xs = K.scale.linear([dlo, dhi], c.phone ? [2, W - 2] : [x0 + 6, W - vw - 18]), ticks = K.ticks(Math.ceil(lo / st) * st, Math.floor(hi / st) * st, 0, st);
      // the key, then the scale's labels over the plot
      var y = 0;
      if (L.up || L.down) {
        y += size + 2;
        y += P.key(c, [{ label: L.up, fill: 'subject', direct: true }, { label: L.down, fill: c.ground === 'charcoal' ? 'context' : 'light-fill', direct: true }].filter(function (e) { return e.label; }), 0, y, W) + 6;
      }
      if (L.scale_head) { c.text(xs(dlo), y + tick, L.scale_head, { role: 'tick', fill: 'secondary' }); y += tick + 8; }
      y += tick;
      var lastx = -1e9;
      ticks.forEach(function (v) {
        var t = K.fmt(v, f.tick || 'number:0'), tw = c.measure(t, 'tick'), tx = Math.max(tw / 2, Math.min(W - tw / 2, xs(v)));
        if (tx - tw / 2 < lastx + 10) return;
        c.text(tx, y, t, { role: 'tick', anchor: 'middle', tnum: true });
        lastx = tx + tw / 2;
      });
      var top = y + 8, bh = c.t('bar-dense-height') - 2, by = top, prev = null, bottom = top, ys = [];
      var other = c.ground === 'charcoal' ? 'context' : 'light-fill';
      var nlines = function (r) { return c.wrap(nm(r), 'label', lmax, 600).length; };
      // each row's place first, so the scale's lines draw under the bars
      var pn = 1;
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
        var r = s.r, lines = nlines(r), isp = pt !== null && String(r[ek]) === pt, by = ys[i];
        var isn = isp || named.indexOf(String(r[ek])) >= 0;
        var cy = by + bh / 2 + size * 0.35;
        if (c.phone) c.text(0, by - 6 - (lines - 1) * lh, nm(r), { role: 'label', weight: isn ? 700 : 600, max: lmax });
        else c.text(0, cy - (lines - 1) * lh / 2, nm(r), { role: 'label', weight: isn ? 700 : 600, max: lmax });
        var xa = xs(Math.min(s.a, s.b)), xb = xs(Math.max(s.a, s.b)), d = { key: r[ek], field: ev, value: r[ev] };
        var kl = isp && c.ground !== 'charcoal' ? { stroke: 'point-keyline', width: c.t('keyline') } : {};
        if (s.total) {
          var fo = isp ? { fill: 'point' } : { fill: isn ? 'subject' : 'surface' };
          c.rect(xa, by, xb - xa, bh, Object.assign(fo, { kind: 'bar', axis: 'x', zero: xs(0), data: d }, kl));
          if (!isp && !isn) c.rect(xa + 0.75, by + 0.75, Math.max(0, xb - xa - 1.5), bh - 1.5, { stroke: 'subject', width: 1.5, mark: false });
        } else {
          var up = r[ev] >= 0, fl = isp ? 'point' : isn || up ? 'subject' : other;
          c.rect(xa, by, Math.max(1, xb - xa), bh, Object.assign({ fill: fl, kind: 'segment', data: d }, kl));
        }
        // the value in a column at the right, flush right in tabular figures (on a phone, on the name's first line)
        c.text(W, c.phone ? by - 6 - (lines - 1) * lh : cy, num(s), { role: 'label', weight: s.total || isn ? 700 : 400, anchor: 'end', tnum: true });
        // a hairline from the last step's end to this one's start; on a phone only where it clears the words between
        var px = prev && xs(prev.x), nb = c.texts[c.texts.length - 2], clear = !c.phone || (prev && (px > nb.x + nb.w + 4 && px < W - vw - 6));
        if (prev !== null && clear) c.line(px, prev.y, px, by, { stroke: 'leader', width: c.t('line-hairline'), mark: false });
        prev = { x: s.b, y: by + bh };
      });
      c.height(bottom + 6);
    }
  });
})(globalThis.OAChart);
