/* Slope chart (coverage plan 3.1, core; S20). Two points in time for many items: each item a line from its earlier value
 * on the left axis to its later value on the right, the earlier value printed at the left, the later value and the item's
 * name at the right. Items the title names are set in ink, the rest in gray; labels that would touch move apart and keep a
 * short leader to their line's end.
 * encode: category (category), value (number), series (category: which of the two times a row is).
 * labels: from, to (the two series values), from_label, to_label (the axis heads; the series values otherwise),
 * categories ({category: printed name}), named (a category or list set in ink). formats: value. scale: y ([lo, hi]). */
(function (K) {
  'use strict';
  function dodge(items, gap, lo, hi) {
    // items: [{y}] -> each gets .ly, at least gap apart, kept between lo and hi where it can be
    var s = items.slice().sort(function (a, b) { return a.y - b.y; });
    s.forEach(function (it, i) { it.ly = i ? Math.max(it.y, s[i - 1].ly + gap) : Math.max(it.y, lo); });
    for (var i = s.length - 1; i >= 0; i--) {
      var cap = i === s.length - 1 ? hi : s[i + 1].ly - gap;
      if (s[i].ly > cap) s[i].ly = cap;
    }
    return items;
  }
  K.register_chart({
    form: 'slope',
    name: 'Slope Chart',
    family: 'comparison',
    encode: { category: 'category', value: 'number', series: 'category' },
    labels: ['from', 'to', 'from_label', 'to_label', 'categories', 'named'],
    phone: 'same',
    draw: function (c) {
      var rows = c.rows, ek = c.field('category'), ev = c.field('value'), es = c.field('series');
      var f = c.spec.formats || {}, W = c.width, L = c.labels, names = L.categories || {};
      var named = L.named === undefined ? null : [].concat(L.named).map(String);
      var ink = function (k) { return !named || named.indexOf(k) >= 0; };
      var cats = [], pair = {};
      rows.forEach(function (r) {
        var k = String(r[ek]);
        if (!pair[k]) { pair[k] = {}; cats.push(k); }
        if (String(r[es]) === String(L.from)) pair[k].from = r[ev];
        else if (String(r[es]) === String(L.to)) pair[k].to = r[ev];
      });
      cats = cats.filter(function (k) {
        if (pair[k].from === undefined || pair[k].to === undefined) { c.warn('row ' + k + ' lacks one of its two values'); return false; }
        return true;
      });
      var name = function (k) { return names[k] !== undefined ? names[k] : k; };
      var fv = function (v) { return K.fmt(v, f.value || 'number:1'); };
      var size = c.size('label'), tick = c.size('tick'), gap = Math.round(size * 1.3);
      // widths: the left values, the right values and names
      var wl = 0, wv = 0, wn = 0;
      cats.forEach(function (k) {
        wl = Math.max(wl, c.measure(fv(pair[k].from), 'label', 700, true));
        wv = Math.max(wv, c.measure(fv(pair[k].to), 'label', 700, true));
        wn = Math.max(wn, c.measure(name(k), 'label', 700));
      });
      var top = tick + 16, plotH = c.t(c.phone ? 'columns-phone-height' : 'columns-height') * 0.85, bot = top + plotH;
      // the span between the axes stays near the plot's height, so a slope reads at a fair angle on a wide artboard
      var xl = Math.ceil(wl + 10), xr = Math.floor(Math.min(W - (wv + 10 + wn + 10), xl + plotH * 1.25));
      if (xr - xl < 60) c.warn('the slope has under 60 px between its axes');
      var vals = [];
      cats.forEach(function (k) { vals.push(pair[k].from, pair[k].to); });
      var sc = (c.spec.scale || {}).y || K.nice(Math.min.apply(null, vals), Math.max.apply(null, vals), 4);
      var ys = K.scale.linear([sc[0], sc[1]], [bot, top]);
      // the axis heads and the two axes
      c.text(xl, tick, L.from_label || String(L.from), { role: 'tick', weight: 600, anchor: 'middle', fill: 'label' });
      c.text(xr, tick, L.to_label || String(L.to), { role: 'tick', weight: 600, anchor: 'middle', fill: 'label' });
      c.line(xl, top - 6, xl, bot, { stroke: 'baseline', width: c.t('line-hairline'), mark: false });
      c.line(xr, top - 6, xr, bot, { stroke: 'baseline', width: c.t('line-hairline'), mark: false });
      // the labels' places, moved apart where they would touch
      var left = dodge(cats.map(function (k) { return { k: k, y: ys(pair[k].from) }; }), gap, top, bot + gap);
      var right = dodge(cats.map(function (k) { return { k: k, y: ys(pair[k].to) }; }), gap, top, bot + gap);
      // gray lines first, ink lines over them
      var order = cats.slice().sort(function (a, b) { return (ink(a) ? 1 : 0) - (ink(b) ? 1 : 0); });
      order.forEach(function (k) {
        var y0 = ys(pair[k].from), y1 = ys(pair[k].to), on = ink(k);
        c.line(xl, y0, xr, y1, { stroke: on ? 'subject' : 'context', width: c.t(on ? 'line-subject' : 'line-context'), data: { key: k, field: ev } });
        c.circle(xl, y0, c.t('dot-vertex-radius'), { fill: on ? 'subject' : 'context', data: { key: k + '|' + L.from, field: ev, value: pair[k].from } });
        c.circle(xr, y1, c.t('dot-vertex-radius'), { fill: on ? 'subject' : 'context', data: { key: k + '|' + L.to, field: ev, value: pair[k].to } });
      });
      left.forEach(function (it) {
        var on = ink(it.k);
        c.text(xl - 8, it.ly + size * 0.35, fv(pair[it.k].from), { role: 'label', weight: on ? 700 : 400, anchor: 'end', tnum: true, fill: on ? 'label' : 'secondary' });
      });
      right.forEach(function (it) {
        var on = ink(it.k), tb = c.text(xr + 8, it.ly + size * 0.35, fv(pair[it.k].to), { role: 'label', weight: on ? 700 : 400, tnum: true, fill: on ? 'label' : 'secondary' });
        c.text(xr + 8 + wv + 10, it.ly + size * 0.35, name(it.k), { role: 'label', weight: on ? 700 : 600 });
        void tb;
      });
      var low = Math.max.apply(null, left.concat(right).map(function (it) { return it.ly; }));
      c.height(Math.max(bot, low + size) + 4);
    }
  });
})(globalThis.OAChart);
