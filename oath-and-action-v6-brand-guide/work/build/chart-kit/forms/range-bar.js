/* Range bar or error bar (coverage plan 3.7, core; S57; Rule 14.9's plate, ED-E4). An estimate with its interval for each
 * row: the name flush left, a thin line across the interval, a dot at the estimate, the estimate printed in a column at the
 * right edge. The interval's level is named in the measure line ("90 percent margin of error"), never in the drawing.
 * One row may be drawn as a reference across the rows (labels.reference): a line at its estimate, with a light band
 * across its own interval where the spec asks, named once above the rows. A row whose interval and the reference's
 * leave their gap inside the gap's own margin (the square root of the sum of the two squared margins, Rule 14.9) takes an
 * open dot when labels.test is "reference"; or a status column with labels.open names the open rows.
 * encode: category (text), value (number), low and high (numbers), or margin (number: low and high are value less and
 * plus it), key (code, optional: the row's key for labels; category otherwise), status (category, optional).
 * labels: reference (key of the row drawn across the rows), reference_label (words over its line, with {value}),
 * reference_dash (true: the line dashed), reference_band (true: a light band across the reference's own interval),
 * test ("reference": open dots computed from the margins), open (a status value drawn open), key_filled, key_open and
 * key_interval (a key above the rows, each entry left out when its words are), named (keys whose name and value print
 * bold, in the subject ink against the light fill), point (the one key in the red point), names ({key: printed name}),
 * short ({key: name printed on a phone}), value (the right column's words, with {value}, {margin}, {low}, {high};
 * default {value}). formats: value (also margin, low and high unless their own are set), tick. scale: x ([lo, hi]).
 * The value scale is ticked along the bottom, and along the top as well past 20 rows. On a phone the same arrangement draws
 * at a narrower plot. Maker B, round 2. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'range-bar',
    name: 'Range Bar',
    family: 'uncertainty-and-estimates',
    encode: { category: 'text', value: 'number', low: 'number?', high: 'number?', margin: 'number?', key: 'code?', status: 'category?' },
    labels: ['reference', 'reference_label', 'reference_dash', 'reference_band', 'test', 'open', 'key_filled', 'key_open', 'key_interval', 'named', 'point', 'names', 'short', 'value'],
    interval: true,
    phone: 'same',
    draw: function (c) {
      var P = K.parts, L = c.labels, f = c.spec.formats || {}, W = c.width, ph = c.phone;
      var ec = c.field('category'), ev = c.field('value'), elo = c.field('low', false), ehi = c.field('high', false), em = c.field('margin', false);
      var ek = c.field('key', false) || ec, es = c.field('status', false), names = L.names || {};
      if (!em && !(elo && ehi)) c.warn('range-bar needs encode.margin, or encode.low and encode.high');
      // each row's estimate and interval through the kit's shared reading (R2-C1, R2-C2), so the drawing and the checks agree
      var iv = P.interval_of(c);
      var lo = function (r) { return iv(r).lo; }, hi = function (r) { return iv(r).hi; }, half = function (r) { return iv(r).m; };
      var ref = L.reference === undefined || L.reference === null ? null : String(L.reference);
      var refrow = ref === null ? null : c.rows.filter(function (r) { return String(r[ek]) === ref; })[0] || null;
      if (ref !== null && !refrow) c.warn('labels.reference names no row: ' + ref);
      var rows = c.rows.filter(function (r) { return r !== refrow; });
      var ink = P.named_fill(c, L.named, ek, 'subject', L.point);
      var bold = function (r) { return ink.named && ink.is_named(r) || ink.is_point(r); };
      // open dots: a status the spec names, or a gap to the reference inside the gap's own margin (Rule 14.9)
      var is_open = function (r) {
        if (es && L.open !== undefined) return String(r[es]) === String(L.open);
        if (L.test === 'reference' && refrow) return !iv.differs(r, refrow);
        return false;
      };
      var fv = f.value || 'number:1';
      var fill = function (r) {
        var m = half(r), set = { value: [r[ev], fv], margin: [m, f.margin || fv], low: [lo(r), f.low || fv], high: [hi(r), f.high || fv] };
        return String(L.value || '{value}').replace(/\{([a-z0-9_]+)\}/g, function (_, k) { return set[k] ? K.fmt(set[k][0], set[k][1]) : K.fmt(r[c.encode[k] || k], f[k] || 'text'); });
      };
      var short = L.short || {};
      var name = function (r) { var k = String(r[ek]); return ph && short[k] !== undefined ? short[k] : names[k] !== undefined ? names[k] : String(r[ec]); };
      var size = c.size('label'), tick = c.size('tick'), pitch = Math.round(size * (ph ? 1.6 : 1.5)), rd = c.t('dot-subject-radius'), y = 0;
      // the key above the rows: a filled dot, an open dot and an interval, each with its words
      var kents = [];
      if (L.key_filled) kents.push({ kind: 'filled', words: L.key_filled });
      if (L.key_open) kents.push({ kind: 'open', words: L.key_open });
      if (L.key_interval) kents.push({ kind: 'interval', words: L.key_interval });
      if (kents.length) {
        var kx = 0, ky = size, sw = 22, kgap = ph ? 12 : 24;
        kents.forEach(function (e) {
          var ww = sw + 8 + c.measure(e.words, 'label');
          if (kx > 0 && kx + ww > W) { kx = 0; ky += Math.round(size * 1.5); }
          var cy = ky - size * 0.35;
          if (e.kind === 'interval') {
            c.line(kx, cy, kx + sw, cy, { stroke: 'context', width: c.t('line-context'), mark: false });
          } else if (e.kind === 'open') {
            c.circle(kx + sw / 2, cy, rd, { fill: 'surface', mark: false });
            c.circle(kx + sw / 2, cy, rd, { stroke: 'subject', width: c.t('line-context'), mark: false });
          } else c.circle(kx + sw / 2, cy, rd, { fill: 'subject', mark: false });
          var tb = c.text(kx + sw + 8, ky, e.words, { role: 'label', max: W - kx - sw - 8 });
          kx += Math.min(ww, W) + kgap;
          ky = Math.max(ky, tb.bottom - size * 0.241);
        });
        c.key([{ fill: 'subject', direct: true }, { fill: 'surface', pattern: true }]);
        y = ky + Math.round(size * 0.9);
      }
      // the name column and the value column
      var lw = 0, vw = 0;
      rows.forEach(function (r) { var b = bold(r) ? 700 : 400; lw = Math.max(lw, c.measure(name(r), 'label', b)); vw = Math.max(vw, c.measure(fill(r), 'label', b === 700 ? 700 : 600, true)); });
      var x0 = Math.ceil(lw + (ph ? 10 : 20)), x1 = W - Math.ceil(vw + (ph ? 10 : 20));
      var all = c.rows.map(lo).concat(c.rows.map(hi));
      var sx = (c.spec.scale || {}).x, dom = sx || K.nice(Math.min.apply(null, all), Math.max.apply(null, all), ph ? 3 : 6);
      var pad = rd + 2, xs = K.scale.linear([dom[0], dom[1]], [x0 + pad, x1 - pad]);
      var ticks = K.ticks(dom[0], dom[1], ph ? 3 : 6), tf = f.tick || 'integer';
      // the reference's words above the rows, kept inside the drawing
      if (refrow && L.reference_label) {
        var words = P.fill(c, L.reference_label, refrow), ww2 = c.measure(words, 'tick', 600);
        y += tick;
        c.text(Math.min(Math.max(xs(refrow[ev]), ww2 / 2), W - ww2 / 2), y, words, { role: 'tick', weight: 600, anchor: 'middle', fill: 'label' });
        y += 8;
      }
      var top_axis = rows.length > 20;
      if (top_axis) {
        y += tick;
        ticks.forEach(function (t) { c.text(xs(t), y, K.fmt(t, tf), { role: 'tick', anchor: 'middle' }); });
        y += 8;
      }
      var top = y + 4, bottom = top + rows.length * pitch;
      // gridlines, the reference's band and line, then the rows over them
      ticks.forEach(function (t) { c.line(xs(t), top, xs(t), bottom, { stroke: 'gridline', width: c.t('line-hairline'), mark: false }); });
      if (refrow) {
        var bl = xs(lo(refrow)), bh = xs(hi(refrow));
        if (L.reference_band && bh - bl >= 1.5) c.rect(bl, top, bh - bl, bottom - top, { fill: 'band', mark: false });
        c.line(xs(refrow[ev]), top - 4, xs(refrow[ev]), bottom, { stroke: 'label', width: c.t('line-baseline'), dash: L.reference_dash ? '4 3' : undefined, data: { key: refrow[ek], field: ev, value: refrow[ev] } });
      }
      rows.forEach(function (r, i) {
        var cy = top + i * pitch + pitch / 2, ty = cy + size * 0.35, b = bold(r), role = ink(r), k = r[ek];
        c.text(0, ty, name(r), { role: 'label', weight: b ? 700 : 400 });
        var a = xs(lo(r)), z = xs(hi(r)), x = xs(r[ev]);
        var wst = role === 'subject' || role === 'point' ? 'context' : role;
        P.whisker(c, a, z, cy, { dir: 'h', stroke: wst, key: k, low: lo(r), high: hi(r) });
        if (is_open(r)) {
          c.circle(x, cy, rd, { fill: 'surface', data: { key: k, field: ev, value: r[ev] } });
          c.circle(x, cy, rd, { stroke: role, width: c.t('line-context'), mark: false });
        } else c.circle(x, cy, rd, Object.assign({ fill: role, data: { key: k, field: ev, value: r[ev] } }, ink.keyline(r)));
        c.text(W, ty, fill(r), { role: 'label', weight: b ? 700 : 600, anchor: 'end', tnum: true });
      });
      // the scale along the bottom
      var ay = bottom + tick + 8;
      ticks.forEach(function (t) {
        c.line(xs(t), bottom, xs(t), bottom + 4, { stroke: 'baseline', width: c.t('line-hairline'), mark: false });
        c.text(xs(t), ay, K.fmt(t, tf), { role: 'tick', anchor: 'middle' });
      });
      c.height(ay + 4);
    }
  });
})(globalThis.OAChart);
