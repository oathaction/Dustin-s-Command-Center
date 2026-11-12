/* Line with event notes (coverage plan 3.3, core; S02). One subject series in Charcoal, others in Stone, each labeled on the
 * line; a break in the series is drawn as a gap, never bridged (R16); notes sit inside the plot with leaders.
 * encode: x (year, month or date), y (number), series (category, optional), break (category, optional: a row whose value is
 * labels.break_end ends a segment, labels.break_start starts one; either may be one value or a list of values, and at one x
 * a row that ends a segment sorts first and a row that starts one sorts last, ED-E8). labels: subject (the series value drawn in Charcoal),
 * series ({value: name}), series_place ({value: {x, dy}}), break_end, break_start, y_max (number). formats: y, y_tick.
 * annotations: [{at: {x, series}, text, place, dx, dy, max, dot, value}] — "value": true prints the point's value.
 * Round 2 (ED-E14): labels.point names the series the title names in the working red, its line and vertex dots one job
 * (the view's one red) on the 1 px keyline on Newsprint; labels.named names series set in the subject ink. With either
 * set, every other series takes the light fill on Newsprint and the context ink on Charcoal (palette rule R3,
 * K.parts.named_fill); with neither, labels.subject draws as before. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'line-event-notes',
    name: 'Line With Event Notes',
    family: 'change-over-time',
    encode: { x: 'time', y: 'number', series: 'category?', break: 'category?' },
    labels: ['subject', 'series', 'series_place', 'break_end', 'break_start', 'y_max', 'series_key', 'point', 'named'],
    phone: 'same',
    draw: function (c) {
      var P = K.parts, rows = c.rows, ex = c.field('x'), ey = c.field('y'), es = c.field('series', false), eb = c.field('break', false);
      var f = c.spec.formats || {}, W = c.width;
      var names = c.labels.series || {}, subj = c.labels.subject;
      // ED-E14: the role of each series, by labels.point and labels.named through the shared light fill; with neither,
      // the subject in ink and the rest in the context ink, as before
      var nf = (c.labels.point !== undefined && c.labels.point !== null) || (c.labels.named !== undefined && c.labels.named !== null)
        ? P.named_fill(c, c.labels.named, 'k', null, c.labels.point) : null;
      var role = function (k) { return nf ? nf({ k: k }) : (!es || k === String(subj) ? 'subject' : 'context'); };
      var heavy = function (k) { var r = role(k); return r === 'point' || r === 'subject'; };
      var groups = {}, order = [];
      rows.forEach(function (r) { var k = es ? String(r[es]) : '_'; if (!groups[k]) { groups[k] = []; order.push(k); } groups[k].push(r); });
      var ts = rows.map(function (r) { return K.time(r[ex]); });
      var tlo = Math.min.apply(null, ts), thi = Math.max.apply(null, ts);
      var vmax = Math.max.apply(null, rows.map(function (r) { return r[ey]; }));
      var vs = P.value_scale(c, 0, c.labels.y_max || vmax, c.phone ? 4 : 5), ticks = vs.ticks;
      var keyed = c.phone && c.labels.series_key === 'phone' && es;
      var top0 = 0;
      if (keyed) {
        top0 = c.size('label') + 2;
        // the subject's line first in the key, as the title is about it
        var kord = order.filter(function (k) { return names[k]; });
        kord.sort(function (a, b) { return heavy(b) - heavy(a); });
        top0 += P.key(c, kord.map(function (k) {
          var sj = heavy(k);
          return { label: names[k], shape: 'line', stroke: role(k), width: c.t(sj ? 'line-subject' : 'line-context'), direct: true };
        }), 0, top0, W) + 8;
      }
      var top = top0 + c.size('tick') + 6, plotH = c.phone ? 260 * 1 : 300;
      plotH = c.t(c.phone ? 'columns-phone-height' : 'columns-height');
      var bot = top + plotH;
      var gut = P.value_gutter(c, ticks, f.y_tick || 'number');
      var x0 = gut + 8, x1 = W - (c.phone ? 8 : 16);
      var ys = K.scale.linear([vs.lo, vs.hi], [bot, top]), xs = K.scale.linear([tlo, thi], [x0, x1]);
      P.value_grid(c, ys, ticks, f.y_tick || 'number', x0, x1, gut);
      P.zero_line(c, ys, x0, x1);
      // segments: a break_end row closes the line; a break_start row opens a new one
      var as_set = function (v) { return v === undefined || v === null ? [] : [].concat(v).map(String); };
      var be = as_set(c.labels.break_end), bs = as_set(c.labels.break_start);
      var ends = function (r) { return !!eb && r[eb] !== null && r[eb] !== undefined && be.indexOf(String(r[eb])) >= 0; };
      var starts = function (r) { return !!eb && r[eb] !== null && r[eb] !== undefined && bs.indexOf(String(r[eb])) >= 0; };
      var rank = function (r) { return ends(r) ? 0 : starts(r) ? 2 : 1; };
      order.forEach(function (k) {
        var g = groups[k].slice().sort(function (a, b) {
          var d = K.time(a[ex]) - K.time(b[ex]);
          if (d) return d;
          // at one x, the row that closes a segment first and the row that opens the next last
          return rank(a) - rank(b);
        });
        var segs = [[]];
        g.forEach(function (r) {
          if (starts(r) && segs[segs.length - 1].length) segs.push([]);
          segs[segs.length - 1].push(r);
          if (ends(r)) segs.push([]);
        });
        var is_subj = heavy(k), rk = role(k), red = rk === 'point', kl = red && c.ground !== 'charcoal' ? c.t('keyline') : 0;
        // the red series' lines and dots are one job, the view's one working red (Rule 05.3, ED-E14)
        var grp = red ? c.group({ job: 'point' }) : null;
        segs.filter(function (s) { return s.length; }).forEach(function (s) {
          var d = s.map(function (r, i) { return (i ? 'L' : 'M') + K.round(xs(K.time(r[ex]))) + ',' + K.round(ys(r[ey])); }).join('');
          if (s.length > 1) {
            if (is_subj) c.path(d, { stroke: 'surface', width: c.t('line-subject') + 2 * c.t('keyline') + 2 * kl, mark: false });
            if (kl) c.path(d, { stroke: 'point-keyline', width: c.t('line-subject') + 2 * kl, mark: false });
            c.path(d, { stroke: rk, width: c.t(is_subj ? 'line-subject' : 'line-context'), data: { series: k } }, [x0, top, x1 - x0, plotH]);
          }
          s.forEach(function (r) {
            c.circle(xs(K.time(r[ex])), ys(r[ey]), c.t(is_subj ? 'dot-vertex-radius' : 'dot-small-vertex-radius'), Object.assign({ fill: rk, data: { key: (es ? r[es] + '|' : '') + r[ex] + (eb ? '|' + r[eb] : ''), field: ey, value: r[ey] } },
              kl ? { stroke: 'point-keyline', width: kl } : {}));
          });
        });
        if (grp) grp.end();
        // the series name on the line
        if (es && names[k] && !keyed) {
          var pl = (c.labels.series_place || {})[k] || {};
          var at = pl.x !== undefined ? g.filter(function (r) { return String(r[ex]) === String(pl.x); })[0] : g[0];
          if (at) c.text(xs(K.time(at[ex])) + (pl.dx || 0), ys(at[ey]) + (pl.dy === undefined ? -12 : pl.dy), names[k], { role: 'label', weight: 600, fill: is_subj ? 'label' : 'secondary', halo: true, anchor: pl.anchor || 'start' });
        }
      });
      // the time axis: one label per tick year, thinned to fit
      var ay = bot + c.size('tick') + 8, step = 1;
      var wmax = c.measure('0000', 'tick') + 16;
      while (xs(tlo + step) - xs(tlo) < wmax) step++;
      if (step > 1 && step < 4 && (thi - tlo) % 4 === 0) step = 4;
      for (var yr = Math.ceil(tlo); yr <= thi; yr += step) {
        var yw = c.measure(String(yr), 'tick');
        c.text(xs(yr) + yw / 2 > W ? W : xs(yr), ay, String(yr), { role: 'tick', anchor: xs(yr) + yw / 2 > W ? 'end' : 'middle' });
      }
      var below = [];
      c.annotations.forEach(function (a) {
        if (c.phone && a.phone && a.phone.hide) return;
        if (c.phone && a.text && !a.value && ((a.phone && a.phone.below) || (!(a.phone && a.phone.below === false) && a.text.length > 60))) { below.push(a.text); return; }
        var hit = rows.filter(function (r) { return String(r[ex]) === String(a.at.x) && (!es || a.at.series === undefined || String(r[es]) === String(a.at.series)) && (!eb || !a.at.break || r[eb] === a.at.break); })[0];
        if (!hit) { c.warn('annotation at ' + JSON.stringify(a.at) + ' matches no row'); return; }
        var px = xs(K.time(hit[ex])), py = ys(hit[ey]);
        if (a.dot) c.circle(px, py, c.t('dot-subject-radius'), { fill: 'subject', mark: false });
        var o = Object.assign({}, a, c.phone && a.phone ? a.phone : {});
        var words = a.value ? K.fmt(hit[ey], f.y || 'number') + (a.text ? a.text : '') : a.text;
        P.note(c, px, py, words, { place: o.place, dx: o.dx, dy: o.dy, max: o.max, weight: a.value ? 700 : 400, anchor: o.anchor, leader: o.leader });
      });
      var by = ay + 14;
      below.forEach(function (t) {
        var b = c.text(0, by + c.size('note'), t, { role: 'note', max: W });
        by = b.y + b.h + 10;
      });
      c.height(below.length ? by : ay + 4);
    }
  });
})(globalThis.OAChart);
