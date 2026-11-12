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
  P.zero_line = function (c, y, x0, x1) {
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
})(typeof globalThis !== 'undefined' ? globalThis : this);
