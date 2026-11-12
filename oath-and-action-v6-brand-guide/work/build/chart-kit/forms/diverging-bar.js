/* Diverging bar (coverage plan 3.2, core; S25). Gains and losses from one zero line: a bar to the left for a loss and to
 * the right for a gain, each starting on zero (Rule 14.4), in the order the spec sorts them. Position and the printed sign
 * carry the direction; the fill repeats it in diverging pair B's end steps, Prussian for a loss and Verdigris for a
 * gain (DR-54). Each figure sits just across the zero line from its bar, so every figure lines up on zero. Row names
 * sit flush left, as the family's long ranked lists set them, and the scale ends 8 px inside the drawing's edge.
 * encode: key (code), label (text, optional when labels.names covers every drawn key), value (number), include (boolean,
 * optional: rows where it is false stay in the table and out of the drawing). labels: names ({key: words} for the drawn
 * rows), apart (a key, such as a total, printed in words above the bars and drawn without a bar), apart_words (with
 * {value}), value (words beside each bar, with {value}). formats: value, tick. Maker B, round 1. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'diverging-bar',
    name: 'Diverging Bar',
    family: 'shift-and-swing',
    encode: { key: 'code', label: 'text?', value: 'number', include: 'boolean?' },
    labels: ['names', 'apart', 'apart_words', 'value'],
    phone: 'same',
    draw: function (c) {
      var L = c.labels, f = c.spec.formats || {}, W = c.width, ek = c.field('key'), el = c.field('label', false), ev = c.field('value'), ei = c.field('include', false);
      var names = L.names || {}, name = function (r) { return names[String(r[ek])] || (el ? r[el] : String(r[ek])); };
      var apart = c.rows.filter(function (r) { return L.apart !== undefined && String(r[ek]) === String(L.apart); });
      var rows = c.rows.filter(function (r) { return apart.indexOf(r) < 0 && (!ei || r[ei] === true) && r[ev] !== null; });
      var words = function (v) { return String(L.value || '{value}').replace('{value}', K.fmt(v, f.value || 'signed:0')); };
      var size = c.size('label'), pitch = Math.round(size * 1.6), bh = Math.min(c.t('bar-dense-height'), pitch - 6);
      var vals = rows.map(function (r) { return r[ev]; });
      var lo = Math.min(0, Math.min.apply(null, vals)), hi = Math.max(0, Math.max.apply(null, vals));
      // the scale ends at the furthest bar on the short side, with ticks only inside it
      var nk = K.nice(lo, hi, c.phone ? 3 : 5);
      var short_lo = -lo < hi, ticks = K.ticks(short_lo ? lo : nk[0], short_lo ? nk[1] : hi, 0, nk.step);
      nk = short_lo ? [Math.min(lo, ticks[0]), nk[1]] : [nk[0], Math.max(hi, ticks[ticks.length - 1])];
      var nw = 0, vw = 0;
      rows.forEach(function (r) { nw = Math.max(nw, c.measure(name(r), 'label')); vw = Math.max(vw, c.measure(words(r[ev]), 'label', 400, true)); });
      // a name column beside the bars, or each name above its bar where the column would crowd the bars
      var stacked = W - nw - 14 < W * 0.5;
      var x0 = stacked ? 0 : Math.ceil(nw + 14), x1 = W - 8;
      // the figures sit across zero from their bars, so each side keeps room for the other side's widest figure
      var pw = x1 - x0, needR = 0, needL = 0;
      rows.forEach(function (r) { var w = c.measure(words(r[ev]), 'label', 400, true) + 8; if (r[ev] < 0) needR = Math.max(needR, w); else needL = Math.max(needL, w); });
      if (nk[0] < 0 && nk[1] / (nk[1] - nk[0]) * pw < needR) nk[1] = needR * -nk[0] / (pw - needR);
      if (nk[1] > 0 && -nk[0] / (nk[1] - nk[0]) * pw < needL) nk[0] = -needL * nk[1] / (pw - needL);
      var xs = K.scale.linear([nk[0], nk[1]], [x0, x1]), xz = xs(0);
      ticks = ticks.filter(function (t) { return t >= nk[0] - 1e-9 && t <= nk[1] + 1e-9; });
      var y = 0;
      // the total in words, set apart above the bars
      if (apart.length && L.apart_words) {
        var at = c.text(0, size, String(L.apart_words).replace('{value}', K.fmt(apart[0][ev], f.value || 'signed:0')), { role: 'label', weight: 700, max: W });
        y = at.bottom + 12;
        c.line(0, y, W, y, { stroke: 'gridline', width: c.t('line-hairline'), mark: false });
        y += 12;
      }
      // the axis: a figure at each step and a hairline down through the bars
      var ty = y + c.size('tick');
      var last_r = -1e9;
      ticks.forEach(function (t) {
        var s = K.fmt(t, f.tick || 'signed:0'), tw = c.measure(s, 'tick');
        var anchor = xs(t) - tw / 2 < 0 ? 'start' : xs(t) + tw / 2 > W ? 'end' : 'middle';
        var l = anchor === 'start' ? xs(t) : anchor === 'end' ? xs(t) - tw : xs(t) - tw / 2;
        if (l < last_r + 8) return;
        c.text(xs(t), ty, s, { role: 'tick', anchor: anchor });
        last_r = l + tw;
      });
      var top = ty + 10, lh = Math.round(size * 1.25), pos = [], cy = top;
      // each row's place first, so the gridlines can go under the bars; a stacked name wider than the drawing wraps
      rows.forEach(function (r) {
        var nl = stacked ? c.wrap(name(r), 'label', W, 600).length : 0;
        var ny = cy + size, by = stacked ? cy + size + lh * (nl - 1) + 6 + (pitch - bh) / 2 : cy + (pitch - bh) / 2;
        pos.push({ ny: ny, by: by });
        cy = stacked ? by + bh + (pitch - bh) / 2 + 2 : cy + pitch;
      });
      var end = cy;
      ticks.forEach(function (t) { if (t !== 0) c.line(xs(t), top, xs(t), end, { stroke: 'gridline', width: c.t('line-hairline'), mark: false }); });
      // the zero line before the names, so the kit clears it behind any name it crosses (round 2 fix pass, BC S1 and AX S2);
      // a short stretch of it is drawn again over each bar, after the bar, so the zero stays crisp where the bars meet it
      c.line(xz, top - 4, xz, end, { stroke: 'baseline', width: c.t('line-baseline'), mark: false });
      rows.forEach(function (r, i) {
        var v = r[ev], by = pos[i].by;
        if (stacked) c.text(0, pos[i].ny, name(r), { role: 'label', weight: 600, max: W - 1 });
        else c.text(0, by + bh / 2 + size * 0.35, name(r), { role: 'label' });
        var xv = xs(v);
        c.rect(Math.min(xz, xv), by, Math.max(Math.abs(xv - xz), 1), bh, { fill: v < 0 ? 'div-1' : 'div-5', kind: 'bar', axis: 'x', zero: xz, data: { key: r[ek], field: ev, value: v } });
        c.line(xz, by - 2, xz, by + bh + 2, { stroke: 'baseline', width: c.t('line-baseline'), mark: false });
        // the figure across zero from its bar
        var tx = v < 0 ? xz + 6 : xz - 6;
        c.text(tx, by + bh / 2 + size * 0.35, words(v), { role: 'label', anchor: v < 0 ? 'start' : 'end', tnum: true, halo: true });
      });
      c.height(end + 4);
    }
  });
})(globalThis.OAChart);
