/* Oath & Action chart kit: drawing parts the forms share (a key, a value axis, a time axis, notes with leaders).
 * Load after kit.js. Every part draws through the form's context, so the layout guard and the checks see it. */
(function (root) {
  'use strict';
  var K = root.OAChart;
  var P = K.parts = {};

  // A key in one row that wraps: [{label, fill, stroke, pattern, shape: 'square'|'line'|'dot', direct}]. Returns its height.
  P.key = function (c, entries, x, y, maxw) {
    var size = c.size('label'), sw = Math.round(size * 0.9), gap = 24, lh = Math.round(size * 1.5);
    var cx = x, cy = y, first = true;
    entries.forEach(function (e) {
      var w = sw + 8 + c.measure(e.label, 'label'), wrapmax = null;
      if (!first && cx + w > x + maxw) { cx = x; cy += lh; }
      // an entry wider than the key's whole width wraps under its own words (D3-93)
      if (w > maxw) { wrapmax = maxw - sw - 8; w = maxw; }
      var top = cy - sw + 2;
      if (e.shape === 'line') c.line(cx, top + sw / 2, cx + sw, top + sw / 2, { stroke: e.stroke || e.fill, width: e.width || c.t('line-subject'), dash: e.dash, mark: false });
      else if (e.shape === 'dot') c.circle(cx + sw / 2, top + sw / 2, sw / 2.4, { fill: e.fill, mark: false });
      else {
        if (e.pattern) { c.pattern(e.pattern, e.stroke || 'subject'); c.rect(cx, top, sw, sw, { pattern: e.pattern, mark: false }); c.rect(cx + 0.5, top + 0.5, sw - 1, sw - 1, { stroke: e.stroke || 'subject', mark: false }); }
        else if (!e.fill && e.stroke) { c.rect(cx + 0.5, top + 0.5, sw - 1, sw - 1, { fill: e.open ? 'surface' : 'none', mark: false }); c.rect(cx + 0.5, top + 0.5, sw - 1, sw - 1, { stroke: e.stroke, dash: e.dash, mark: false }); }
        else c.rect(cx, top, sw, sw, { fill: e.fill, mark: false });
      }
      var tb = c.text(cx + sw + 8, cy, e.label, { role: 'label', max: wrapmax || undefined });
      if (wrapmax) cy = tb.bottom - size * 0.241;   // the last line's baseline
      cx += w + gap;
      first = false;
    });
    // an entry told apart by its outline, dash or hatch is marked, as a pattern is; the lightness test leaves it out
    c.key(entries.map(function (e) { return { fill: e.fill || e.stroke, pattern: !!(e.pattern || e.dash || e.open || (!e.fill && e.stroke) || e.shape === 'line'), direct: !!e.direct }; }));
    return cy - y + lh;
  };

  // Horizontal gridlines with value labels in a left gutter. Returns the gutter width.
  P.tick_fmt = function (c, ticks, i, fmt) {
    var f = c.spec.formats || {};
    return i === ticks.length - 1 && f.y_tick_top ? f.y_tick_top : fmt;
  };
  P.value_gutter = function (c, ticks, fmt) {
    var w = 0;
    ticks.forEach(function (v, i) { w = Math.max(w, c.measure(K.fmt(v, P.tick_fmt(c, ticks, i, fmt)), 'tick', 400, true)); });
    return Math.ceil(w + 8);
  };
  P.value_grid = function (c, ys, ticks, fmt, x0, x1, gutter_x) {
    ticks.forEach(function (v, i) {
      var y = ys(v);
      if (v !== 0) c.line(x0, y, x1, y, { stroke: 'gridline', width: c.t('line-hairline'), mark: false });
      c.text(gutter_x, y + c.size('tick') * 0.35, K.fmt(v, P.tick_fmt(c, ticks, i, fmt)), { role: 'tick', anchor: 'end', tnum: true });
    });
  };
  // The zero line. Pass the value scale (a K.scale.linear) and the line draws only where the scale holds zero, so a scale
  // that starts above zero never draws a line far under its plot (CD RM1); a number is the line's place, drawn as given.
  P.zero_line = function (c, y, x0, x1) {
    if (typeof y === 'function') {
      var d = y.domain || [0, 0];
      if (Math.min(d[0], d[1]) > 0 || Math.max(d[0], d[1]) < 0) return;
      y = y(0);
    }
    c.line(x0, y, x1, y, { stroke: 'baseline', width: c.t('line-baseline'), mark: false });
  };

  // Year labels along a time axis: one at each January the domain holds, thinned to fit
  P.year_axis = function (c, xs, lo, hi, y, x_end) {
    var years = [], step = 1, size = c.size('tick');
    for (var yr = Math.ceil(lo - 1e-9); yr <= hi + 1e-9; yr++) years.push(yr);
    var wmax = c.measure('0000', 'tick') + 14;
    while (years.length > 1 && (xs(years[0] + step) - xs(years[0])) < wmax) step++;
    years.forEach(function (yr, i) {
      if ((yr - years[0]) % step) return;
      var x = xs(yr);
      if (x + c.measure(String(yr), 'tick') > (x_end || c.width)) return;
      c.line(x, y - size - 6, x, y - size - 2, { stroke: 'baseline', width: c.t('line-hairline'), mark: false });
      c.text(x, y, String(yr), { role: 'tick' });
    });
  };

  // A note set inside the plot with a leader to the point it explains. place: above, below, left, right.
  P.note = function (c, px, py, words, o) {
    o = o || {};
    var size = c.size('label'), place = o.place || 'above', clear = c.t('note-leader-min'), wgt = o.weight || 600;
    var lines = o.max ? c.wrap(words, 'label', o.max, wgt) : [words];
    var w = 0;
    lines.forEach(function (l) { w = Math.max(w, c.measure(l, 'label', wgt)); });
    var lh = Math.round(size * 1.25), h = lh * (lines.length - 1) + size;
    var anchor = o.anchor || 'middle';
    var tx = px, ty;
    if (place === 'above') ty = py - clear - (lines.length - 1) * lh - size * 0.25;
    else if (place === 'below') ty = py + clear + size;
    else { ty = py + size * 0.35 - (lines.length - 1) * lh / 2; tx = place === 'left' ? px - clear : px + clear; anchor = place === 'left' ? 'end' : 'start'; }
    if (o.dx) tx += o.dx;
    if (o.dy) ty += o.dy;
    var x0 = anchor === 'middle' ? tx - w / 2 : anchor === 'end' ? tx - w : tx;
    // keep the note inside the artboard
    if (x0 < 0) { tx += -x0; x0 = 0; }
    if (x0 + w > c.width) { tx -= x0 + w - c.width; x0 = c.width - w; }
    // a note that would touch a text already drawn moves up or down a line at a time, up to three, to the nearest clear
    // place (D3-93: at a width the spec's offsets were not set for)
    var asc = size * 0.969, touches = function (yy) {
      var b = { x: x0, y: yy - asc + 2, w: w, h: h };
      return c.texts.some(function (t) { return b.x < t.x + t.w + 1 && t.x < b.x + b.w + 1 && b.y < t.y + t.h + 1 && t.y < b.y + b.h + 1; });
    };
    if (touches(ty)) {
      var step = h + 6, alt = [-1, 1, -2, 2, -3, 3].map(function (k) { return ty + k * step; }).filter(function (yy) { return yy - asc > 0 && !touches(yy); });
      if (alt.length) ty = alt[0];
    }
    var box = c.text(tx, ty, lines.join(' '), { role: 'label', weight: wgt, anchor: anchor, max: o.max ? o.max + 1 : undefined, halo: true });
    // the leader from the note's near edge to the point
    var lx = Math.max(box.x, Math.min(px, box.x + box.w)), ly;
    if (place === 'above') ly = box.y + box.h + 3;
    else if (place === 'below') ly = box.y - 3;
    else { lx = place === 'left' ? box.x + box.w + 3 : box.x - 3; ly = py; }
    var dist = Math.sqrt((lx - px) * (lx - px) + (ly - py) * (ly - py));
    // beside its point a note needs no leader under a dozen pixels: a short dash before a figure reads as a minus sign
    var side = place === 'left' || place === 'right';
    if (dist > (side ? 12 : 4) && o.leader !== false) c.line(lx, ly, px, py, { stroke: 'leader', width: c.t('line-hairline'), mark: false });
    return box;
  };

  // The value scale: the spec's own (scale.y = [lo, hi]) or a nice one from the data; ticks at one step inside it
  P.value_scale = function (c, lo, hi, count) {
    var sc = (c.spec.scale || {}).y;
    if (sc) { var st = K.nice(sc[0], sc[1], count).step; return { lo: sc[0], hi: sc[1], ticks: K.ticks(sc[0], sc[1], 0, st) }; }
    var nk = K.nice(lo, hi, count);
    return { lo: nk[0], hi: nk[1], ticks: K.ticks(nk[0], nk[1], 0, nk.step) };
  };
  // Styles that tell parts apart in grayscale (ranked bar, unit chart): fill, outline, hatch, dash. A form passes its own
  // pattern name and dash where its drawing needs them, so each draws exactly as before the styles were shared.
  P.style = function (name, over) {
    var base = { solid: { fill: 'subject', text: 'label-on-subject' }, open: { fill: 'surface', stroke: 'subject', text: 'label' },
      gray: { fill: 'light-fill', text: 'label' }, hatch: { pattern: 'hatch', stroke: 'subject', text: null },
      dashed: { fill: 'none', stroke: 'subject', dash: '3 2', text: null } };
    var st = base[name] || base.solid, o = (over || {})[name in base ? name : 'solid'] || {};
    var out = {};
    for (var k in st) out[k] = st[k];
    for (var k2 in o) out[k2] = o[k2];
    return out;
  };
  P.styled = function (c, x, y, w, h, st, o) {
    if (st.pattern) c.pattern(st.pattern, st.stroke);
    c.rect(x, y, w, h, Object.assign({ fill: st.fill === 'none' ? 'none' : st.fill, pattern: st.pattern }, o));
    if (st.stroke) c.rect(x + 0.5, y + 0.5, w - 1, h - 1, { stroke: st.stroke, dash: st.dash, mark: false });
  };
  // The square tile grid's measures at this width
  P.tiles = function (c) {
    var gap = c.t(c.phone ? 'tile-phone-gap' : 'tile-gap'), size = Math.min(c.t('tile-size-max'), Math.floor((c.width - 11 * gap) / 12));
    return { gap: gap, size: size, pitch: size + gap };
  };
  // Fill {placeholders} in a label from a row: {x}, {y} and any encode name, formatted by spec.formats
  P.fill = function (c, tmpl, row) {
    var f = c.spec.formats || {};
    return String(tmpl).replace(/\{([a-z0-9_]+)\}/g, function (_, k) {
      var col = c.encode[k] || k;
      var v = row[col];
      return K.fmt(v, f[k] || f[col] || 'text');
    });
  };
  // A shift arrow from x1 (its tail dot) to x2 (its head) at height y, in the subject ink; o.data marks the head for the checks.
  // Shared by shift-arrows, results-table, tile-map-shift-arrows and diverging-bar-arrows (moved from shift-arrows.js, R-B6).
  P.arrow = function (c, x1, x2, y, o) {
    var hl = c.t(c.phone ? 'arrow-phone-head-length' : 'arrow-head-length'), hw = c.t(c.phone ? 'arrow-phone-head-half-width' : 'arrow-head-half-width');
    // BC S16: the shaft lands on the pixel grid (K.snap), and its tail dot and head follow it, so the three stay on one line
    y = K.snap(y, c.t('arrow-shaft'));
    var dir = x2 >= x1 ? 1 : -1, len = Math.abs(x2 - x1);
    // an arrow shorter than its head draws the head alone, never a tail dot under it, which reads as a diamond (brand KS4)
    if (len < hl + 2) { c.polygon([[x2, y], [x2 - dir * hl, y - hw], [x2 - dir * hl, y + hw]], { fill: 'subject', kind: 'arrow', data: o.data }); return; }
    c.circle(x1, y, c.t('arrow-tail-radius'), { fill: 'subject', mark: false });
    if (len > hl) c.line(x1, y, x2 - dir * hl, y, { stroke: 'subject', width: c.t('arrow-shaft'), mark: false });
    var b = x2 - dir * Math.min(hl, Math.max(len, hl * 0.6));
    c.polygon([[x2, y], [b, y - hw], [b, y + hw]], { fill: 'subject', kind: 'arrow', data: o.data });
  };
  // The light fill (palette rule R3, DR-236, D3-164): where a spec names some marks (labels.named: a value or a list of
  // values of the given field), those take the subject ink and every other takes the light fill on Newsprint and the
  // context ink on Charcoal, values still printed. With nothing named every mark takes the subject ink. Returns a
  // function row -> color role, with .named (true when the spec names any) and .is_named(row).
  // point (ED-E1, round 1): the one mark a title names in working red takes the point role, with the 1 px keyline on
  // Newsprint where Pillar Red measures 2.96 to 1 (fn.keyline(row) gives the stroke options to merge into the mark's).
  // round 2 (ED-E15, ruling (c)): point may be a list, the marks a title names together in one role (an age band), which
  // share the red as one job: merge fn.job(row) into each mark's options ({job: 'point'} on a point, {} otherwise), so the
  // red count reads them as one working red.
  P.named_fill = function (c, named, field, base, point) {
    var pts = point === undefined || point === null ? null : [].concat(point).map(String);
    // ED-E12 (second pass): a point with nothing else named names the point alone, so one key gives the red point and the
    // light fill on every other mark (palette rule R3); a spec that sets both keys draws as before
    var list = named === undefined || named === null ? pts : [].concat(named).map(String);
    var other = c.ground === 'charcoal' ? 'context' : 'light-fill';
    var is_named = function (r) { return !list || list.indexOf(String(r[field])) >= 0; };
    var is_point = function (r) { return pts !== null && pts.indexOf(String(r[field])) >= 0; };
    var fn = function (r) { return is_point(r) ? 'point' : is_named(r) ? (base || 'subject') : other; };
    fn.named = !!list;
    fn.is_named = is_named;
    fn.is_point = is_point;
    fn.keyline = function (r) { return is_point(r) && c.ground !== 'charcoal' ? { stroke: 'point-keyline', width: c.t('keyline') } : {}; };
    fn.job = function (r) { return is_point(r) ? { job: 'point' } : {}; };
    // G2 (round 2, opt-in): a light-fill mark that prints no value of its own may take a 1 px edge in the context ink, so
    // its edge reads at 4.29 to 1 on Newsprint where the fill alone reads at 1.81; on Charcoal those marks take the context
    // ink (5.41 to 1) and need none. Merge fn.edge(row) into the mark's options.
    fn.edge = function (r) { return fn(r) === 'light-fill' ? { stroke: 'context', width: 1 } : {}; };
    return fn;
  };

  // ---- Round 2 (R2-5, contract R2-C2): intervals, bands and stacks ------------------------------------------------
  // An estimate and its interval, read by the spec's encode: the estimate is encode.value (else encode.y); the interval is
  // encode.low and encode.high, or encode.margin (low = value - margin, high = value + margin). iv(row) gives
  // {v, lo, hi, m}, m the margin (or half of high - low); iv.differs(a, b) tells whether two rows differ by more than the
  // margin of their difference, the square root of the sum of the margins squared (the Census Bureau's test, Rule 14.9).
  var num = function (x) { return x === null || x === undefined || x === '' ? NaN : +x; };
  P.interval_of = function (c) {
    var e = c.encode || {}, fv = e.value !== undefined ? e.value : e.y, fl = e.low, fh = e.high, fm = e.margin;
    var iv = function (r) {
      var v = num(r[fv]), lo, hi, m;
      if (fm !== undefined && fm !== null) { m = num(r[fm]); lo = v - m; hi = v + m; }
      else { lo = num(r[fl]); hi = num(r[fh]); m = (hi - lo) / 2; }
      return { v: v, lo: lo, hi: hi, m: m };
    };
    iv.differs = function (a, b) {
      var x = iv(a), y = iv(b);
      return Math.abs(x.v - y.v) > Math.sqrt(x.m * x.m + y.m * y.m);
    };
    iv.fields = { value: fv, low: fl, high: fh, margin: fm };
    return iv;
  };
  // An interval's thin line from p0 to p1 (pixels along the value axis) at the cross position at: dir 'h' (a row's
  // whisker, the default) or 'v' (a column's). The context ink at 2 px with no caps, as Rule 14.9's plate draws it; o.cap
  // is a cap's half-length in px. With o.key and o.low / o.high each end is recorded for the checks (no element).
  P.whisker = function (c, p0, p1, at, o) {
    o = o || {};
    var a = Math.min(p0, p1), b = Math.max(p0, p1), h = o.dir !== 'v';
    var st = { stroke: o.stroke || 'context', width: o.width || c.t('line-context'), mark: false };
    if (h) c.line(a, at, b, at, st); else c.line(at, a, at, b, st);
    if (o.cap) [a, b].forEach(function (p) { if (h) c.line(p, at - o.cap, p, at + o.cap, st); else c.line(at - o.cap, p, at + o.cap, p, st); });
    if (o.key !== undefined) {
      var fl = o.field_low || 'low', fh = o.field_high || 'high';
      if (o.low !== undefined) c.datum(h ? (p0 <= p1 ? p0 : p1) : at, h ? at : (p0 <= p1 ? p0 : p1), { data: { key: o.key, field: fl, value: o.low } });
      if (o.high !== undefined) c.datum(h ? (p0 <= p1 ? p1 : p0) : at, h ? at : (p0 <= p1 ? p1 : p0), { data: { key: o.key, field: fh, value: o.high } });
    }
    return h ? { x: a, y: at - (o.cap || 0), w: b - a, h: 2 * (o.cap || 0) } : { x: at - (o.cap || 0), y: a, w: 2 * (o.cap || 0), h: b - a };
  };
  // A filled band between two series: pts [{x, y0, y1, key, low, high, break}] in drawing order, pixels. A point with y0 or
  // y1 missing ends the run before it; break: true starts a new run at that point (a break in the series, which the band
  // never bridges). Each run is one closed path in o.fill ('band' by default, or o.pattern); o.edge draws each edge as a
  // line in that stroke role. A run of one point draws a short whisker. Returns {runs: [[first, last]], top, bottom}.
  P.band = function (c, pts, o) {
    o = o || {};
    var runs = [], cur = null, top = Infinity, bottom = -Infinity;
    var ok = function (p) { return p && isFinite(p.x) && isFinite(p.y0) && isFinite(p.y1) && p.y0 !== null && p.y1 !== null; };
    pts.forEach(function (p, i) {
      if (!ok(p)) { cur = null; return; }
      if (!cur || p.break) { cur = [i, i]; runs.push(cur); } else cur[1] = i;
      top = Math.min(top, p.y0, p.y1); bottom = Math.max(bottom, p.y0, p.y1);
      if (p.key !== undefined) {
        if (p.low !== undefined) c.datum(p.x, Math.max(p.y0, p.y1), { data: { key: p.key, field: o.field_low || 'low', value: p.low } });
        if (p.high !== undefined) c.datum(p.x, Math.min(p.y0, p.y1), { data: { key: p.key, field: o.field_high || 'high', value: p.high } });
      }
    });
    // D3-903 (round 2 fix pass): the band is recorded for the checks, which hold its fill, or its edges, to 3 to 1 against
    // what lies under it, and its height to the line it carries (o.line_width, default the context line's 2 px)
    (c.bands = c.bands || []).push({ fill: o.pattern ? null : (o.fill || 'band'), pattern: o.pattern || null, edge: o.edge || null,
      edge_width: o.edge ? (o.edge_width || c.t('line-hairline')) : 0, line: o.line_width || c.t('line-context'), top: top, bottom: bottom,
      heights: pts.filter(ok).map(function (p) { return Math.abs(p.y1 - p.y0); }), runs: runs.length });
    var R = K.round, edge = { stroke: o.edge, width: o.edge_width || c.t('line-hairline'), mark: false };
    runs.forEach(function (rn) {
      var seg = pts.slice(rn[0], rn[1] + 1);
      if (seg.length === 1) { P.whisker(c, seg[0].y0, seg[0].y1, seg[0].x, { dir: 'v', stroke: o.edge || 'context', width: c.t('line-context') }); return; }
      var up = seg.map(function (p) { return R(p.x) + ',' + R(Math.min(p.y0, p.y1)); });
      var dn = seg.slice().reverse().map(function (p) { return R(p.x) + ',' + R(Math.max(p.y0, p.y1)); });
      c.path('M' + up.join('L') + 'L' + dn.join('L') + 'Z', { fill: o.pattern ? undefined : (o.fill || 'band'), pattern: o.pattern, mark: false });
      if (o.edge) {
        c.path('M' + up.join('L'), Object.assign({ fill: 'none' }, edge));
        c.path('M' + seg.map(function (p) { return R(p.x) + ',' + R(Math.max(p.y0, p.y1)); }).join('L'), Object.assign({ fill: 'none' }, edge));
      }
    });
    return { runs: runs, top: top, bottom: bottom };
  };
  // A stack layout (draws nothing): rows, and parts the value columns in stacking order, the first on the baseline.
  // o.offset 'zero' (default): positives stack up from 0 and negatives down from 0, the parts in o.negative counted as
  // negative (a pyramid's left side); 'expand': each row's parts as shares of its total (o.total, a column, else the parts'
  // sum), 0 to 100; 'center': expand, moved so the boundary before part o.center_at sits at 0 (a share bar's midline).
  // Returns one item a row, {row, total, segs: [{field, value, start, end, share, missing}]}, start <= end; .lo and .hi
  // are the extent over every row.
  P.stack = function (rows, parts, o) {
    o = o || {};
    var off = o.offset || 'zero', neg = [].concat(o.negative || []), lo = 0, hi = 0;
    var out = rows.map(function (r) {
      var vals = parts.map(function (p) { var v = num(r[p]); return { field: p, raw: v, missing: !isFinite(v) }; });
      var sum = vals.reduce(function (s, x) { return s + (x.missing ? 0 : Math.abs(x.raw)); }, 0);
      var total = o.total ? num(r[o.total]) : sum;
      var pos = 0, ng = 0, segs = vals.map(function (x) {
        var v = x.missing ? 0 : x.raw, share = total ? 100 * Math.abs(v) / total : 0, s, e;
        if (off === 'zero') {
          var d = neg.indexOf(x.field) >= 0 ? -Math.abs(v) : v;
          if (d >= 0) { s = pos; e = pos + d; pos = e; } else { e = ng; s = ng + d; ng = s; }
        } else { s = pos; e = pos + share; pos = e; }
        return { field: x.field, value: x.missing ? null : x.raw, start: s, end: e, share: share, missing: x.missing };
      });
      if (off === 'center') {
        var at = o.center_at !== undefined ? parts.indexOf(o.center_at) : -1, shift = at > 0 ? segs[at].start : 0;
        segs.forEach(function (sg) { sg.start -= shift; sg.end -= shift; });
      }
      segs.forEach(function (sg) { lo = Math.min(lo, sg.start); hi = Math.max(hi, sg.end); });
      return { row: r, total: total, segs: segs };
    });
    out.lo = lo; out.hi = hi;
    return out;
  };
  // A total or national line and point, one treatment for every form (the data lead's round 2 ruling (b)): a line across a
  // plot dashed 5 and 3 px in the text's ink at the field's weight (o.width, default 2 px; never heavier than the named
  // mark), drawn under the named mark; a point as an open ring in the text's ink. o.data marks the line or ring for the checks.
  P.total_line = function (c, x1, y1, x2, y2, o) {
    o = o || {};
    c.line(x1, y1, x2, y2, { stroke: 'label', width: o.width || c.t('line-context'), dash: '5 3', mark: !!o.data, data: o.data });
  };
  P.total_ring = function (c, x, y, r, o) {
    o = o || {};
    c.circle(x, y, r, { fill: 'surface', mark: false });
    c.circle(x, y, r, { stroke: 'label', width: o.width || c.t('line-context'), data: o.data, mark: !!o.data, row: o.row });
  };
  // ---- Labels in small areas and labels beside points (round 2, contract R2-C2) -------------------------------------
  // The box the layout guard gives a one-line label set at baseline y (Inter's line box less its half-leading, as c.text
  // records it): from 0.864 em above the baseline to 0.136 em below it
  var ABOVE = 0.864, BELOW = 0.136;
  var lbox = function (x, y, w, size, anchor) {
    return { x: anchor === 'middle' ? x - w / 2 : anchor === 'end' ? x - w : x, y: y - ABOVE * size, w: w, h: size };
  };
  var overlaps = function (b, t, pad) { return b.x < t.x + t.w + pad && t.x < b.x + b.w + pad && b.y < t.y + t.h + pad && t.y < b.y + b.h + pad; };
  // Words set inside a rectangle (a treemap's tile, a block of seats): fit_label(c, box, words, o) tries each role in
  // o.roles (default label, then tick) on one line, then up to o.lines lines (default 2), inside o.pad px (default 4; a list
  // of pads is tried in order, each with every role, A-E3); o.sub is a second block under the words, in the tick size and
  // weight 400 on up to o.sub_lines lines (default 1), which must fit with them (a figure and its share);
  // o.align 'start' (top left, default) or 'middle'; o.fill the text role for the ground under it (label-on-subject on the
  // subject ink, on-cat-1 to on-cat-3 on a group's fill); o.weight (default 600). Returns the text's box, or null and draws
  // nothing where the words do not fit, so the form sets them outside or folds the area into "All other".
  P.fit_label = function (c, box, words, o) {
    o = o || {};
    var pads = [].concat(o.pad === undefined ? 4 : o.pad), wgt = o.weight || 600, roles = o.roles || ['label', 'tick'], maxl = o.lines || 2;
    var ss = c.size('tick'), slh = Math.round(ss * 1.25), sgap = 3;
    for (var k = 0; k < pads.length; k++) {
      var pad = pads[k], aw = box.w - 2 * pad, ah = box.h - 2 * pad;
      if (aw <= 0) continue;
      var sub = o.sub === undefined || o.sub === null || o.sub === '' ? null : K.wrap(o.sub, ss, aw, 400, 'reading'), sw = 0;
      if (sub) sub.forEach(function (ln) { sw = Math.max(sw, c.measure(ln, ss, 400)); });
      if (sub && (sub.length > (o.sub_lines || 1) || sw > aw)) continue;
      var sh = sub ? sgap + ss + (sub.length - 1) * slh : 0;
      for (var i = 0; i < roles.length; i++) {
        var role = roles[i], size = c.size(role), lh = Math.round(size * 1.25);
        var lines = K.wrap(words, size, aw, wgt, 'reading'), wide = 0;
        lines.forEach(function (ln) { wide = Math.max(wide, c.measure(ln, size, wgt)); });
        var th = size + (lines.length - 1) * lh;
        if (lines.length > maxl || wide > aw || th + sh > ah) continue;
        var mid = o.align === 'middle', x = mid ? box.x + box.w / 2 : box.x + pad;
        var y = (mid ? box.y + (box.h - th - sh) / 2 : box.y + pad) + ABOVE * size;
        var tb = c.text(x, y, String(words), { role: role, weight: wgt, anchor: mid ? 'middle' : 'start', max: aw + 0.5, leading: lh, fill: o.fill });
        if (sub) tb.sub = c.text(x, y + BELOW * size + (lines.length - 1) * lh + sgap + ABOVE * ss, String(o.sub), { role: 'tick', weight: 400, anchor: mid ? 'middle' : 'start', max: aw + 0.5, leading: slh, fill: o.fill });
        return tb;
      }
    }
    return null;
  };
  // Labels beside points that keep clear of each other: place_labels(c, items, o), items [{x, y, r, words, key, weight,
  // fill}] in the order they claim room (the named point first). Each label tries eight places around its point, right,
  // left, above, below, then the four corners, r + o.gap px out (default 4); then, with o.leaders (default true), the same
  // places o.reach px further (default 14) with a hairline leader; o.reach may be a list of reaches, tried in order (RB-G3). A place must sit inside the drawing (0 to c.width, o.top
  // to o.bottom), clear of every label placed, every text already drawn, every point's dot and o.avoid boxes. Returns
  // {placed: [{item, box}], unplaced: [items]}; name the unplaced in a note (K.word('unlabeled_marks')) or the table.
  P.place_labels = function (c, items, o) {
    o = o || {};
    var role = o.role || 'label', size = c.size(role), gap = o.gap === undefined ? 4 : o.gap, pad = 2;
    var rings = o.leaders === false ? [0] : [0].concat(o.reach === undefined ? [14] : [].concat(o.reach));
    var top = o.top || 0, bottom = o.bottom === undefined ? Infinity : o.bottom;
    var dots = items.map(function (it) { var r = it.r || 0; return { x: it.x - r, y: it.y - r, w: 2 * r, h: 2 * r }; });
    var taken = (o.avoid || []).slice(), placed = [], unplaced = [];
    // a leader from the dot's edge to the label box's nearest point; a place whose leader would cross a word already drawn,
    // or whose label would sit on a leader already drawn, is not clear: the layout guard's own test (K.leader_crosses)
    var leader_of = function (it, b) {
      var r0 = it.r || 0, bx = Math.max(b.x, Math.min(it.x, b.x + b.w)), by = Math.max(b.y, Math.min(it.y, b.y + b.h));
      var dx = bx - it.x, dy = by - it.y, len = Math.sqrt(dx * dx + dy * dy) || 1;
      return [it.x + dx / len * (r0 + 1), it.y + dy / len * (r0 + 1), bx - dx / len * 2, by - dy / len * 2];
    };
    var crosses = function (L, t) { return K.leader_crosses({ x1: L[0], y1: L[1], x2: L[2], y2: L[3] }, t); };
    var places = [['right', 1, 0], ['left', -1, 0], ['above', 0, -1], ['below', 0, 1], ['upper right', 0.75, -0.75], ['lower right', 0.75, 0.75], ['upper left', -0.75, -0.75], ['lower left', -0.75, 0.75]];
    items.forEach(function (it, n) {
      var wgt = it.weight || 400, w = c.measure(it.words, role, wgt), r = it.r || 0, done = null;
      for (var ring = 0; ring < rings.length && !done; ring++) {
        var d = r + gap + rings[ring];
        for (var k = 0; k < places.length && !done; k++) {
          var ax = places[k][1], ay = places[k][2];
          var anchor = ax > 0 ? 'start' : ax < 0 ? 'end' : 'middle';
          var x = it.x + ax * d, y = ay < 0 ? it.y + ay * d - BELOW * size : ay > 0 ? it.y + ay * d + ABOVE * size : it.y + 0.35 * size;
          var b = lbox(x, y, w, size, anchor);
          if (b.x < 0 || b.x + b.w > c.width || b.y < top || b.y + b.h > bottom) continue;
          if (taken.some(function (t) { return overlaps(b, t, pad); }) || c.texts.some(function (t) { return overlaps(b, t, pad); })) continue;
          if (dots.some(function (t, j) { return j !== n && t.w > 0 && overlaps(b, t, 1); })) continue;
          if ((c.leaders || []).some(function (l) { return K.leader_crosses(l, b); })) continue;
          if (ring) {
            var L = leader_of(it, b);
            if (c.texts.some(function (t) { return crosses(L, t); })) continue;
          }
          done = { x: x, y: y, anchor: anchor, box: b, ring: ring };
        }
      }
      if (!done) { unplaced.push(it); return; }
      var tb = c.text(done.x, done.y, String(it.words), { role: role, weight: wgt, anchor: done.anchor, fill: it.fill, halo: o.halo !== false });
      taken.push(tb);
      if (done.ring) {
        // the leader from the dot's edge to the label's nearest edge
        var LL = leader_of(it, tb);
        c.line(LL[0], LL[1], LL[2], LL[3], { stroke: 'leader', width: c.t('line-hairline'), mark: false });
      }
      placed.push({ item: it, box: tb });
    });
    return { placed: placed, unplaced: unplaced };
  };
  // Long rows to one row a key, for stack: wide(rows, key, series, value) gives one row per key value with a column per
  // series value, in first-seen order; .series lists the series values
  P.wide = function (rows, key, series, value) {
    var by = {}, order = [], ser = [];
    rows.forEach(function (r) {
      var k = String(r[key]), s = String(r[series]);
      if (!(k in by)) { by[k] = {}; by[k][key] = r[key]; order.push(k); }
      if (ser.indexOf(s) < 0) ser.push(s);
      by[k][s] = r[value];
    });
    var out = order.map(function (k) { return by[k]; });
    out.series = ser;
    return out;
  };
})(typeof globalThis !== 'undefined' ? globalThis : this);
