/* Multi-line with one highlighted, as small multiples (coverage plan 3.3, core; S05). One panel per series on one shared
 * scale; each panel draws its own series in Charcoal over the others in thin Stone, so a reader compares shape and level.
 * A change in the break column between two points starts a new segment, never bridged (R16).
 * encode: x (year or month), y (number), series (category), break (category, optional).
 * labels: panels ([{value, label}] in order), panel_value (words under each panel title with {x} and {y} of its last point),
 * domain ([lo, hi]), columns (panels per row at desktop; 2 on a phone), ticks_x (more years to label on each panel's time
 * axis, such as a break year). formats: x, y, tick.
 * annotations (E13, round 1): a gap bracket, [{"panel": series value, "at": {"x": 2003}, "to_series": series value,
 * "text": "27.3", "unit": "points", "place": "left" or "right"}]: a hairline bracket from the panel's own point at x to the
 * other series' point at the same x, with its words beside it. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'multi-line-highlight', name: 'Small Multiple Lines', family: 'change-over-time',
    encode: { x: 'time', y: 'number', series: 'category', break: 'category?' },
    labels: ['panels', 'panel_value', 'domain', 'columns', 'ticks_x'],
    phone: 'same',
    draw: function (c) {
      var P = K.parts, rows = c.rows, ex = c.field('x'), ey = c.field('y'), es = c.field('series'), eb = c.field('break', false);
      var f = c.spec.formats || {}, W = c.width, L = c.labels;
      var panels = L.panels || [];
      var by = {};
      rows.forEach(function (r) { (by[String(r[es])] = by[String(r[es])] || []).push(r); });
      Object.keys(by).forEach(function (k) { by[k].sort(function (a, b) { return K.time(a[ex]) - K.time(b[ex]); }); });
      var ts = rows.map(function (r) { return K.time(r[ex]); }), tlo = Math.min.apply(null, ts), thi = Math.max.apply(null, ts);
      var vals = rows.map(function (r) { return r[ey]; });
      var dom = L.domain || K.nice(Math.min.apply(null, vals), Math.max.apply(null, vals), 4);
      var cols = c.phone ? 2 : (L.columns || panels.length), gapx = c.phone ? 18 : 26;
      var tk = K.ticks(dom[0], dom[1], 4), gut = 0;
      tk.forEach(function (t, i) { gut = Math.max(gut, c.measure(K.fmt(t, (i === tk.length - 1 && f.tick_last) || f.tick || 'integer'), 'tick') + 12); });
      gut = Math.ceil(gut);
      // the panels leave room for the yearly dot's radius at the right edge
      var pw = Math.floor((W - gut - gapx * (cols - 1) - c.t('dot-small-vertex-radius') - 1) / cols), ph = c.phone ? 110 : 130, head = 46;
      function segs(list) {
        var out = [[]];
        list.forEach(function (r, i) {
          if (i && eb && r[eb] !== list[i - 1][eb] && out[out.length - 1].length) out.push([]);
          if (i && K.time(r[ex]) === K.time(list[i - 1][ex]) && out[out.length - 1].length) out.push([]);
          out[out.length - 1].push(r);
        });
        return out.filter(function (s) { return s.length > 1; });
      }
      var y0 = 0, ticks = K.ticks(dom[0], dom[1], 4);
      panels.forEach(function (pnl, i) {
        var col = i % cols, row = Math.floor(i / cols);
        var px = gut + col * (pw + gapx), py = y0 + row * (ph + head + 34);
        var ys = K.scale.linear(dom, [py + head + ph, py + head]), xs = K.scale.linear([tlo, thi], [px, px + pw]);
        var mine = by[String(pnl.value)] || [];
        var lb = c.text(px, py + c.size('label'), pnl.label, { role: 'label', weight: 600, max: pw });
        if (L.panel_value && mine.length) c.text(px, lb.y + lb.h + c.size('tick') + 2, P.fill(c, L.panel_value, mine[mine.length - 1]), { role: 'tick' });
        ticks.forEach(function (t) {
          c.line(px, ys(t), px + pw, ys(t), { stroke: 'gridline', width: c.t('line-hairline'), mark: false });
          if (col === 0) c.text(gut - 8, ys(t) + c.size('tick') * 0.35, K.fmt(t, (t === ticks[ticks.length - 1] && f.tick_last) || f.tick || 'integer'), { role: 'tick', anchor: 'end' });
        });
        panels.forEach(function (o) {
          if (o.value === pnl.value) return;
          segs(by[String(o.value)] || []).forEach(function (s) {
            c.path(s.map(function (r, j) { return (j ? 'L' : 'M') + K.round(xs(K.time(r[ex]))) + ',' + K.round(ys(r[ey])); }).join(''), { stroke: 'context', width: c.t('line-hairline'), mark: false });
          });
        });
        segs(mine).forEach(function (s) {
          c.path(s.map(function (r, j) { return (j ? 'L' : 'M') + K.round(xs(K.time(r[ex]))) + ',' + K.round(ys(r[ey])); }).join(''), { stroke: 'subject', width: c.t('line-subject'), data: { series: pnl.value } }, [px, py + head, pw, ph]);
        });
        // the panel's own line at the subject's weight with a dot at each year, as Phase 2 drew it (brand KS3)
        mine.forEach(function (r) {
          c.circle(xs(K.time(r[ex])), ys(r[ey]), c.t('dot-small-vertex-radius'), { fill: 'subject', mark: false });
          c.datum(xs(K.time(r[ex])), ys(r[ey]), { data: { key: pnl.value + '|' + r[ex] + (eb ? '|' + r[eb] : ''), field: ey, value: r[ey] } });
        });
        // gap brackets (E13): from this panel's point to another series' point in the same year
        var placed = [];
        (c.spec.annotations || []).filter(function (a) { return String(a.panel) === String(pnl.value) && a.at && a.to_series !== undefined; }).forEach(function (a) {
          var at = K.time(a.at.x), here = mine.filter(function (r) { return K.time(r[ex]) === at; }), there = (by[String(a.to_series)] || []).filter(function (r) { return K.time(r[ex]) === at; });
          if (!here.length || !there.length) { c.warn('annotation: no ' + (here.length ? a.to_series : pnl.value) + ' value at ' + a.at.x); return; }
          var y1 = ys(here[here.length - 1][ey]), y2 = ys(there[there.length - 1][ey]), left = a.place !== 'right';
          // the words stay inside the panel and clear the panel's other bracket words: the unit drops, then the bracket changes
          // side, then the words move along the bracket, in that order
          var full = String(a.text || '') + (a.unit ? ' ' + a.unit : ''), bare = String(a.text || ''), x0 = xs(at), th = c.size('tick');
          var lo = Math.min(y1, y2), hi = Math.max(y1, y2), pick = null;
          [[full, left], [bare, left], [full, !left], [bare, !left]].some(function (cand) {
            return [(y1 + y2) / 2, lo + th * 0.6, hi - th * 0.2, lo - 2, hi + th].some(function (ty) {
              var tw = c.measure(cand[0], 'tick'), tx = cand[1] ? x0 - 9 - tw : x0 + 9, box = { x: tx, y: ty - th, w: tw, h: th * 1.25 };
              if (tx < px || tx + tw > px + pw) return false;
              if (placed.some(function (b) { return box.x < b.x + b.w + 3 && b.x < box.x + box.w + 3 && box.y < b.y + b.h && b.y < box.y + box.h; })) return false;
              pick = { words: cand[0], left: cand[1], y: ty, box: box };
              return true;
            });
          });
          if (!pick) { c.warn('annotation: no room for the bracket words at ' + a.at.x + ' in ' + pnl.value); return; }
          placed.push(pick.box);
          var bx = x0 + (pick.left ? -5 : 5), arm = pick.left ? 3 : -3, w = c.t('line-hairline');
          c.line(bx, y1, bx, y2, { stroke: 'secondary', width: w, mark: false });
          c.line(bx, y1, bx + arm, y1, { stroke: 'secondary', width: w, mark: false });
          c.line(bx, y2, bx + arm, y2, { stroke: 'secondary', width: w, mark: false });
          c.text(bx + (pick.left ? -4 : 4), pick.y, pick.words, { role: 'tick', anchor: pick.left ? 'end' : 'start', halo: true });
        });
        var ay = py + head + ph + c.size('tick') + 6;
        var e0 = c.text(px, ay, K.fmt(tlo, 'year'), { role: 'tick' });
        var e1 = c.text(px + pw, ay, K.fmt(Math.round(thi), 'year'), { role: 'tick', anchor: 'end' });
        // more years on the time axis (KS3: the break year), each only where it clears the end labels
        [].concat(L.ticks_x || []).forEach(function (v) {
          var tx = xs(K.time(v)), t = K.fmt(v, 'year'), hw = c.measure(t, 'tick') / 2;
          if (tx - hw > e0.x + e0.w + 6 && tx + hw < e1.x - 6) {
            c.line(tx, py + head + ph, tx, py + head + ph + 4, { stroke: 'secondary', width: c.t('line-hairline'), mark: false });
            c.text(tx, ay, t, { role: 'tick', anchor: 'middle' });
          }
        });
      });
      var nrows = Math.ceil(panels.length / cols);
      c.height(y0 + nrows * (ph + head + 34) - 10);
    }
  });
})(globalThis.OAChart);
