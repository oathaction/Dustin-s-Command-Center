/* Beeswarm or strip plot (coverage plan 3.5, core; S50). Every item as one dot on one value scale, the dots packed up and
 * down from a center line so none hides another; the packing is computed from the data alone, in value order, so it is
 * the same in Node and every browser. One row may be drawn as a reference line across the swarm (labels.reference),
 * dashed in the text's ink and named above it in regular weight (the data lead's ruling (b)). Named items take the
 * subject ink (or the red point) against the light fill and carry their name and value over or under the swarm on a
 * leader; where a side's names cannot sit apart on one line, each takes two, its value under it. The value axis runs
 * along the bottom.
 * encode: key (code), label (text), value (number).
 * labels: reference (key of the row drawn as a line), reference_label (words over it, with {value}), named (keys in the
 * subject ink, each named), point (the one key in the red point, named), names ({key: printed name}), place ({key: "above"
 * or "below"}: which side of the swarm a name sits; alternate sides otherwise), value (a named item's words, with {label}
 * and {value}; default "{label} {value}"), axis (words under the value axis).
 * formats: value, tick. scale: x ([lo, hi]). On a phone the same arrangement draws narrower, so the swarm grows taller.
 * Maker B, round 2. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'beeswarm',
    name: 'Beeswarm',
    family: 'distribution-and-density',
    encode: { key: 'code', label: 'text', value: 'number' },
    labels: ['reference', 'reference_label', 'named', 'point', 'names', 'place', 'value', 'axis'],
    phone: 'same',
    draw: function (c) {
      var P = K.parts, L = c.labels, f = c.spec.formats || {}, W = c.width, ph = c.phone;
      var ek = c.field('key'), el = c.field('label'), ev = c.field('value'), names = L.names || {}, place = L.place || {};
      var fv = f.value || 'integer', ft = f.tick || fv, tick = c.size('tick'), size = c.size('label');
      var ref = L.reference === undefined || L.reference === null ? null : String(L.reference);
      var refrow = ref === null ? null : c.rows.filter(function (r) { return String(r[ek]) === ref; })[0] || null;
      if (ref !== null && !refrow) c.warn('labels.reference names no row: ' + ref);
      var rows = c.rows.filter(function (r) { return r !== refrow; });
      var ink = P.named_fill(c, L.named, ek, 'subject', L.point);
      var lit = rows.filter(function (r) { return ink.named && ink.is_named(r) || ink.is_point(r); });
      var name = function (r) { var k = String(r[ek]); return names[k] !== undefined ? names[k] : String(r[el]); };
      var words = function (r) { return String(L.value || '{label} {value}').replace('{label}', name(r)).replace('{value}', K.fmt(r[ev], fv)); };
      var vals = c.rows.map(function (r) { return r[ev]; });
      var sx = (c.spec.scale || {}).x, dom = sx || K.nice(Math.min.apply(null, vals), Math.max.apply(null, vals), W < 300 ? 3 : ph ? 4 : 6);
      var rd = c.t(ph ? 'dot-open-radius' : 'dot-subject-radius'), gap = 1.5, D = 2 * rd + gap;
      var xs = K.scale.linear([dom[0], dom[1]], [rd + 2, W - rd - 2]);
      // the packing: each dot, in value order, takes the place nearest the center line where it touches no dot placed before
      var placed = [];
      rows.slice().sort(function (a, b) { return a[ev] - b[ev] || String(a[ek]).localeCompare(String(b[ek])); }).forEach(function (r) {
        var x = xs(r[ev]), bans = [];
        placed.forEach(function (p) { var dx = Math.abs(p.x - x); if (dx < D) { var h = Math.sqrt(D * D - dx * dx); bans.push([p.y - h, p.y + h]); } });
        var cands = [0];
        bans.forEach(function (b) { cands.push(b[0], b[1]); });
        cands.sort(function (a, b) { return Math.abs(a) - Math.abs(b) || a - b; });
        var y = cands.filter(function (y0) { return bans.every(function (b) { return y0 <= b[0] + 1e-6 || y0 >= b[1] - 1e-6; }); })[0];
        placed.push({ r: r, x: x, y: y });
      });
      var ext = Math.max.apply(null, placed.map(function (p) { return Math.abs(p.y); })) + rd;
      // the named items' words, over the swarm and under it, each kept apart from its neighbor on that side
      var lab = { above: [], below: [] }, alt = 0;
      placed.filter(function (p) { return lit.indexOf(p.r) >= 0; }).sort(function (a, b) { return a.x - b.x; }).forEach(function (p) {
        var side = place[String(p.r[ek])] || (alt++ % 2 ? 'below' : 'above');
        var w = c.measure(words(p.r), 'label', 700);
        lab[side].push({ p: p, w: w, x: Math.min(Math.max(p.x, w / 2), W - w / 2) });
      });
      // spread each side's names apart; where they still touch, each name takes two lines, its value under it
      var spread = function (ls) {
        for (var pass = 0; pass < 40; pass++) {
          var moved = false;
          for (var i = 1; i < ls.length; i++) {
            var o = ls[i - 1].x + ls[i - 1].w / 2 + 12 - (ls[i].x - ls[i].w / 2);
            if (o > 0.1) { ls[i - 1].x -= o / 2; ls[i].x += o / 2; moved = true; }
          }
          ls.forEach(function (l) { var nx = Math.min(Math.max(l.x, l.w / 2), W - l.w / 2); if (Math.abs(nx - l.x) > 0.01) { l.x = nx; moved = true; } });
          if (!moved) break;
        }
        return ls.every(function (l, i) { return !i || ls[i - 1].x + ls[i - 1].w / 2 + 11 <= l.x - l.w / 2; });
      };
      var two = { above: false, below: false };
      ['above', 'below'].forEach(function (s) {
        if (spread(lab[s])) return;
        two[s] = true;
        lab[s].forEach(function (l) { l.w = Math.max(c.measure(name(l.p.r), 'label', 700), c.measure(K.fmt(l.p.r[ev], fv), 'label', 700)); l.x = Math.min(Math.max(l.p.x, l.w / 2), W - l.w / 2); });
        spread(lab[s]);
      });
      var y = 0;
      if (refrow && L.reference_label) y += tick + 6;
      var lead = 14, lh = Math.round(size * 1.2), rowA = lab.above.length ? size + lead + (two.above ? lh : 0) : 0;
      var cy = y + rowA + ext + 6, bottom = cy + ext + 6;
      // the reference line through the swarm, with its words over everything
      if (refrow) {
        var rx = xs(refrow[ev]);
        if (L.reference_label) { var rw = P.fill(c, L.reference_label, refrow), rww = c.measure(rw, 'tick'); c.text(Math.min(Math.max(rx, rww / 2), W - rww / 2), tick, rw, { role: 'tick', anchor: 'middle', fill: 'label' }); }
        // the line stops short of any named item's words it would cross, and starts again past them (BC S1, AX S2)
        var ya = y, yb = bottom + (lab.below.length ? lead : 0), gaps = [];
        [['above', y + size], ['below', bottom + lead + size * 0.75]].forEach(function (sd) {
          var s = sd[0], base = sd[1], hh = s === 'above' ? (two.above ? lh : 0) : (two.below ? lh : 0);
          lab[s].forEach(function (l) { if (rx >= l.x - l.w / 2 - 3 && rx <= l.x + l.w / 2 + 3) gaps.push([base - size * 0.969 - 3, base + hh + size * 0.25 + 3]); });
        });
        gaps.sort(function (a, b) { return a[0] - b[0]; });
        var segs = [], at = ya;
        gaps.forEach(function (g) { if (g[0] > at) segs.push([at, Math.min(g[0], yb)]); at = Math.max(at, g[1]); });
        if (yb > at) segs.push([at, yb]);
        segs.sort(function (a, b) { return (b[1] - b[0]) - (a[1] - a[0]); }).forEach(function (sg, i) {
          P.total_line(c, rx, sg[0], rx, sg[1], i ? { width: c.t('line-baseline') } : { width: c.t('line-baseline'), data: { key: refrow[ek], field: ev, value: refrow[ev] } });
        });
      }
      // leaders first, so the dots sit over them
      var ly = { above: y + size, below: bottom + lead + size * 0.75 };
      var hgt = { above: two.above ? lh : 0, below: two.below ? lh : 0 };
      ['above', 'below'].forEach(function (s) {
        lab[s].forEach(function (l) {
          var py = cy + l.p.y, ty = s === 'above' ? ly.above + hgt.above + 4 : ly.below - size * 0.75 - 4;
          var end = s === 'above' ? py - rd - 1 : py + rd + 1;
          if (s === 'above' ? ty < end : ty > end) c.line(l.p.x, ty, l.p.x, end, { stroke: 'leader', width: c.t('line-hairline'), mark: false });
        });
      });
      placed.forEach(function (p) {
        c.circle(p.x, cy + p.y, rd, Object.assign({ fill: ink(p.r), data: { key: p.r[ek], field: ev, value: p.r[ev] } }, ink.keyline(p.r)));
      });
      ['above', 'below'].forEach(function (s) {
        lab[s].forEach(function (l) {
          if (two[s]) {
            c.text(l.x, ly[s], name(l.p.r), { role: 'label', weight: 700, anchor: 'middle' });
            c.text(l.x, ly[s] + lh, K.fmt(l.p.r[ev], fv), { role: 'label', weight: 700, anchor: 'middle', tnum: true });
          } else c.text(l.x, ly[s], words(l.p.r), { role: 'label', weight: 700, anchor: 'middle' });
        });
      });
      // the value axis along the bottom
      var ab = (lab.below.length ? ly.below + hgt.below + 10 : bottom + 4), ticks = K.ticks(dom[0], dom[1], W < 300 ? 3 : ph ? 4 : 6);
      c.line(xs(dom[0]), ab, xs(dom[1]), ab, { stroke: 'baseline', width: c.t('line-hairline'), mark: false });
      ticks.forEach(function (t, i) {
        c.line(xs(t), ab, xs(t), ab + 4, { stroke: 'baseline', width: c.t('line-hairline'), mark: false });
        var tw = c.measure(K.fmt(t, ft), 'tick'), tx = xs(t), an = tx - tw / 2 < 0 ? 'start' : tx + tw / 2 > W ? 'end' : 'middle';
        c.text(an === 'start' ? 0 : an === 'end' ? W : tx, ab + tick + 8, K.fmt(t, ft), { role: 'tick', anchor: an });
      });
      var end = ab + tick + 12;
      if (L.axis) { var xb = c.text(0, end + tick + 2, L.axis, { role: 'tick', weight: 600, max: W }); end = xb.bottom; }
      c.height(end + 2);
    }
  });
})(globalThis.OAChart);
