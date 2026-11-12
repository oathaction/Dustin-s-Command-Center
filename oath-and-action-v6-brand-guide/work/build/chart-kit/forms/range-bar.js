/* Range bar or error bar (coverage plan 3.7, core; S57; Rule 14.9's plate, ED-E4). An estimate with its interval for each
 * row: the name flush left, a thin line across the interval, a dot at the estimate, the estimate printed in a column at the
 * right edge. The interval's level is named in the measure line ("90 percent margin of error"), never in the drawing.
 * One row may be drawn as a reference across the rows (labels.reference): a line dashed in the text's ink at its estimate
 * (the data lead's ruling (b)), with a light band across its own interval where the spec asks, named once above the rows
 * in regular weight. A row whose interval and the reference's
 * leave their gap inside the gap's own margin (the square root of the sum of the two squared margins, Rule 14.9) takes an
 * open dot when labels.test is "reference"; or a status column with labels.open names the open rows.
 * encode: category (text), value (number), low and high (numbers), or margin (number: low and high are value less and
 * plus it), key (code, optional: the row's key for labels; category otherwise), status (category, optional).
 * labels: reference (key of the row drawn across the rows), reference_label (words over its line, with {value}),
 * reference_band (true: a light band across the reference's own interval),
 * test ("reference": open dots computed from the margins), open (a status value drawn open), key_filled, key_open and
 * key_interval (a key above the rows, each entry left out when its words are), named (keys whose name and value print
 * bold, in the subject ink against the light fill), point (the one key in the red point), names ({key: printed name}),
 * short ({key: name printed on a phone}), value (the right column's words, with {value}, {margin}, {low}, {high};
 * default {value}), stack_below (px: the plot's width under which the rows stack; default 160).
 * formats: value (also margin, low and high unless their own are set), tick. scale: x ([lo, hi]).
 * The value scale is ticked along the bottom, and along the top as well past 20 rows. Where the name and value columns would
 * leave the plot narrower than labels.stack_below, the rows stack (ED-E16): each row's name and value on one line, its
 * interval across the full width on the line beneath, the gridlines and the reference only through the interval lines, and
 * the scale ticked at the top and the bottom; the drawing then reports the phone arrangement (c.arrange). Where the middle
 * row's interval would still hide behind a 13 px dot, every row takes a 7 px dot; where it would hide behind that too, the
 * interval lines go and each margin prints beside its value with a note under the drawing (labels.margin_note to reword
 * it); the form then calls c.margins_in_words() and marks each margin (margin_of) and the note (margin_note) for the kit's
 * interval check (the data lead's RF-25; the engineer's names).
 * Maker B, round 2. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'range-bar',
    name: 'Range Bar',
    family: 'uncertainty-and-estimates',
    encode: { category: 'text', value: 'number', low: 'number?', high: 'number?', margin: 'number?', key: 'code?', status: 'category?' },
    labels: ['reference', 'reference_label', 'reference_band', 'test', 'open', 'key_filled', 'key_open', 'key_interval', 'named', 'point', 'names', 'short', 'value', 'stack_below', 'margin_note'],
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
      // the name column and the value column; where they would leave the plot under labels.stack_below px (160 by
      // default), the rows stack: each row's name and value on one line and its interval across the full width on the line
      // beneath, on one shared scale (ED-E16), and the drawing reports its phone arrangement (R2-C4)
      var lw = 0, vw = 0;
      // names and values in one weight, 400, and 700 for a row the title names (K.parts.row_name, BC S8, call 11)
      rows.forEach(function (r) { var b = P.row_weight(bold(r)); lw = Math.max(lw, c.measure(name(r), 'label', b)); vw = Math.max(vw, c.measure(fill(r), 'label', b, true)); });
      var x0 = Math.ceil(lw + (ph ? 10 : 20)), x1 = W - Math.ceil(vw + (ph ? 10 : 20));
      var stack = x1 - x0 < (L.stack_below || 160);
      if (stack) { x0 = 0; x1 = W; c.arrange('phone'); }
      var all = c.rows.map(lo).concat(c.rows.map(hi));
      var sx = (c.spec.scale || {}).x, nt = stack ? 4 : ph ? (W < 300 ? 3 : 4) : 6, dom = sx || K.nice(Math.min.apply(null, all), Math.max.apply(null, all), nt);
      var pad = rd + 2, xs = K.scale.linear([dom[0], dom[1]], [x0 + pad, x1 - pad]);
      // RF-25 (the data lead, after the second pass; the access reviewer's N2): where the middle row's interval would not run
      // 5 px past a 13 px dot on each side at this width, every row takes a 7 px dot; where it would not run 5 px past even
      // that, the form draws no interval lines and prints each margin beside its value, with a note under the drawing. Never
      // a tick in place of the dot, which carries Rule 14.9's test, and never a wider interval or scale.
      var med_run = function () { var v = rows.map(function (r) { return xs(hi(r)) - xs(lo(r)); }).sort(function (a, b) { return a - b; }); var n = v.length; return n ? (n % 2 ? v[(n - 1) / 2] : (v[n / 2 - 1] + v[n / 2]) / 2) : Infinity; };
      var state = 'lines';
      if (med_run() + 1e-6 < 2 * rd + 10) {
        rd = 3.5; pad = rd + 2; xs = K.scale.linear([dom[0], dom[1]], [x0 + pad, x1 - pad]); state = 'small';
        if (med_run() + 1e-6 < 2 * rd + 10) state = 'margins';
      }
      var mtxt = function (r) { return '\u00b1' + K.fmt(half(r), f.margin || fv); };
      if (state === 'margins' && !stack) {
        // the value column widens for the margins, so the plot narrows to fit them
        vw = 0;
        rows.forEach(function (r) { var b = P.row_weight(bold(r)); vw = Math.max(vw, c.measure(fill(r), 'label', b, true) + 5 + c.measure(mtxt(r), 'label', 400, true)); });
        x1 = W - Math.ceil(vw + (ph ? 10 : 20));
        xs = K.scale.linear([dom[0], dom[1]], [x0 + pad, x1 - pad]);
      }
      if (state === 'margins') c.margins_in_words();   // the kit's interval check then asks for every margin and the note (RF-25)
      // the key above the rows: a filled dot, an open dot and an interval, each with its words
      var kents = [];
      if (L.key_filled) kents.push({ kind: 'filled', words: L.key_filled });
      if (L.key_open) kents.push({ kind: 'open', words: L.key_open });
      if (L.key_interval && state !== 'margins') kents.push({ kind: 'interval', words: L.key_interval });
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

      var ticks = K.ticks(dom[0], dom[1], 0, K.nice(dom[0], dom[1], nt).step), tf = f.tick || 'integer';
      var tick_at = function (t) { var w = c.measure(K.fmt(t, tf), 'tick'), x = xs(t); return { x: Math.min(Math.max(x, w / 2), W - w / 2) }; };
      // the reference's words above the rows, kept inside the drawing
      if (refrow && L.reference_label) {
        // with the margins in words, the reference's words carry its margin too (RF-25)
        var words = P.fill(c, L.reference_label, refrow) + (state === 'margins' ? ' ' + mtxt(refrow) : ''), ww2 = c.measure(words, 'tick');
        y += tick;
        c.text(Math.min(Math.max(xs(refrow[ev]), ww2 / 2), W - ww2 / 2), y, words, { role: 'tick', anchor: 'middle', fill: 'label', margin_of: state === 'margins' ? refrow[ek] : undefined });
        y += 8;
      }
      var top_axis = rows.length > 20 || stack;
      if (top_axis) {
        y += tick;
        ticks.forEach(function (t) { c.text(tick_at(t).x, y, K.fmt(t, tf), { role: 'tick', anchor: 'middle' }); });
        y += 8;
      }
      var line_gap = 5, spitch = Math.round(size + line_gap + 2 * rd + 10);
      var top = y + 4, bottom = top + rows.length * (stack ? spitch : pitch);
      var dot_y = function (i) { return stack ? top + i * spitch + size + line_gap + rd + 2 : top + i * pitch + pitch / 2; };
      // gridlines, the reference's band and line, then the rows over them; stacked, each runs only through the rows'
      // interval lines, so no line crosses a name
      var seg = function (x) {
        if (!stack) return 'M' + K.round(x) + ',' + K.round(top) + 'V' + K.round(bottom);
        return rows.map(function (r, i) { return 'M' + K.round(x) + ',' + K.round(dot_y(i) - rd - 2) + 'V' + K.round(dot_y(i) + rd + 2); }).join('');
      };
      ticks.forEach(function (t) { c.path(seg(K.snap(xs(t), 1)), { stroke: 'gridline', width: c.t('line-hairline'), mark: false }); });
      if (refrow) {
        var bl = xs(lo(refrow)), bh = xs(hi(refrow)), rx = xs(refrow[ev]);
        if (L.reference_band && bh - bl >= 1.5 && !stack) c.rect(bl, top, bh - bl, bottom - top, { fill: 'band', mark: false });
        if (!stack) P.total_line(c, rx, top - 4, rx, bottom, { data: { key: refrow[ek], field: ev, value: refrow[ev] } });
        else rows.forEach(function (r, i) {
          P.total_line(c, rx, dot_y(i) - rd - 3, rx, dot_y(i) + rd + 3, i ? {} : { data: { key: refrow[ek], field: ev, value: refrow[ev] } });
        });
      }
      rows.forEach(function (r, i) {
        var cy = dot_y(i), ty = stack ? top + i * spitch + size : cy + size * 0.35, b = bold(r), role = ink(r), k = r[ek];
        P.row_name(c, 0, ty, name(r), { named: b });
        var a = xs(lo(r)), z = xs(hi(r)), x = xs(r[ev]);
        var wst = role === 'subject' || role === 'point' ? 'context' : role;
        if (state !== 'margins') P.whisker(c, a, z, cy, { dir: 'h', stroke: wst, key: k, low: lo(r), high: hi(r) });
        if (is_open(r)) {
          c.circle(x, cy, rd, { fill: 'surface', data: { key: k, field: ev, value: r[ev] } });
          c.circle(x, cy, rd, { stroke: role, width: state === 'lines' ? c.t('line-context') : 1.5, mark: false });
        } else c.circle(x, cy, rd, Object.assign({ fill: role, data: { key: k, field: ev, value: r[ev] } }, ink.keyline(r)));
        if (state === 'margins') {
          // each margin printed beside its value, as its own words so the check can count them (RF-25)
          var mw = mtxt(r), mwid = c.measure(mw, 'label', 400, true);
          P.row_value(c, W - mwid - 5, ty, fill(r), { named: b });
          c.text(W, ty, mw, { role: 'label', weight: 400, anchor: 'end', tnum: true, margin_of: k });
        } else P.row_value(c, W, ty, fill(r), { named: b });
      });
      // the scale along the bottom
      var ay = bottom + tick + 8;
      ticks.forEach(function (t) {
        c.line(xs(t), bottom, xs(t), bottom + 4, { stroke: 'baseline', width: c.t('line-hairline'), mark: false });
        c.text(tick_at(t).x, ay, K.fmt(t, tf), { role: 'tick', anchor: 'middle' });
      });
      var hend = ay + 4;
      if (state === 'margins') {
        var nb = c.text(0, hend + c.size('note') + 8, L.margin_note || 'At this width each margin of error is narrower than its dot, so each figure prints its margin beside it; the table gives every margin.', { role: 'note', max: W, fill: 'secondary', margin_note: true });
        hend = nb.bottom;
      }
      c.height(hend + 2);
    }
  });
})(globalThis.OAChart);
