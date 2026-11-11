/* Timeline (coverage plan 3.3, core; S09). Dated events on lanes along one true time scale, each event's date and name
 * printed; shaded bands mark stretches the notes explain. On a phone each lane becomes a dated list (DR-64).
 * encode: date (date), lane (category), label (text), key (id).
 * labels: lanes ([{value, label, question}]), bands ([{from, to, label, note}]), axis_years ([years]). */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'timeline', name: 'Timeline', family: 'change-over-time',
    encode: { date: 'date', lane: 'category', label: 'text', key: 'id' },
    labels: ['lanes', 'bands', 'axis_years', 'cut_at'],
    phone: 'differs',
    draw: function (c) {
      var rows = c.rows, ed = c.field('date'), el = c.field('lane'), et = c.field('label'), ek = c.field('key'), L = c.labels, W = c.width;
      var lanes = L.lanes || [], size = c.size('label'), small = c.size('tick');
      if (c.phone) {
        var y = 0;
        lanes.forEach(function (ln) {
          y += size + 4;
          c.text(0, y, ln.label, { role: 'label', weight: 700 });
          if (ln.question) { var q = c.text(0, y + small + 4, ln.question, { role: 'tick', max: W, fill: 'secondary' }); y = q.y + q.h; }
          y += 12;
          var evs = rows.filter(function (r) { return r[el] === ln.value; }).sort(function (a, b) { return a[ed] < b[ed] ? -1 : 1; });
          var y_first = y;
          evs.forEach(function (r) {
            c.circle(4, y + 6, c.t('dot-vertex-radius'), { fill: 'subject', data: { key: r[ek], field: ed, value: r[ed] } });
            c.text(16, y + small, K.fmt(r[ed], 'year'), { role: 'tick', weight: 700 });
            var b = c.text(58, y + small, r[et], { role: 'tick', max: W - 58 });
            y = b.y + b.h + 8;
          });
          if (evs.length) c.line(4, y_first + 6, 4, y - 14, { stroke: 'baseline', width: c.t('line-hairline'), mark: false });
          y += 18;
        });
        c.height(y);
        return;
      }
      var ts = rows.map(function (r) { return K.time(r[ed]); });
      var lo = Math.floor(Math.min.apply(null, ts) / 25) * 25, hi = Math.ceil(Math.max.apply(null, ts));
      var lw = 0;
      lanes.forEach(function (ln) { lw = Math.max(lw, c.measure(ln.label, 'label', 700)); });
      var x0 = Math.min(Math.ceil(lw + 30), 120), x1 = W - 8, xs = K.scale.linear([lo, hi], [x0, x1]);
      var top = (L.bands || []).some(function (b) { return b.note; }) ? 42 : 26, y = top;
      // bands
      var bands = L.bands || [];
      var laneTops = [];
      lanes.forEach(function (ln) {
        var evs = rows.filter(function (r) { return r[el] === ln.value; }).sort(function (a, b) { return a[ed] < b[ed] ? -1 : 1; });
        // stack labels in rows above the lane's line so none overlap, latest first at the top
        var slots = [], maxw = Math.min(260, (x1 - x0) * 0.45), lh = small + 6, llh = Math.round(small * 1.25);
        var placed = evs.map(function (r) {
          var nm = String(r[et]);
          if (L.cut_at && nm.indexOf(L.cut_at) > 0) nm = nm.slice(0, nm.indexOf(L.cut_at)).replace(/\s+$/, '');
          var x = xs(K.time(r[ed])), txt = K.fmt(r[ed], 'year') + ' ' + nm;
          var lines = K.wrap(txt, small, maxw, 400), w = 0;
          lines.forEach(function (l) { w = Math.max(w, c.measure(l, 'tick', 400) + 4); });
          var anchor = x + w <= x1 ? 'start' : 'end';
          var a0 = anchor === 'start' ? x : Math.max(x0, x - w);
          var s = 0;
          while (slots[s] && slots[s].some(function (iv) { return a0 < iv[1] + 8 && iv[0] < a0 + w + 8; })) s++;
          (slots[s] = slots[s] || []).push([a0, a0 + w]);
          return { r: r, x: x, txt: txt, lines: lines.length, a0: a0, w: w, anchor: anchor, slot: s };
        });
        var nslot = Math.max(1, slots.length);
        var sh = [];
        placed.forEach(function (p) { sh[p.slot] = Math.max(sh[p.slot] || 1, p.lines); });
        var off = [], acc = 0;
        for (var si = nslot - 1; si >= 0; si--) { off[si] = acc; acc += (sh[si] || 1) * llh + 6; }
        var qh = ln.question ? K.wrap(ln.question, small, x0 - 12, 400).length * llh + size + 10 : size + 6;
        var laneH = Math.max(acc + 16, qh);
        laneTops.push([y, laneH]);
        c.text(0, y + size, ln.label, { role: 'label', weight: 700 });
        if (ln.question) c.text(0, y + size + small + 6, ln.question, { role: 'tick', fill: 'secondary', max: x0 - 12 });
        var base = y + laneH;
        void lh;
        placed.forEach(function (p) {
          var ty = base - 12 - off[p.slot] - (p.lines - 1) * llh;
          c.line(p.x, ty + (p.lines - 1) * llh + 4, p.x, base, { stroke: 'leader', width: c.t('line-hairline'), mark: false });
          var tx = p.anchor === 'start' ? p.x + 3 : p.a0 + p.w;
          c.text(tx, ty, p.txt, { role: 'tick', anchor: p.anchor, halo: true, max: p.lines > 1 ? Math.min(260, (x1 - x0) * 0.45) + 1 : undefined });
          c.circle(p.x, base, c.t('dot-small-vertex-radius'), { fill: 'subject', data: { key: p.r[ek], field: ed, value: p.r[ed] } });
        });
        c.line(x0, base, x1, base, { stroke: 'gridline', width: c.t('line-hairline'), mark: false });
        y = base + 26;
      });
      bands.forEach(function (b) {
        var a = xs(b.from), z = xs(b.to + 1);
        c.rect(a, top - 6, z - a, y - top - 14, { fill: 'band', mark: false });
        if (b.label) { var bw = c.measure(b.label, 'tick', 700); c.text(Math.min(z - 4, W), top - 10 - (b.note ? 16 : 0), b.label, { role: 'tick', weight: 700, anchor: 'end' }); void bw; }
        if (b.note) c.text(Math.min(z - 4, W), top - 10, b.note, { role: 'tick', fill: 'secondary', anchor: 'end' });
      });
      // bands draw under the lanes: move them to the front of the element list
      if (bands.length) {
        var n = bands.length * 1;
        var els = c._els, tail = els.splice(els.length - (bands.length + bands.filter(function (b) { return b.label; }).length));
        c._els = tail.filter(function (e) { return e.indexOf('<rect') === 0; }).concat(els, tail.filter(function (e) { return e.indexOf('<rect') !== 0; }));
        void n;
      }
      var ay = y - 4;
      (L.axis_years || K.ticks(lo, hi, 6)).forEach(function (yr) {
        if (yr < lo || yr > hi) return;
        var yw = c.measure(String(yr), 'tick');
        c.text(Math.min(xs(yr), W - yw / 2), ay, String(yr), { role: 'tick', anchor: 'middle' });
      });
      c.line(x0, ay - small - 6, x1, ay - small - 6, { stroke: 'baseline', width: c.t('line-baseline'), mark: false });
      c.height(ay + 6);
    }
  });
})(globalThis.OAChart);
