/* Change lollipop with a size-of-shift key (coverage plan 3.2, core; S24). One shift per item, ranked from the largest:
 * a stem from zero to the change and a dot at its end, with the change printed beside the dot. A key at the top shows the
 * length of one round shift, and the nation's row sits apart above the rest (DR-64). Direction is carried by position and
 * the printed sign; every stem takes the subject ink, so no color codes a side.
 * The change is read from a long table, two rows per item (encode x and y, with labels.from and labels.to naming the two
 * x values), or from a column that holds it (encode value).
 * encode: key (code), label (text), x (year or category, optional), y (number, optional), value (number, optional).
 * labels: from, to (the two x values compared), measure ("percent", the default, or "difference"), apart (the key value
 * set apart above the rest, such as "US"), key (words for the key, with {value}), key_value (the key's shift), value
 * (words beside each dot, with {value}, such as "{value}%"). formats: value (the shift in the words), key (the key's
 * shift), tick (the axis). Maker B, round 1. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'change-lollipop',
    name: 'Change Lollipop',
    family: 'shift-and-swing',
    encode: { key: 'code', label: 'text', x: 'category?', y: 'number?', value: 'number?' },
    labels: ['from', 'to', 'measure', 'apart', 'key', 'key_value', 'value'],
    phone: 'same',
    draw: function (c) {
      var L = c.labels, f = c.spec.formats || {}, W = c.width, ek = c.field('key'), el = c.field('label');
      var ev = c.field('value', false), exx = c.field('x', false), ey = c.field('y', false);
      // one item per key, with its shift
      var items = [], by = {};
      c.rows.forEach(function (r) {
        var k = String(r[ek]);
        if (!by[k]) { by[k] = { key: k, label: r[el], row: r }; items.push(by[k]); }
        if (ev) by[k].value = r[ev];
        else if (String(r[exx]) === String(L.from)) by[k].a = r[ey];
        else if (String(r[exx]) === String(L.to)) by[k].b = r[ey];
      });
      items.forEach(function (it) {
        if (ev) return;
        if (it.a === undefined || it.b === undefined || it.a === null || it.b === null) { it.value = null; c.warn('no pair of values for ' + it.key); return; }
        it.value = L.measure === 'difference' ? it.b - it.a : (it.b / it.a - 1) * 100;
      });
      items = items.filter(function (it) { return it.value !== null && it.value !== undefined; });
      var apart = items.filter(function (it) { return L.apart !== undefined && it.key === String(L.apart); });
      var rest = items.filter(function (it) { return apart.indexOf(it) < 0; }).sort(function (a, b) { return b.value - a.value; });
      var words = function (v) { return String(L.value || '{value}').replace('{value}', K.fmt(v, f.value || 'signed:0')); };
      // the scale: from zero, or from the lowest shift when one falls below it
      var lo = Math.min(0, Math.min.apply(null, items.map(function (it) { return it.value; }))), hi = Math.max(0, Math.max.apply(null, items.map(function (it) { return it.value; })));
      var size = c.size('label'), pitch = Math.max(c.t('shift-axis-pitch'), Math.round(size * 1.4));
      var nw = 0;
      items.forEach(function (it) { nw = Math.max(nw, c.measure(it.label, 'label', it.key === String(L.apart) ? 700 : 400)); });
      var vw = 0;
      items.forEach(function (it) { vw = Math.max(vw, c.measure(words(it.value), 'label', 700, true)); });
      // a name column beside the stems, or each name above its stem where the column would leave the stems too little room
      var stacked = W - nw - 16 - vw - 10 < W * 0.4;
      var x0 = stacked ? 0 : Math.ceil(nw + 16), x1 = W - vw - 10;
      // the axis ends at the largest shift, with a tick at each step inside it, so no empty step trails the longest stem;
      // the finer steps where their figures fit apart (a phone keeps the +100 step a reading guide may name)
      var nk, ticks;
      [4, 3, 2].some(function (n) {
        nk = K.nice(lo, hi, n); ticks = K.ticks(nk[0], hi, 0, nk.step);
        var span = Math.max(hi, ticks[ticks.length - 1]) - nk[0], tw = 0;
        ticks.forEach(function (t) { tw = Math.max(tw, c.measure(K.fmt(t, f.tick || 'signed:0'), 'tick')); });
        return nk.step / span * (x1 - x0) >= tw + 12;
      });
      nk = [nk[0], Math.max(hi, ticks[ticks.length - 1])];
      var xs = K.scale.linear([nk[0], nk[1]], [x0, x1]);
      var y = 0;
      // the size-of-shift key
      if (L.key && L.key_value !== undefined) {
        var kw = String(L.key).replace('{value}', K.fmt(L.key_value, f.key || f.value || 'signed:0'));
        var ky = size;
        c.line(xs(0), ky - size * 0.35, xs(L.key_value), ky - size * 0.35, { stroke: 'subject', width: c.t('arrow-shaft'), mark: false });
        c.circle(xs(L.key_value), ky - size * 0.35, c.t('dot-vertex-radius'), { fill: 'subject', mark: false });
        c.line(xs(0), ky - size * 0.35 - 5, xs(0), ky - size * 0.35 + 5, { stroke: 'baseline', width: c.t('line-hairline'), mark: false });
        var kb = c.text(xs(L.key_value) + 10, ky, kw, { role: 'label', weight: 600 });
        if (kb.x + kb.w > W) c.warn('the key runs past the drawing');
        y = ky + 14;
      }
      // the axis: a tick label at each step, and a hairline down through the rows
      var ty = y + c.size('tick');
      ticks.forEach(function (t) {
        var tw = c.measure(K.fmt(t, f.tick || 'signed:0'), 'tick');
        var anchor = xs(t) - tw / 2 < 0 ? 'start' : xs(t) + tw / 2 > W ? 'end' : 'middle';
        c.text(xs(t), ty, K.fmt(t, f.tick || 'signed:0'), { role: 'tick', anchor: anchor });
      });
      y = ty + 10;
      var grid_top = y, step = stacked ? size + 10 + Math.round(pitch * 0.8) : pitch;
      var grid_end = y + step * (apart.length + rest.length) + (apart.length ? 8 : 0);
      // the gridlines first, under the stems and words
      ticks.forEach(function (t) {
        c.line(xs(t), grid_top, xs(t), grid_end, { stroke: t === 0 ? 'baseline' : 'gridline', width: c.t(t === 0 ? 'line-baseline' : 'line-hairline'), mark: false });
      });
      var row = function (it, bold) {
        var ny = stacked ? y + size : y + pitch / 2 + size * 0.35, ly = stacked ? y + size + 10 : y + pitch / 2;
        // names flush left at the drawing's edge, as the family's long ranked lists set them (brand S13, round 1 fix pass)
        c.text(0, ny, it.label, { role: 'label', weight: bold ? 700 : 400, halo: true });
        var xe = xs(it.value);
        c.line(xs(0), ly, xe, ly, { stroke: 'subject', width: c.t('arrow-shaft'), mark: false });
        c.circle(xe, ly, c.t('dot-vertex-radius'), { fill: 'subject', data: { key: it.key, field: ev || 'change', value: Math.round(it.value * 10) / 10 } });
        var vx = it.value >= 0 ? xe + 8 : xe - 8;
        c.text(vx, ly + size * 0.35, words(it.value), { role: 'label', weight: bold ? 700 : 400, anchor: it.value >= 0 ? 'start' : 'end', tnum: true, halo: true });
        y += step;
      };
      apart.forEach(function (it) { row(it, true); });
      if (apart.length) { c.line(0, y + 3, W, y + 3, { stroke: 'gridline', width: c.t('line-hairline'), mark: false }); y += 8; }
      rest.forEach(function (it) { row(it, false); });
      c.height(y + 4);
    }
  });
})(globalThis.OAChart);
