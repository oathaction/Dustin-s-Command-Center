/* Dot plot (coverage plan 3.1, core; S19). Many items on one scale, one row each: the name at the left, a dot at the
 * value, every value printed in a column at the right edge. One row may be drawn as a reference line across the plot in
 * place of a dot (labels.reference names its key), labeled once above the rows. Rows whose status equals labels.open take an
 * open dot, explained by a key above the rows. Ticks and light gridlines run along the bottom.
 * encode: key (code), label (text), value (number), status (category, optional).
 * labels: reference (the key drawn as a line), reference_label (words over the line, with {value}), open (the status value
 * drawn as an open dot), key_open (the key's words for an open dot), named (keys whose names print bold), names ({key: printed name}).
 * formats: value, tick. scale: x ([lo, hi]). On a phone the same arrangement draws at a narrower plot.
 * IM-E5 (round 4, the data lead's five conditions): inside a social card (c.card, R4-4) with ranks "across", each row is a
 * column left to right in the rows' order, the value scale vertical with S19's domain and ticks at the left, the reference
 * row a dashed line across with its words where no dot falls, only the named rows labeled (beside their dots, clear of
 * every other dot), each dot at most its column's pitch less 2 px across at the card's true size and an open ring at least
 * 2.8 px, 2 px or more between dots; a named dot with no clear place beside it labeled in a band under the zero line on a
 * hairline leader (IM-E6); the plot fills c.card.height. It warns where it cannot meet that. Outside a card the form draws as
 * before. */
(function (K) {
  'use strict';
  function across(c, rows, refrow, o) {
    var W = c.width, H = c.card.height, L = c.labels, k = (c._m && c._m[0]) || 1, size = c.size('label'), tick = c.size('tick'), y = 0;
    var dom = (c.spec.scale || {}).x || K.nice(0, Math.max.apply(null, c.rows.map(function (r) { return r[o.ev]; })), 6), ticks = K.ticks(dom[0], dom[1], 6);
    if (rows.some(o.is_open) && L.key_open) {
      var kr = c.t('dot-open-radius');
      y += size + 2;
      c.circle(kr + 1, y - size * 0.35, kr, { fill: 'surface', mark: false });
      c.circle(kr + 1, y - size * 0.35, kr, { stroke: 'subject', width: c.t('line-context'), mark: false });
      // inside the card's scaled group c.text returns the card's coordinates, so the key is measured in the form's own
      var ko = { role: 'label', max: W - 2 * kr - 10 };
      c.text(2 * kr + 10, y, L.key_open, ko);
      y += Math.round(size * 1.25) * (c.text_box(2 * kr + 10, y, L.key_open, ko).lines - 1) + 14;
      c.key([{ fill: 'subject', direct: true }, { fill: 'surface', pattern: true }]);
    }
    var tw = Math.max.apply(null, ticks.map(function (t) { return c.measure(K.fmt(t, o.f.tick || 'integer'), 'tick'); }));
    var x0 = Math.ceil(tw + 8), py0 = y + size + 8, py1, ys, dots, n = rows.length, pitch = (W - x0) / n;
    // IM-E6: a gap of 2 px or more at true size between dots, after each center is written to 0.1 of a unit
    var R = Math.floor((pitch - 2 / k - 0.1) * 50) / 100, sw = Math.max(2.8 / k + 0.1, Math.min(c.t('line-context'), R * 0.35));
    if (R - sw < 0.5) c.warn('card: ' + n + ' columns leave no room for an open dot\u2019s ring at ' + Math.round(pitch * k * 10) / 10 + ' px a column');
    var lay = function (band) {
      py1 = H - 2 - band; ys = K.scale.linear([dom[0], dom[1]], [py1, py0]);
      dots = rows.map(function (r, i) { return { r: r, x: x0 + (i + 0.5) * pitch, y: ys(r[o.ev]) }; });
    };
    lay(0);
    // a place for words clear of every dot (1 px), inside the drawing and right of the scale, and of words placed before
    var placed = [], clear = function (b) {
      return b.x >= x0 && b.x + b.w <= W && b.y >= 0 && b.y + b.h <= H && !placed.some(function (p) { return b.x < p.x + p.w && p.x < b.x + b.w && b.y < p.y + p.h && p.y < b.y + b.h; }) &&
        !dots.some(function (d) { var nx = Math.max(b.x, Math.min(d.x, b.x + b.w)), ny = Math.max(b.y, Math.min(d.y, b.y + b.h)); return Math.hypot(nx - d.x, ny - d.y) < R + 1; });
    };
    var spot = function (words, spots, opt, draw) {
      for (var i = 0; i < spots.length; i++) {
        var s = spots[i], so = Object.assign({ anchor: s[2] }, opt), b = c.text_box(s[0], s[1], words, so);
        // DD-I21: the words clear the gridlines under them (a 1 px knockout of the ground; every spot is 1 px clear of the dots)
        if (clear(b)) { if (draw) { placed.push(b); K.parts.clear_label(c, s[0], s[1], words, Object.assign({ gap: 1 }, so)); } return true; }
      }
      return false;
    };
    var up = size * 0.241 + 3, dn = size * 0.969 + 3, LO = { role: 'label', weight: 700, fill: 'label' };
    var spots = function (d) { return [[d.x - R, d.y - R - up, 'start'], [d.x + R, d.y - R - up, 'end'], [d.x + R, d.y + R + dn, 'end'], [d.x - R, d.y + R + dn, 'start'],
      [d.x + R + 4, d.y + size * 0.35, 'start'], [d.x - R - 4, d.y + size * 0.35, 'end']]; };
    var lab = function (d) { return o.name(d.r) + ' ' + o.val(d.r); }, isn = function (d) { return o.named.indexOf(String(d.r[o.ek])) >= 0; };
    // IM-E6 (the data lead, 21:32): a named dot with no clear place beside it takes a band one label tall under the zero line,
    // its words there alone, on a hairline leader to 2 px short of its dot
    var low = dots.filter(function (d) { return isn(d) && !spot(lab(d), spots(d), LO); }).map(function (d) { return d.r; });
    if (low.length) lay(Math.ceil(size * 1.25) + 6);
    ticks.forEach(function (t) {
      c.line(x0, ys(t), W, ys(t), { stroke: 'gridline', width: c.t('line-hairline'), mark: false });
      c.text(x0 - 6, ys(t) + tick * 0.35, K.fmt(t, o.f.tick || 'integer'), { role: 'tick', anchor: 'end' });
    });
    if (refrow) c.line(x0, ys(refrow[o.ev]), W, ys(refrow[o.ev]), { stroke: 'label', width: c.t('line-baseline'), dash: '4 3', data: { key: refrow[o.ek], field: o.ev, value: refrow[o.ev] } });
    dots.forEach(function (d) {
      if (!isn(d)) return;
      if (low.indexOf(d.r) < 0) { if (!spot(lab(d), spots(d), LO, true)) c.warn('card: no place clear of the dots for "' + lab(d) + '"'); return; }
      var by = H - 2 - size * 0.241, b = c.text_box(d.x + R, by, lab(d), Object.assign({ anchor: 'end' }, LO));
      if (!clear(b)) { c.warn('card: no place clear of the dots for "' + lab(d) + '", in the band under the zero line'); return; }
      placed.push(b);
      c.line(d.x, b.y - 1, d.x, d.y + R + 2 / k, { stroke: 'leader', width: c.t('line-hairline'), mark: false });
      c.text(d.x + R, by, lab(d), Object.assign({ anchor: 'end' }, LO));
    });
    if (refrow && L.reference_label) {
      var ry = ys(refrow[o.ev]), words = K.parts.fill(c, L.reference_label, refrow);
      if (!spot(words, [[W, ry - 5 - tick * 0.241, 'end'], [x0, ry - 5 - tick * 0.241, 'start'], [W, ry + 5 + tick * 0.969, 'end'], [x0, ry + 5 + tick * 0.969, 'start']], { role: 'tick', weight: 600, fill: 'label' }, true))
        c.warn('card: no place clear of the dots for "' + words + '"');
    }
    dots.forEach(function (d) {
      if (o.is_open(d.r)) {
        c.circle(d.x, d.y, R - sw / 2, { fill: 'surface', data: { key: d.r[o.ek], field: o.ev, value: d.r[o.ev] } });
        c.circle(d.x, d.y, R - sw / 2, { stroke: 'subject', width: sw, mark: false });
      } else c.circle(d.x, d.y, R, { fill: 'subject', data: { key: d.r[o.ek], field: o.ev, value: d.r[o.ev] } });
    });
    c.height(H);
  }
  K.register_chart({
    form: 'dot-plot',
    name: 'Dot Plot',
    family: 'comparison',
    encode: { key: 'code', label: 'text', value: 'number', status: 'category?' },
    labels: ['reference', 'reference_label', 'open', 'key_open', 'named', 'names'],
    phone: 'same',
    draw: function (c) {
      var P = K.parts, ek = c.field('key'), el = c.field('label'), ev = c.field('value'), es = c.field('status', false);
      var f = c.spec.formats || {}, W = c.width, L = c.labels, names = L.names || {};
      var ref = L.reference === undefined ? null : String(L.reference);
      var named = [].concat(L.named || []).map(String);
      var rows = c.rows.filter(function (r) { return String(r[ek]) !== ref; });
      var refrow = ref === null ? null : c.rows.filter(function (r) { return String(r[ek]) === ref; })[0];
      if (ref !== null && !refrow) c.warn('labels.reference names no row: ' + ref);
      var is_open = function (r) { return es && L.open !== undefined && String(r[es]) === String(L.open); };
      var name = function (r) { return names[String(r[ek])] !== undefined ? names[String(r[ek])] : String(r[el]); };
      var val = function (r) { return K.fmt(r[ev], f.value || 'integer'); };
      if (c.card && c.card.ranks === 'across') return across(c, rows, refrow, { ek: ek, ev: ev, f: f, named: named, name: name, val: val, is_open: is_open });
      var size = c.size('label'), tick = c.size('tick'), pitch = Math.round(size * 1.5), y = 0;
      // the key, when any row takes an open dot: the open dot and its words (a filled dot needs none)
      if (rows.some(is_open) && L.key_open) {
        var kr = c.t('dot-open-radius');
        y += size + 2;
        c.circle(kr + 1, y - size * 0.35, kr, { fill: 'surface', mark: false });
        c.circle(kr + 1, y - size * 0.35, kr, { stroke: 'subject', width: c.t('line-context'), mark: false });
        var kb = c.text(2 * kr + 10, y, L.key_open, { role: 'label', max: W - 2 * kr - 10 });
        y = kb.bottom - size * 0.241 + 14;
        c.key([{ fill: 'subject', direct: true }, { fill: 'surface', pattern: true }]);   // the open dot reads by its outline
      }
      // the name column and the value column
      var lw = 0, vw = 0;
      rows.forEach(function (r) { lw = Math.max(lw, c.measure(name(r), 'label', named.indexOf(String(r[ek])) >= 0 ? 700 : 400)); vw = Math.max(vw, c.measure(val(r), 'label', 600, true)); });
      var x0 = Math.ceil(lw + (c.phone ? 12 : 20)), x1 = W - Math.ceil(vw + (c.phone ? 12 : 20));
      var vals = c.rows.map(function (r) { return r[ev]; });
      var sx = (c.spec.scale || {}).x, dom = sx || K.nice(Math.min(0, Math.min.apply(null, vals)), Math.max.apply(null, vals), c.phone ? 3 : 6);
      var xs = K.scale.linear([dom[0], dom[1]], [x0 + 8, x1 - 8]);
      // the reference line's words above the rows, kept inside the plot
      if (refrow && L.reference_label) {
        var words = P.fill(c, L.reference_label, refrow), ww = c.measure(words, 'tick', 600);
        y += tick;
        c.text(Math.min(Math.max(xs(refrow[ev]), x0 + ww / 2), W - ww / 2), y, words, { role: 'tick', weight: 600, anchor: 'middle', fill: 'label' });
        y += 10;
      }
      var top = y, r_dot = c.t('dot-open-radius');
      var bottom = top + rows.length * pitch;
      // gridlines at the ticks, then the reference line, then the rows over them
      var ticks = K.ticks(dom[0], dom[1], c.phone ? 3 : 6);
      ticks.forEach(function (t) { c.line(xs(t), top, xs(t), bottom, { stroke: 'gridline', width: c.t('line-hairline'), mark: false }); });
      if (refrow) c.line(xs(refrow[ev]), top - 4, xs(refrow[ev]), bottom, { stroke: 'label', width: c.t('line-baseline'), dash: '4 3', data: { key: refrow[ek], field: ev, value: refrow[ev] } });
      rows.forEach(function (r, i) {
        var cy = top + i * pitch + pitch / 2, ty = cy + size * 0.35, b = named.indexOf(String(r[ek])) >= 0;
        c.text(0, ty, name(r), { role: 'label', weight: b ? 700 : 400 });
        var x = xs(r[ev]);
        if (is_open(r)) {
          c.circle(x, cy, r_dot, { fill: 'surface', data: { key: r[ek], field: ev, value: r[ev] } });
          c.circle(x, cy, r_dot, { stroke: 'subject', width: c.t('line-context'), mark: false });
        } else c.circle(x, cy, r_dot, { fill: 'subject', data: { key: r[ek], field: ev, value: r[ev] } });
        c.text(W, ty, val(r), { role: 'label', weight: b ? 700 : 600, anchor: 'end', tnum: true });
      });
      // the scale along the bottom
      var ay = bottom + tick + 8;
      ticks.forEach(function (t, i) {
        c.line(xs(t), bottom, xs(t), bottom + 4, { stroke: 'baseline', width: c.t('line-hairline'), mark: false });
        c.text(xs(t), ay, K.fmt(t, i === ticks.length - 1 && f.tick_last ? f.tick_last : (f.tick || 'integer')), { role: 'tick', anchor: 'middle' });
      });
      c.height(ay + 4);
    }
  });
})(globalThis.OAChart);
