/* Choropleth, sequential (coverage plan 3.14, core; S78). Each state shaded by its class on real 2024 Census outlines
 * (the kit's 'states' layer: the lower 48 on an Albers equal-area projection, Alaska and Hawaii apart in thin frames);
 * classes in sequential steps, the lightest with a 1 px context edge; borders a 1 px line of the ground; each state's code
 * on its shape in its step's label ink, or beside it with a leader; DC a small square beside Maryland; the nation beside
 * the map with its name and value, never as a region (Rule 14.6). county-choropleth and small-multiple-maps draw through
 * this form's panel (K.forms.choropleth.panel), as bubble-scatter draws through scatter-named.
 * encode: code (code, a state; or id, a geoid, on a county layer), value (number), margin (number, optional).
 * labels: layer ('states'), bins ([b1, b2, b3]: a class starts at each), class_field (read a class 1 to n from this column
 * in place of bins), steps (fills, lightest first; default seq-1, seq-3, seq-4, seq-5), class_labels, key_title, nation
 * (the row's code, default US), nation_label ({value}, {margin}), dc ('DC' square words), codes (false: no state codes),
 * state_lines (true on a county layer: state borders in the context ink at 0.5 px), none_label (a region with no value),
 * outline_all (true: the context edge round the land). formats: value, margin. */
(function (K) {
  'use strict';
  var STEPS = ['seq-1', 'seq-3', 'seq-4', 'seq-5'];
  var on_ink = function (fill) { var m = /^(?:seq|mag)-(\d)$/.exec(fill || ''); return m && +m[1] >= (fill.charAt(0) === 'm' ? 3 : 4) ? 'label-on-subject' : 'label'; };
  // one map: o = {layer, x, y, w, max_h, items: [{id, cls (1 to n, or null), data, code}], steps, codes, dc, state_lines,
  // outline_all}; returns {T, bottom, unplaced}
  var panel = function (c, o) {
    var L = K.geo(o.layer), steps = o.steps || STEPS, T = K.parts.map_fit(c, L, { x: o.x || 0, y: o.y || 0, w: o.w, max_h: o.max_h });
    var fill_of = function (it) { return it.cls ? steps[it.cls - 1] : 'land'; };
    K.parts.map_shapes(c, L, T, o.items.map(function (it) { return { id: it.id, fill: fill_of(it), data: it.data }; }), { merge: !!o.merge });
    var cls_of = {};
    o.items.forEach(function (it) { cls_of[it.id] = it.cls; });
    var first = function (id) { return id !== null && (cls_of[id] === 1 || cls_of[id] === null || cls_of[id] === undefined); };
    if (o.state_lines) {
      // a county map: no county lines; state lines in the context ink at 0.5 px, and the land's edge in the context ink
      K.parts.map_mesh(c, L, T, { between: function (a, b) { return b !== null && a.slice(0, 2) !== b.slice(0, 2); }, stroke: 'context', width: 0.5 });
      K.parts.map_mesh(c, L, T, { which: 'outline', stroke: 'context', width: 0.5 });
    } else {
      K.parts.map_mesh(c, L, T, { stroke: 'surface', width: 1 });
      // the lightest step meets the ground with a 1 px context edge (call 3)
      K.parts.map_mesh(c, L, T, { between: function (a, b) { return o.outline_all ? b === null || first(a) || first(b) : first(a) || first(b); }, stroke: 'context', width: 1 });
    }
    if (L.ids.some(function (id) { return id.slice(0, 2) === '02'; })) K.parts.map_insets(c, L, T);
    var bottom = T.y + T.h, unplaced = [], avoid = [];
    // DC, whose outline draws under a pixel: a small square east of it in its class fill, named, kept inside the drawing
    var dc = o.items.filter(function (it) { return it.id === '11'; })[0];
    if (o.dc && dc && L.labels) {
      var p = T.pt(L.labels[L.index['11']]), s = Math.max(7, Math.min(11, T.k * 12)), tw = c.measure(o.dc, 'tick', 600);
      var dx = Math.min(p[0] + T.k * 46, c.width - s - 5 - tw), dy = p[1] + T.k * 22;
      c.line(p[0], p[1], dx, dy + s / 2, { stroke: 'leader', width: c.t('line-hairline'), mark: false });
      c.rect(dx, dy, s, s, { fill: fill_of(dc), data: dc.data });
      if (dc.cls === 1) c.rect(dx + 0.5, dy + 0.5, s - 1, s - 1, { stroke: 'context', width: 1, mark: false });
      c.text(dx + s + 4, dy + s - 1, o.dc, { role: 'tick', weight: 600, halo: true });
      avoid.push({ x: dx - 2, y: dy - 2, w: s + 4, h: s + 4 });
    }
    if (o.codes) {
      // names claim room largest shape first: inside the shape in its step's label ink (the kit's map_labels, which here
      // places none beside); the rest beside with a leader, on the ground's halo, clear of every word and leader, over the ground or the lightest step only
      var items = o.items.filter(function (it) { return it.code && it.id !== '11' && L.index[it.id] !== undefined; })
        .sort(function (a, b) { return L.labels[L.index[b.id]][2] - L.labels[L.index[a.id]][2] || (a.id < b.id ? -1 : 1); });
      var r1 = K.parts.map_labels(c, L, T, items.map(function (it) { return { id: it.id, words: it.code, weight: 600, fill: on_ink(fill_of(it)) }; }), { role: 'tick', reach: [], top: Infinity });
      var dark = o.items.filter(function (it) { return it.cls > 1; }).map(function (it) { return L.rings(L.index[it.id]).map(function (rs) { return rs.map(function (r) { return r.map(T.pt); }); }); });
      var in_dark = function (x, y) { return dark.some(function (ps) { return ps.some(function (rs) { return K.in_poly(rs, x, y); }); }); };
      var hit = function (a, b2) { return a.x < b2.x + b2.w + 2 && b2.x < a.x + a.w + 2 && a.y < b2.y + b2.h + 2 && b2.y < a.y + a.h + 2; };
      var size = c.size('tick');
      r1.unplaced.forEach(function (it) {
        var q = T.pt(L.labels[L.index[it.id]]), w = c.measure(it.words, 'tick', 600), pick = null;
        [14, 24, 36, 50].forEach(function (d) {
          [[1, 0], [-1, 0], [0, -1], [0, 1], [0.7, -0.7], [0.7, 0.7], [-0.7, -0.7], [-0.7, 0.7]].forEach(function (v) {
            if (pick) return;
            var cx = q[0] + v[0] * (d + w / 2), cy = q[1] + v[1] * (d + size / 2), b = { x: cx - w / 2, y: cy - size / 2, w: w, h: size };
            if (b.x < 0 || b.x + b.w > c.width || b.y < T.y) return;
            if (c.texts.some(function (t) { return hit(b, t); }) || avoid.some(function (t) { return hit(b, t); })) return;
            if ((c.leaders || []).some(function (l) { return K.leader_crosses(l, b); })) return;
            for (var i = 0; i <= 2; i++) for (var j = 0; j <= 2; j++) if (in_dark(b.x + i * b.w / 2, b.y + j * b.h / 2)) return;
            var ex = Math.max(b.x, Math.min(q[0], b.x + b.w)), ey = Math.max(b.y, Math.min(q[1], b.y + b.h));
            if (c.texts.some(function (t) { return K.seg_hits_box(q[0], q[1], ex, ey, t.x - 1, t.y - 1, t.x + t.w + 1, t.y + t.h + 1); })) return;
            pick = { b: b, ex: ex, ey: ey };
          });
        });
        if (!pick) { unplaced.push(it.words); return; }
        var len = Math.hypot(pick.ex - q[0], pick.ey - q[1]) || 1, ux = (pick.ex - q[0]) / len, uy = (pick.ey - q[1]) / len;
        c.line(q[0], q[1], pick.ex - ux * 2, pick.ey - uy * 2, { stroke: 'leader', width: c.t('line-hairline'), mark: false });
        c.text(pick.b.x + w / 2, pick.b.y + size * 0.82, it.words, { role: 'tick', weight: 600, anchor: 'middle', halo: true });
      });
      c.texts.forEach(function (t) { bottom = Math.max(bottom, t.y + t.h); });
    }
    return { T: T, bottom: bottom, unplaced: unplaced };
  };
  // a row's class: from labels.class_field, or by labels.bins
  var classer = function (c) {
    var L = c.labels, f = c.field('value', false), cf = L.class_field, bins = L.bins || [];
    return function (r) {
      if (cf) { var k = r[cf]; return k === null || k === undefined || k === '' ? null : +k; }
      var v = r[f];
      if (v === null || v === undefined || v === '') return null;
      var n = 1; bins.forEach(function (b) { if (v >= b) n++; }); return n;
    };
  };
  // the key: a swatch a class, each named, in one row that wraps; the nation's figure to its right or under it
  var key = function (c, y, steps, words, extra) {
    var L = c.labels, W = c.width, sw = 14, x = 0, ky = y;
    if (L.key_title) { var kt = c.text(0, ky + 13, L.key_title, { role: 'eyebrow', weight: 700, fill: 'secondary', max: W }); ky = kt.bottom + 8; }
    var by = ky + 13;
    words.forEach(function (w, i) {
      var tw = c.measure(w, 'tick'), need = sw + 6 + tw;
      if (x > 0 && x + need > W) { x = 0; by += 22; }
      c.rect(x, by - 11, sw, sw, { fill: steps[i], mark: false });
      if (i === 0) c.rect(x + 0.5, by - 10.5, sw - 1, sw - 1, { stroke: 'context', width: 1, mark: false });
      var tb = c.text(x + sw + 6, by, w, { role: 'tick' });
      x = tb.x + tb.w + 16;
    });
    (extra || []).forEach(function (e) {
      var tw = c.measure(e.words, 'tick'), need = sw + 6 + tw;
      if (x > 0 && x + need > W) { x = 0; by += 22; }
      c.rect(x, by - 11, sw, sw, { fill: e.fill, mark: false });
      c.rect(x + 0.5, by - 10.5, sw - 1, sw - 1, { stroke: 'context', width: 1, mark: false });
      var tb = c.text(x + sw + 6, by, e.words, { role: 'tick' });
      x = tb.x + tb.w + 16;
    });
    c.key(steps.slice(0, words.length).map(function (s, i) { return { fill: s, ordered: true, outline: i === 0 }; }));
    return by + 12;
  };
  var def = K.register_chart({
    form: 'choropleth', name: 'Choropleth', family: 'maps',
    encode: { code: 'code?', id: 'id?', value: 'number', margin: 'number?' },
    labels: ['layer', 'bins', 'class_field', 'steps', 'class_labels', 'key_title', 'nation', 'nation_label', 'dc', 'codes', 'state_lines', 'none_label', 'outline_all'],
    phone: 'same',
    draw: function (c) {
      var L = c.labels, W = c.width, f = c.spec.formats || {}, G = globalThis.OAChartGeo;
      var ec = c.field('code', false), ei = c.field('id', false), ev = c.field('value'), em = c.field('margin', false);
      var layer = L.layer || 'states', steps = L.steps || STEPS, cls = classer(c), nation = L.nation || 'US';
      var id_of = function (r) { return ei ? String(r[ei]) : (G.tiles[r[ec]] || [])[2]; };
      var nrow = c.rows.filter(function (r) { return (ec && r[ec] === nation) || (ei && String(r[ei]) === nation); })[0];
      var items = c.rows.filter(function (r) { return r !== nrow && id_of(r); }).map(function (r) {
        return { id: id_of(r), cls: cls(r), code: ec ? r[ec] : null, data: { key: ec ? r[ec] : r[ei], field: ev, value: r[ev] === null ? '' : r[ev] } };
      });
      var y = key(c, 0, steps, L.class_labels || [], items.some(function (it) { return !it.cls; }) && L.none_label ? [{ fill: 'land', words: L.none_label }] : null);
      if (nrow && L.nation_label) {
        var nw = String(L.nation_label).replace('{value}', K.fmt(nrow[ev], f.value || 'number:1')).replace('{margin}', em ? K.fmt(nrow[em], f.margin || 'number:1') : '');
        var nb = c.text(0, y + 12, nw, { role: 'tick', weight: 700, max: W });
        y = nb.bottom + 4;
      }
      var r = panel(c, { layer: layer, x: 0, y: y + 10, w: W, items: items, steps: steps, codes: L.codes !== false && !!ec, dc: L.dc, merge: !!L.state_lines, state_lines: L.state_lines, outline_all: L.outline_all });
      var bottom = r.bottom;
      if (r.unplaced.length) {
        var nt = c.text(0, bottom + 20, K.word('unlabeled_marks').replace('{codes}', r.unplaced.sort().join(', ')), { role: 'note', max: W, fill: 'secondary' });
        bottom = nt.bottom;
      }
      c.height(bottom + 4);
    }
  });
  def.panel = panel;
  def.classer = classer;
  def.key = key;
  def.STEPS = STEPS;
})(globalThis.OAChart);
