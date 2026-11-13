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
 * none_hatch (true: that region and its key swatch take a hatch in the context ink over the land ink; BC-S3),
 * outline_all (true: the context edge round the land), phone_tiles (true: under 480 px the states take the studio's tile
 * grid, every state's code on its tile; set phone "differs"; C-M1, round 3 fix pass), code_column (true: at a desk the map
 * fits 44 px narrower and the northeastern codes with no room inside take a column on the ocean, on leaders), tiles_under
 * (a width in px under which the tile grid draws at a desk too, where the outlines leave a code no room). formats:
 * value, margin. */
(function (K) {
  'use strict';
  var STEPS = ['seq-1', 'seq-3', 'seq-4', 'seq-5'];
  var fill_of_cls = function (steps, it) { return it.cls ? steps[it.cls - 1] : 'land'; };
  var on_ink = function (fill) { return /^(seq|mag|div)-\d$/.test(fill || '') ? 'on-' + fill : 'label'; };   // the step's own label ink
  // one map: o = {layer, x, y, w, max_h, items: [{id, cls (1 to n, or null), data, code}], steps, codes, dc, dc_room,
  // state_lines, outline_all}; returns {T, bottom, unplaced}. dc_room (AX-S3, round 3 fix pass): DC's square and its
  // name stay inside the panel's own width, and where the panel is too narrow for them east of Maryland the map is fitted
  // narrower, so the square draws in every panel at every width
  var panel = function (c, o) {
    var L = K.geo(o.layer), steps = o.steps || STEPS, fit = function (w) { return K.parts.map_fit(c, L, { x: o.x || 0, y: o.y || 0, w: w, max_h: o.max_h }); };
    // o.column (C-M1, round 3 fix pass): the map fits 44 px narrower than the panel, leaving the ocean to the east room for
    // a column of the small northeastern states' codes on leaders (the kit's map_labels column)
    var T = fit(o.column ? o.w - 44 : o.w), right = o.dc_room ? (o.x || 0) + o.w : c.width;
    var dc_size = function (T) { return Math.max(7, Math.min(11, T.k * 12)); };
    if (o.dc && o.dc_room && L.labels && L.index['11'] !== undefined && o.items.some(function (it) { return it.id === '11'; })) {
      for (var tries = 0; tries < 6; tries++) {
        var q0 = T.pt(L.labels[L.index['11']]), need = q0[0] + T.k * 46 - 2 + dc_size(T) + 6 + c.measure(o.dc, 'tick', 600) + 2 - right;
        if (need <= 0) break;
        T = fit(T.w - need - 1);
      }
    }
    var fill_of = function (it) { return it.cls ? steps[it.cls - 1] : 'land'; };
    K.parts.map_shapes(c, L, T, o.items.map(function (it) { return { id: it.id, fill: fill_of(it), data: it.data }; }), { merge: !!o.merge });
    // BC-S3 (round 3 fix pass): a region with no estimate takes a hatch in the context ink over the land ink, on both
    // grounds, so it never reads as the lightest class (o.none_hatch)
    var nones = o.items.filter(function (it) { return !it.cls; });
    if (o.none_hatch && nones.length) {
      c.pattern('none', 'context');
      K.parts.map_shapes(c, L, T, nones.map(function (it) { return { id: it.id, pattern: 'none' }; }), { merge: !!o.merge });
    }
    var cls_of = {};
    o.items.forEach(function (it) { cls_of[it.id] = it.cls; });
    var first = function (id) { return id !== null && (cls_of[id] === 1 || cls_of[id] === null || cls_of[id] === undefined); };
    if (o.state_lines) {
      // a county map: no county lines; state lines in the context ink at 0.5 px, and the land's edge in the context ink at 1 px
      K.parts.map_mesh(c, L, T, { between: function (a, b) { return b !== null && a.slice(0, 2) !== b.slice(0, 2); }, stroke: 'context', width: 0.5 });
      K.parts.map_mesh(c, L, T, { which: 'outline', stroke: 'context', width: 1 });   // 1 px, so the land's edge carries on Charcoal
      // a county with no estimate keeps the land ink with a 1 px context edge (ruling (b))
      K.parts.map_mesh(c, L, T, { which: 'all', between: function (a, b) { return cls_of[a] === null || (b !== null && cls_of[b] === null); }, stroke: 'context', width: 1 });
    } else {
      K.parts.map_mesh(c, L, T, { stroke: 'surface', width: 1 });
      // the lightest step meets the ground with a 1 px context edge (call 3)
      K.parts.map_mesh(c, L, T, { between: function (a, b) { return o.outline_all ? b === null || first(a) || first(b) : first(a) || first(b); }, stroke: 'context', width: 1 });
    }
    if (L.ids.some(function (id) { return id.slice(0, 2) === '02'; })) K.parts.map_insets(c, L, T);
    var bottom = T.y + T.h, unplaced = [], avoid = [], colinfo = null;
    if (o.codes) {
      // names claim room largest shape first: inside the shape in its step's label ink (the kit's map_labels, inside
      // only); the rest beside with a leader, on the ground's halo, clear of every word and leader, over the ground or the lightest step only
      var items = o.items.filter(function (it) { return it.code && it.id !== '11' && L.index[it.id] !== undefined; })
        .sort(function (a, b) { return L.labels[L.index[b.id]][2] - L.labels[L.index[a.id]][2] || (a.id < b.id ? -1 : 1); });
      var r1 = K.parts.map_labels(c, L, T, items.map(function (it) { return { id: it.id, words: it.code, weight: 600, fill: on_ink(fill_of(it)) }; }), { role: 'tick', beside: false, inset: 1 });
      if (o.column && r1.unplaced.length) {
        // the codes that found no room inside: the eastern ones to the column on the ocean, the rest on short leaders over
        // light ground; whatever is left goes to the search below
        var r2 = K.parts.map_labels(c, L, T, r1.unplaced, { role: 'tick', inset: 1, column: 0.8, reach: [16, 30, 46, 64], ring0: false });
        // a code left over (West Virginia, whose leader would cross a neighbor's code at the column's own row) joins the
        // column below its last name, on the ocean, if its leader crosses no word and no other leader
        var colb = r2.beside.filter(function (b) { return b.box.x > T.x + T.w * 0.8; }).map(function (b) { return b.box; });
        if (colb.length) {
          var cx0 = Math.min.apply(null, colb.map(function (b) { return b.x; })), cy = Math.max.apply(null, colb.map(function (b) { return b.y + b.h; }));
          var ctop = Math.min.apply(null, colb.map(function (b) { return b.y; }));
          var lh = Math.round(c.size('tick') * 1.3), sz = c.size('tick');
          var cross = function (a, b2) {
            var d = function (p, q, r) { return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0]); };
            var p1 = [a.x1, a.y1], p2 = [a.x2, a.y2], q1 = [b2.x1, b2.y1], q2 = [b2.x2, b2.y2];
            return d(p1, p2, q1) * d(p1, p2, q2) < 0 && d(q1, q2, p1) * d(q1, q2, p2) < 0;
          };
          r2.unplaced = r2.unplaced.filter(function (it) {
            var q = T.pt(L.labels[L.index[it.id]]);
            // any free row of the column, nearest the code's own height first
            var rows = [];
            for (var yy0 = ctop + sz / 2; yy0 + sz / 2 < T.y + T.h; yy0 += lh / 2) rows.push(yy0);
            rows.sort(function (a, b) { return Math.abs(a - q[1]) - Math.abs(b - q[1]); });
            for (var ri = 0; ri < rows.length; ri++) {
              var yy = rows[ri];
              var b = c.text_box(cx0, yy + 0.35 * sz, it.words, { role: 'tick', weight: 600 }), ln = { x1: q[0], y1: q[1], x2: cx0 - 3, y2: yy };
              if (c.texts.some(function (t) { return b.x < t.x + t.w + 1 && t.x < b.x + b.w + 1 && b.y < t.y + t.h + 1 && t.y < b.y + b.h + 1; })) continue;
              if (c.texts.some(function (t) { return K.leader_crosses(ln, t); }) || (c.leaders || []).some(function (l) { return cross(l, ln); })) continue;
              var ok = true;
              for (var i = 0; i <= 4 && ok; i++) for (var j = 0; j <= 2 && ok; j++) if (['surface', 'none', null].indexOf(c.fill_under(b.x - 2 + i * (b.w + 4) / 4, b.y - 2 + j * (b.h + 4) / 2)) < 0) ok = false;
              if (!ok) continue;
              c.line(q[0], q[1], cx0 - 3, yy, { stroke: 'leader', width: c.t('line-hairline'), mark: false });
              var tb3 = c.text(cx0, yy + 0.35 * sz, it.words, { role: 'tick', weight: 600, halo: true });
              cy = Math.max(cy, tb3.y + tb3.h);
              return false;
            }
            return true;
          });
          colinfo = { x: cx0, y: cy, lh: lh };
        }
        // last, inside the shape with no room to spare (Kentucky and Tennessee near 480 px)
        if (r2.unplaced.length) r2 = K.parts.map_labels(c, L, T, r2.unplaced, { role: 'tick', beside: false, inset: 0, spare: 0 });
        r1 = { unplaced: r2.unplaced };
      }
      var dark = o.items.filter(function (it) { return it.cls > 1; }).map(function (it) { return L.rings(L.index[it.id]).map(function (rs) { return rs.map(function (r) { return r.map(T.pt); }); }); });
      var LIGHT = [null, 'surface', 'none', 'land', 'seq-1'];
      var in_dark = function (x, y) { return LIGHT.indexOf(c.fill_under(x, y)) < 0 || dark.some(function (ps) { return ps.some(function (rs) { return K.in_poly(rs, x, y); }); }); };
      var hit = function (a, b2) { return a.x < b2.x + b2.w + 2 && b2.x < a.x + a.w + 2 && a.y < b2.y + b2.h + 2 && b2.y < a.y + a.h + 2; };
      var size = c.size('tick');
      r1.unplaced.forEach(function (it) {
        var q = T.pt(L.labels[L.index[it.id]]), w = c.measure(it.words, 'tick', 600), pick = null;
        (c.phone ? [8, 16] : [10, 20, 32]).forEach(function (d) {
          [[1, 0], [-1, 0], [0, -1], [0, 1], [0.7, -0.7], [0.7, 0.7], [-0.7, -0.7], [-0.7, 0.7]].forEach(function (v) {
            if (pick) return;
            var cx = q[0] + v[0] * (d + w / 2), base = q[1] + v[1] * (d + size / 2) + size * 0.32, b = c.text_box(cx, base, it.words, { role: 'tick', weight: 600, anchor: 'middle' }); b.base = base;
            if (b.x < 0 || b.x + b.w > c.width || b.y < T.y) return;
            if (c.texts.some(function (t) { return hit(b, t); }) || avoid.some(function (t) { return hit(b, t); })) return;
            if ((c.leaders || []).some(function (l) { return K.leader_crosses(l, b); })) return;
            for (var i = 0; i <= 4; i++) for (var j = 0; j <= 2; j++) if (in_dark(b.x - 2 + i * (b.w + 4) / 4, b.y - 2 + j * (b.h + 4) / 2)) return;
            var ex = Math.max(b.x, Math.min(q[0], b.x + b.w)), ey = Math.max(b.y, Math.min(q[1], b.y + b.h));
            if (c.texts.some(function (t) { return K.seg_hits_box(q[0], q[1], ex, ey, t.x - 1, t.y - 1, t.x + t.w + 1, t.y + t.h + 1); })) return;
            pick = { b: b, ex: ex, ey: ey };
          });
        });
        if (!pick) { unplaced.push(it.words); return; }
        var len = Math.hypot(pick.ex - q[0], pick.ey - q[1]) || 1, ux = (pick.ex - q[0]) / len, uy = (pick.ey - q[1]) / len;
        c.line(q[0], q[1], pick.ex - ux * 2, pick.ey - uy * 2, { stroke: 'leader', width: c.t('line-hairline'), mark: false });
        c.text(pick.b.x + pick.b.w / 2, pick.b.base, it.words, { role: 'tick', weight: 600, anchor: 'middle', halo: true });
      });
    }
    // DC, whose outline draws under a pixel: a small square in its class fill with a leader and its name, at the first
    // spot east or south of it clear of every word, leader and darker step, drawn after the codes
    var dc = o.items.filter(function (it) { return it.id === '11'; })[0];
    if (o.dc && dc && L.labels) {
      var p0 = T.pt(L.labels[L.index['11']]), s = dc_size(T), tw = c.measure(o.dc, 'tick', 600), dpick = null;
      // with a column of codes on the ocean, DC's square joins it below its last name (frame units from DC's point)
      var spots = colinfo ? [0, 1, 2, 3, 4, 5].map(function (k) { return [(colinfo.x - p0[0]) / T.k, (colinfo.y + 4 + k * colinfo.lh - p0[1]) / T.k]; }) : [];
      spots.concat([[46, 40], [60, 30], [60, 50], [40, 60], [70, 70], [30, 80], [80, 10], [90, 40], [60, 90], [90, 80], [40, 100], [80, 110], [20, 110], [100, 100], [60, 130]]).forEach(function (v) {
        if (dpick) return;
        var dx = p0[0] + T.k * v[0], dy = p0[1] + T.k * v[1], tb = c.text_box(dx + s + 4, dy + s - 1, o.dc, { role: 'tick', weight: 600 });
        var box = { x: dx - 2, y: Math.min(dy, tb.y) - 2, w: s + 6 + tb.w + 2, h: Math.max(s, tb.h) + 4 };
        if (box.x + box.w > right) return;
        if (c.texts.some(function (t) { return box.x < t.x + t.w && t.x < box.x + box.w && box.y < t.y + t.h && t.y < box.y + box.h; })) return;
        var sq = { x: dx - 1, y: dy - 1, w: s + 2, h: s + 2 };
        if ((c.leaders || []).some(function (l) { return K.leader_crosses(l, box) || K.leader_crosses(l, sq) || K.leader_crosses(l, tb) || K.seg_hits_box(l.x1, l.y1, l.x2, l.y2, tb.x - 1, tb.y - 1, tb.x + tb.w + 1, tb.y + tb.h + 1); })) return;
        if (c.texts.some(function (t) { return K.seg_hits_box(p0[0], p0[1], dx, dy + s / 2, t.x - 1, t.y - 1, t.x + t.w + 1, t.y + t.h + 1); })) return;
        dpick = [dx, dy];
      });
      if (dpick) {
        c.line(p0[0], p0[1], dpick[0], dpick[1] + s / 2, { stroke: 'leader', width: c.t('line-hairline'), mark: false });
        c.rect(dpick[0], dpick[1], s, s, { fill: fill_of(dc), data: dc.data });
        if (dc.cls === 1) c.rect(dpick[0] + 0.5, dpick[1] + 0.5, s - 1, s - 1, { stroke: 'context', width: 1, mark: false });
        c.text(dpick[0] + s + 4, dpick[1] + s - 1, o.dc, { role: 'tick', weight: 600, halo: true });
      } else unplaced.push(o.dc);
    }
    c.texts.forEach(function (t) { bottom = Math.max(bottom, t.y + t.h); });
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
    var by = ky + 13, rowb = by;
    // one swatch and its words a step, in rows that wrap; a label too long for the row wraps under itself, and the next
    // row starts under its last line (the data lead's C-2: S84's longest label at 224 px)
    var items = words.map(function (w, i) { return { w: w, fill: steps[i], edge: i === 0 }; }).concat((extra || []).map(function (e) { return { w: e.words, fill: e.fill, edge: true, pattern: e.pattern }; }));
    items.forEach(function (it) {
      var need = sw + 6 + c.measure(it.w, 'tick');
      if (x > 0 && x + need > W) { x = 0; by = rowb + 19; }
      c.rect(x, by - 11, sw, sw, { fill: it.fill, mark: false });
      if (it.pattern) { c.pattern(it.pattern, 'context'); c.rect(x, by - 11, sw, sw, { pattern: it.pattern, mark: false }); }
      if (it.edge) c.rect(x + 0.5, by - 10.5, sw - 1, sw - 1, { stroke: 'context', width: 1, mark: false });
      var tb = c.text(x + sw + 6, by, it.w, { role: 'tick', max: W - x - sw - 6 });
      rowb = Math.max(rowb, tb.bottom);
      x = tb.x + tb.w + 16;
      if (tb.lines > 1) { x = 0; by = rowb + 19; }
    });
    c.key(steps.slice(0, words.length).map(function (s, i) { return { fill: s, ordered: true, outline: i === 0 }; }));
    return rowb + 9;
  };
  var def = K.register_chart({
    form: 'choropleth', name: 'Choropleth', family: 'maps',
    encode: { code: 'code?', id: 'id?', value: 'number', margin: 'number?' },
    labels: ['layer', 'bins', 'class_field', 'steps', 'class_labels', 'key_title', 'nation', 'nation_label', 'dc', 'codes', 'state_lines', 'none_label', 'none_hatch', 'outline_all', 'phone_tiles', 'tiles_under', 'code_column'],
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
      if ((c.phone || W < (L.tiles_under || 0)) && L.phone_tiles && ec && G.tiles) {
        // C-M1 (round 3 fix pass): under 480 px the states take the studio's tile grid (S07's), one square each in the same
        // classes, steps and edges, so every state keeps its code where outlines leave most of them no room; a code sits
        // on its tile in its step's label ink with 1 px to spare each side, and any that cannot is named in a note
        var tm = K.parts.tiles(c), top = y + 10, tsize = c.t('type-tile-code-phone'), lost = [], tb2 = top;
        // where more than ten codes would find no room the tiles carry none, as S07's and S12's do, and the kit's note says so
        var fits_code = function (code) { return tm.size - 2 >= c.measure(code, 'tick', 600) * tsize / c.size('tick'); };
        var none = items.filter(function (it) { return it.code && G.tiles[it.code] && !fits_code(it.code); }).length > 10;
        items.forEach(function (it) {
          var t = G.tiles[it.code];
          if (!t) return;
          var x = t[0] * tm.pitch, yy = top + t[1] * tm.pitch, fl = fill_of_cls(steps, it);
          c.rect(x, yy, tm.size, tm.size, { fill: fl, data: it.data });
          if (it.cls === 1 || !it.cls) c.rect(x + 0.5, yy + 0.5, tm.size - 1, tm.size - 1, { stroke: 'context', width: 1, mark: false });
          if (none) { /* no codes at this width */ } else if (fits_code(it.code)) c.text(x + tm.size / 2, yy + tm.size / 2 + tsize * 0.35, it.code, { role: 'tick', size: tsize, weight: 600, anchor: 'middle', fill: on_ink(fl) });
          else lost.push(it.code);
          tb2 = Math.max(tb2, yy + tm.size);
        });
        if (none) tb2 = c.text(0, tb2 + 20, K.word('unlabeled_tiles'), { role: 'note', max: W, fill: 'secondary' }).bottom;
        else if (lost.length) tb2 = c.text(0, tb2 + 20, K.word('unlabeled_marks').replace('{codes}', lost.sort().join(', ')), { role: 'note', max: W, fill: 'secondary' }).bottom;
        c.height(tb2 + 4);
        return;
      }
      var r = panel(c, { layer: layer, x: 0, y: y + 10, w: W, items: items, steps: steps, codes: L.codes !== false && !!ec, dc: L.dc, merge: !!L.state_lines, state_lines: L.state_lines, outline_all: L.outline_all, column: !!L.code_column && !c.phone });
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
