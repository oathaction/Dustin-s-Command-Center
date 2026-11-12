/* Implementation timeline (coverage plan 3.3, core; S32). When each part of a law or rule takes effect, as phase-in bars:
 * one row per part in date order, its words over a lane, and a bar from the date the part starts to the chart's end. A part
 * that reaches each plan or program only when its own year begins is hatched for its first year (labels.phase_months),
 * then solid. A deadline is a dot on its date with no bar. The date the law was approved runs as a line down every
 * lane, dashed, and is named at the top.
 * encode: date (date), title (text: the row's first words), text (text, optional: the row's plain summary), kind
 * (category). labels: kinds ({kind value: "approved" | "deadline" | "phase" | "start"}; "start" by default), approved
 * (words at the approval line, with {date}), phase_months (12 by default), end (the date the axis ends), phase_key,
 * start_key, deadline_key (the key's words), row_title, row_text (each row's words from a template with {date} and any
 * encode or column name, in place of the title and text columns), words ({stored value: printed words}). formats: date (in the words, "date" by default).
 * Maker B, round 1. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'implementation-timeline',
    name: 'Implementation Timeline',
    family: 'change-over-time',
    encode: { date: 'date', title: 'text', text: 'text?', kind: 'category' },
    labels: ['kinds', 'approved', 'phase_months', 'end', 'phase_key', 'start_key', 'deadline_key', 'row_title', 'row_text', 'words'],
    phone: 'same',
    draw: function (c) {
      var P = K.parts, L = c.labels, f = c.spec.formats || {}, W = c.width;
      var ed = c.field('date'), et = c.field('title'), ex = c.field('text', false), ek = c.field('kind');
      // labels.words prints a stored value in other words (such as a curled apostrophe) before it fills a row's template
      var wr = function (r) { var o = {}, W2 = L.words || {}; for (var k in r) o[k] = typeof r[k] === 'string' && W2[r[k]] !== undefined ? W2[r[k]] : r[k]; return o; };
      var tw = function (r) { return L.row_title ? P.fill(c, L.row_title, wr(r)) : String(wr(r)[et]); };
      var xw = function (r) { return L.row_text ? P.fill(c, L.row_text, wr(r)) : ex ? String(wr(r)[ex] || '') : ''; };
      var kind = function (r) { return (L.kinds || {})[String(r[ek])] || 'start'; };
      var rows = c.rows.slice().sort(function (a, b) { return K.time(a[ed]) - K.time(b[ed]); });
      var appr = rows.filter(function (r) { return kind(r) === 'approved'; })[0];
      var parts = rows.filter(function (r) { return kind(r) !== 'approved'; });
      var t0 = K.time(rows[0][ed]), tend = L.end ? K.time(L.end) : Math.floor(K.time(rows[rows.length - 1][ed])) + 1;
      var x0 = 0, x1 = W - 2, xs = K.scale.linear([Math.floor(t0), tend], [x0, x1]);
      var size = c.size('label'), lh = Math.round(size * 1.3), bh = 12, phase = (L.phase_months || 12) / 12;
      var y = 0;
      // the key
      c.pattern('phase', 'context');
      var keys = [];
      if (L.start_key) keys.push({ label: L.start_key, fill: 'context' });
      if (L.phase_key && parts.some(function (r) { return kind(r) === 'phase'; })) keys.push({ label: L.phase_key, pattern: 'phase', stroke: 'context', direct: true });
      if (L.deadline_key && parts.some(function (r) { return kind(r) === 'deadline'; })) keys.push({ label: L.deadline_key, shape: 'dot', fill: 'subject', direct: true });
      if (keys.length) { y += size + 2; y += P.key(c, keys, 0, y, W) + 8; }
      // the approval date's words over the axis, at its line
      var xp = appr ? xs(K.time(appr[ed])) : null;
      if (appr && L.approved) {
        var aw = String(L.approved).replace('{date}', K.fmt(appr[ed], f.date || 'date'));
        var at = c.text(Math.min(xp + 6, W - c.measure(aw, 'tick', 600)), y + c.size('tick'), aw, { role: 'tick', weight: 600, max: W });
        y = at.bottom + 6;
      }
      // the year axis along the top, with a hairline down at each January
      var ay = y + c.size('tick'), yrs = [];
      for (var yr = Math.ceil(Math.floor(t0) - 1e-9); yr <= tend + 1e-9; yr++) yrs.push(yr);
      yrs.forEach(function (yr) {
        var w = c.measure(String(yr), 'tick'), x = xs(yr), anchor = x + w > W ? 'end' : 'start';
        if (yr < tend) c.text(x + (anchor === 'start' ? 3 : 0), ay, String(yr), { role: 'tick', anchor: anchor });
      });
      var top = ay + 8;
      // each row's place first: its words, then its lane, so the lines can go under the words
      var pos = [], cy = top + 10, lhl = Math.round(size * 1.25);
      parts.forEach(function (r) {
        var nh = c.wrap(tw(r), 'label', W - 1, 700).length, ty = cy + size, by = ty + lhl * (nh - 1) + c.size('label') * 0.241 + 2, xy = null;
        if (xw(r)) { xy = by + size * 0.95; by = xy + lhl * (c.wrap(xw(r), 'label', W - 1, 400).length - 1) + c.size('label') * 0.241 + 2; }
        pos.push({ r: r, ty: ty, xy: xy, by: by + 4 });
        cy = by + 4 + bh + 16;
      });
      var end = cy - 8;
      // the year lines and the approval line cross the lanes only, never the words over them
      yrs.forEach(function (yr) { c.line(xs(yr), top - 4, xs(yr), top + 2, { stroke: 'gridline', width: c.t('line-hairline'), mark: false }); });
      if (appr) c.datum(xp, top, { data: { key: appr[ed] + '|' + appr[et], field: ed, value: appr[ed] } });
      pos.forEach(function (p) {
        var r = p.r, k = kind(r), xa = xs(K.time(r[ed]));
        c.text(0, p.ty, tw(r), { role: 'label', weight: 700, max: W - 1, halo: true, leading: lhl });
        if (p.xy !== null) c.text(0, p.xy, xw(r), { role: 'label', max: W - 1, halo: true, leading: lhl });
        // the lane under the bar, so the reader sees where a part has not started, with the year lines across it
        c.rect(x0, p.by, x1 - x0, bh, { fill: 'track', mark: false });
        yrs.forEach(function (yr) { if (yr > Math.floor(t0) && yr < tend) c.line(xs(yr), p.by - 4, xs(yr), p.by + bh + 4, { stroke: 'gridline', width: c.t('line-hairline'), mark: false }); });
        if (appr) c.line(xp, p.by - 4, xp, p.by + bh + 4, { stroke: 'subject', width: c.t('line-hairline') * 1.5, dash: '2 2', mark: false });
        if (k === 'deadline') {
          c.circle(xa, p.by + bh / 2, bh / 2 + 2, { fill: 'subject', data: { key: r[ed] + '|' + r[et], field: ed, value: r[ed] } });
          return;
        }
        if (k === 'phase') {
          var xb = Math.min(x1, xs(K.time(r[ed]) + phase));
          c.rect(xa, p.by, xb - xa, bh, { pattern: 'phase', data: { key: r[ed] + '|' + r[et], field: ed, value: r[ed] } });
          c.rect(xa + 0.5, p.by + 0.5, xb - xa - 1, bh - 1, { stroke: 'context', mark: false });
          if (xb < x1) c.rect(xb, p.by, x1 - xb, bh, { fill: 'context', mark: false });
        } else c.rect(xa, p.by, x1 - xa, bh, { fill: 'context', data: { key: r[ed] + '|' + r[et], field: ed, value: r[ed] } });
        c.line(xa, p.by - 3, xa, p.by + bh + 3, { stroke: 'subject', width: 2, mark: false });
      });
      c.height(end + 2);
    }
  });
})(globalThis.OAChart);
