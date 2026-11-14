/* Columns with a moving average (coverage plan 3.3, core; S14). Monthly values as columns from zero in Stone, the average
 * as a Charcoal line, preliminary months hatched and the average dashed where it includes one, the latest month labeled.
 * encode: x (month), y (number), average (number, optional), status (category, optional; spec.labels.preliminary_value
 * names the value that marks a preliminary month). labels: key_columns, key_preliminary, key_average, latest (one or two
 * lines with {x} and {y}), preliminary_value. formats: x, y (labels), y_tick (axis). annotations: [{at: {x}, text, target:
 * 'average' | 'y' | 'low', place, dx, dy}].
 * Round 5 (R5-4, the data lead's ruling c, opt-in: with neither key the drawing is S14's, byte for byte):
 * labels.named: [{x, text: [line, line], place, dx, dy, phone: {...}}], the columns a title names, in the subject ink, each
 *   with its words (a first line in bold, the rest regular) on a leader, below a loss and above a gain unless place says
 *   otherwise; every other column takes the light fill (the context ink on Charcoal) and the average the context ink at
 *   the context weight, so the named columns alone carry the subject ink. text [] names a column with no words.
 * labels.margin: {value, label, key}, a band from minus to plus value (the y unit) across the plot, behind the columns, in
 *   magnitude step 1 with its 1 px context edges (K.parts.band); label set in the band below zero at the plot's left, key
 *   as its own key entry. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'columns-moving-average',
    name: 'Columns With Moving Average',
    family: 'change-over-time',
    encode: { x: 'month', y: 'number', average: 'number?', status: 'category?' },
    labels: ['key_columns', 'key_preliminary', 'key_average', 'latest', 'preliminary_value', 'named', 'margin'],
    phone: 'same',
    draw: function (c) {
      var P = K.parts, rows = c.rows, ex = c.field('x'), ey = c.field('y'), ea = c.field('average', false), es = c.field('status', false);
      var f = c.spec.formats || {};
      var prelim_value = c.label('preliminary_value', 'preliminary');
      var is_pre = function (r) { return es && r[es] === prelim_value; };
      var W = c.width, y = 0;
      // round 5 (ruling c): the named columns and the margin band, each only where the spec sets it
      var named = c.labels.named ? [].concat(c.labels.named).map(function (n) { return typeof n === 'object' ? n : { x: n, text: [] }; }) : null;
      var nf = named ? P.named_fill(c, named.map(function (n) { return n.x; }), ex) : null;
      var other = c.ground === 'charcoal' ? 'context' : 'light-fill';
      var margin = c.labels.margin && isFinite(+c.labels.margin.value) ? c.labels.margin : null;
      // the key
      var keys = [{ label: c.label('key_columns'), fill: named ? other : 'context' }];
      if (es && rows.some(is_pre) && c.labels.key_preliminary) keys.push({ label: c.labels.key_preliminary, pattern: 'pre', stroke: 'context', direct: true });
      if (ea && c.labels.key_average) keys.push({ label: c.labels.key_average, shape: 'line', stroke: named ? 'context' : 'subject', direct: true });
      if (margin && margin.key) keys.push({ label: margin.key, fill: 'mag-1', edge: 'context' });
      y += c.size('label') + 2;
      y += P.key(c, keys, 0, y, W) + 14;
      // the scale
      var vals = [];
      rows.forEach(function (r) { vals.push(r[ey]); if (ea && r[ea] !== null) vals.push(r[ea]); });
      var lo = Math.min(0, Math.min.apply(null, vals)), hi = Math.max(0, Math.max.apply(null, vals));
      var vs = P.value_scale(c, lo, hi, c.phone ? 4 : 5), ticks = vs.ticks;
      var gut = P.value_gutter(c, ticks, f.y_tick || 'signed');
      var top = y + 30, plotH = c.t(c.phone ? 'columns-phone-height' : 'columns-height'), bot = top + plotH;
      var ys = K.scale.linear([vs.lo, vs.hi], [bot, top]);
      var x0 = gut + 4, x1 = W;
      var n = rows.length, step = (x1 - x0) / n, bw = step * c.t('columns-fill-share');
      var xc = function (i) { return x0 + step * i + step / 2; };
      P.value_grid(c, ys, ticks, f.y_tick || 'signed', x0, x1, gut);
      // the margin: one band across the plot, behind the columns, with its edges; the zero line draws over it
      if (margin) {
        var m = Math.abs(+margin.value);
        P.band(c, [{ x: x0, y0: ys(m), y1: ys(-m) }, { x: x1, y0: ys(m), y1: ys(-m) }], { fill: 'mag-1', edge: 'context' });
      }
      // the columns
      c.pattern('pre', 'context');
      rows.forEach(function (r, i) {
        var v = r[ey], yz = ys(0), yv = ys(v);
        var o = { kind: 'bar', axis: 'y', zero: yz, data: { key: r[ex], field: ey, value: v } };
        if (is_pre(r)) {
          c.rect(xc(i) - bw / 2, Math.min(yz, yv), bw, Math.abs(yv - yz), Object.assign({ pattern: 'pre' }, o));
          c.rect(xc(i) - bw / 2 + 0.5, Math.min(yz, yv) + 0.5, Math.max(0, bw - 1), Math.max(0, Math.abs(yv - yz) - 1), { stroke: 'context', mark: false });
        } else c.rect(xc(i) - bw / 2, Math.min(yz, yv), bw, Math.abs(yv - yz), Object.assign({ fill: nf ? nf(r) : 'context' }, o));
      });
      P.zero_line(c, ys, x0, x1);
      // the average: solid through final months, dashed from the first segment that reaches a preliminary month
      if (ea) {
        var pts = rows.map(function (r, i) { return r[ea] === null ? null : [xc(i), ys(r[ea]), is_pre(r)]; });
        var solid = '', dash = '', prev = null;
        pts.forEach(function (p) {
          if (!p) { prev = null; return; }
          if (prev) {
            var seg = 'M' + K.round(prev[0]) + ',' + K.round(prev[1]) + 'L' + K.round(p[0]) + ',' + K.round(p[1]);
            if (p[2]) dash += seg; else solid += seg;
          }
          prev = p;
        });
        var lw = named ? c.t('line-context') : c.t('columns-average-line'), ink = named ? 'context' : 'subject';
        if (solid) c.path(solid, { stroke: 'surface', width: lw + 2 * c.t('keyline'), mark: false });
        if (solid) c.path(solid, { stroke: ink, width: lw, data: { field: ea } }, [x0, top, x1 - x0, plotH]);
        if (dash) c.path(dash, { stroke: ink, width: lw, dash: '4 3', data: { field: ea, status: prelim_value } }, [x0, top, x1 - x0, plotH]);
      }
      // the time axis
      var tlo = K.time(rows[0][ex]), thi = K.time(rows[n - 1][ex]);
      var xt = function (t) { return x0 + (t - tlo) * 12 * step + (step - bw) / 2; };
      var ay = bot + c.size('tick') + 10;
      if (vs.lo < 0) ay = Math.max(ay, ys(vs.lo) + c.size('tick') + 10);
      P.year_axis(c, xt, tlo, thi, ay, x1);
      var h = ay + 6;
      // the latest month, labeled at the right edge
      var last = rows[n - 1];
      if (c.labels.latest) {
        var lines = [].concat(c.labels.latest).map(function (t) { return P.fill(c, t, last); });
        // in a narrow column the second line wraps, so it stays over the latest months and clear of the tall early columns
        // (D3-904's sweep: 256 to 288 px; placement only)
        if (W < 300) lines = [lines[0]].concat([].concat.apply([], lines.slice(1).map(function (l) { return c.wrap(l, 'tick', Math.round(W * 0.55), 400); })));
        var lx = xc(n - 1), ly = Math.min(ys(last[ey]), ys(0)) - 8;
        var lt = top - 4 + c.size('label');
        var hi_y = Math.min(ly - 12 - (lines.length - 1) * 19, lt);
        c.text(W, hi_y, lines[0], { role: 'label', weight: 700, anchor: 'end', halo: true });
        for (var li = 1; li < lines.length; li++) c.text(W, hi_y + li * 19, lines[li], { role: 'label', weight: 400, anchor: 'end', fill: 'secondary', halo: true, size: c.size('tick') + 1 });
        c.line(lx, hi_y + (lines.length - 1) * 19 + 6, lx, ly, { stroke: 'leader', width: c.t('line-hairline'), mark: false });
      }
      // the margin's words, in the band below zero at the plot's left, where no column of the window reaches
      // (round 5, the maker's request 4): at the plot's left where clear, else the first place along the band clear of every
      // column and word; where none is clear (a narrow drawing), the words stay out and the key names the band
      if (margin && margin.label) {
        var mm = Math.abs(+margin.value), my = (ys(0) + ys(-mm)) / 2 + c.size('tick') * 0.35, mo = { role: 'tick', weight: 600, fill: 'label', alone: true };
        var bars = c.marks.filter(function (mk) { return mk.kind === 'bar' && mk.w > 0 && mk.h > 0; });
        var meets = function (b, t) { return t.x < b.x + b.w + 1 && b.x < t.x + t.w + 1 && t.y < b.y + b.h + 1 && b.y < t.y + t.h + 1; };
        for (var mx = x0 + 6; mx <= x1; mx += Math.max(1, step)) {
          var mb = c.text_box(mx, my, margin.label, mo);
          if (mb.x + mb.w > x1) break;
          if (bars.some(function (b) { return meets(b, mb); }) || c.texts.some(function (t) { return meets(t, mb); })) continue;
          c.text(mx, my, margin.label, mo);
          break;
        }
      }
      // the named columns' words: a first line in bold and the rest regular, on a leader. Each takes the first clear place of:
      // the spec's place (or below a loss, above a gain), then left, right, and above the plot's columns, clear of every
      // word drawn, of every other column and of the time axis; a spec may set place, dx, dy and a phone object
      if (named) named.forEach(function (nm) {
        var lines = [].concat(nm.text || []);
        if (!lines.length) return;
        var narrow = c.phone || W < 490;
        var o = Object.assign({}, nm, narrow && nm.phone ? nm.phone : {});
        if (o.hide) return;
        var i = rows.findIndex(function (r) { return String(r[ex]) === String(nm.x); });
        if (i < 0) { c.warn('named column ' + nm.x + ' matches no row'); return; }
        var v = rows[i][ey], px = xc(i), yz = ys(0), yv = ys(v), lo_y = Math.max(yz, yv), hi_y2 = Math.min(yz, yv);
        var size = c.size('label'), lh = 19, gap = c.t('note-leader-min'), asc = size * 0.969;
        var ws = lines.map(function (l, k) { return c.measure(l, 'label', k ? 400 : 700); }), w = Math.max.apply(null, ws);
        var bh = (lines.length - 1) * lh + size, floor = ay - c.size('tick') - 2;
        var cols = c.marks.filter(function (mk) { return mk.kind === 'bar' && String(mk.data.key) !== String(rows[i][ex]); });
        var hit = function (bx, by) {
          if (bx < 0 || bx + w > W || by < 0 || by + bh > floor) return true;
          var b = { x: bx - 2, y: by - 2, w: w + 4, h: bh + 4 };
          var over = function (t) { return b.x < t.x + t.w && t.x < b.x + b.w && b.y < t.y + t.h && t.y < b.y + b.h; };
          return c.texts.some(over) || cols.some(function (mk) { return mk.h > 0 && over(mk); }) ||
            (c.leaders || []).some(function (l) { return K.leader_crosses(l, b); });
        };
        // the leader from the box's nearest point to the column, which may cross no word already drawn
        var lead = function (bx, by, ax, ay2) {
          var lx = Math.max(bx, Math.min(ax, bx + w)), ly = Math.max(by, Math.min(ay2, by + bh));
          return { x1: lx, y1: ly, x2: ax, y2: ay2 };
        };
        // each place: [box left, box top, anchor point x, y]
        var first = o.place || (v < 0 ? 'below' : 'above');
        var place = function (pl) {
          if (pl === 'below') return [px - w / 2, lo_y + gap, px, lo_y];
          if (pl === 'above') return [px - w / 2, hi_y2 - gap - bh, px, hi_y2];
          if (pl === 'left') return [px - bw / 2 - gap - w, yv - bh / 2, px - bw / 2, yv];
          if (pl === 'right') return [px + bw / 2 + gap, yv - bh / 2, px + bw / 2, yv];
          return null;
        };
        var tries = [first, 'left', 'right', 'above', 'below'].map(place);
        for (var k = 1; k <= 4; k++) [w / 2, w, 0].forEach(function (sh) { tries.push([px - sh, hi_y2 - gap - bh - k * (bh + 8), px, hi_y2]); });
        var pick = null;
        tries.forEach(function (t) {
          if (pick || !t) return;
          var bx = t[0] + (o.dx || 0), by = t[1] + (o.dy || 0), L = lead(bx, by, t[2], t[3]);
          if (!hit(bx, by) && !c.texts.some(function (tx) { return K.leader_crosses(L, tx); })) pick = [bx, by, t[2], t[3]];
        });
        // no clear place: the words stay out of the drawing and the build says so; a spec hides them at this width (phone:
        // {hide: true}) and prints them in phone_notes, as S14's in-plot note does
        if (!pick) { c.warn('no clear place for the words of ' + nm.x + ' at ' + W + ' px; hide them here (phone: {hide: true}) and print them in phone_notes'); return; }
        var boxes = lines.map(function (l, k) { return c.text(pick[0] + w / 2, pick[1] + asc + k * lh, l, { role: 'label', weight: k ? 400 : 700, anchor: 'middle', halo: true }); });
        var L = lead(pick[0], pick[1], pick[2], pick[3]);
        if (Math.abs(L.x1 - L.x2) + Math.abs(L.y1 - L.y2) > 4) c.line(L.x1, L.y1, L.x2, L.y2, { stroke: 'leader', width: c.t('line-hairline'), mark: false });
      });
      // notes inside the plot
      c.annotations.forEach(function (a) {
        // a column under 490 px takes a note's phone setting too: there the note's words would sit on the tall early columns
        // (D3-904's sweep: 480 to 489 px; placement only)
        var narrow = c.phone || W < 490;
        if (narrow && a.phone && a.phone.hide) return;
        a = Object.assign({}, a, narrow && a.phone ? a.phone : {});
        var i = rows.findIndex(function (r) { return String(r[ex]) === String(a.at.x); });
        if (i < 0) { c.warn('annotation at ' + a.at.x + ' matches no row'); return; }
        var r = rows[i], py;
        if (a.target === 'average' && ea) py = ys(r[ea]);
        else if (a.target === 'low') py = ys(Math.min(0, r[ey]));
        else py = ys(r[ey]);
        P.note(c, xc(i), py, a.text, { place: a.place, dx: a.dx, dy: a.dy, max: a.max });
      });
      c.height(h);
    }
  });
})(globalThis.OAChart);
