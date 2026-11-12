/* Unit chart (coverage plan 3.4, core; S08). One square per row, keyed by its ID, so every mark traces to one record; squares
 * stack in columns by group (such as year) and in bands by category, read by fill, outline, hatch and dash.
 * encode: key (id), category (category), group (year or category, optional).
 * labels: categories ([{value, label, style}] style solid, open, gray, hatch or dashed, in band order), bins ([{label, max}],
 * optional: groups up to max print as one column), count_label (words before the counts row, optional). */
(function (K) {
  'use strict';
  // the shared styles, with the unit chart's own hatch name and dash; text inks are not used here
  var OVER = { hatch: { pattern: 'u-hatch' }, dashed: { dash: '2 2' } };
  var STY = {};
  ['solid', 'open', 'gray', 'hatch', 'dashed'].forEach(function (n) { STY[n] = K.parts.style(n, OVER); delete STY[n].text; });
  // The mirrored layout (E17, Phase 2's S08): one category stacks up from a central row of group labels, a second hangs down
  // from it, and the rest share a band below with their own key; a ring marks one square with its words on a leader.
  function mirrored(c, gkey, groups) {
    var rows = c.rows, ek = c.field('key'), ec = c.field('category'), L = c.labels, W = c.width;
    var cats = {};
    (L.categories || []).forEach(function (x) { cats[x.value] = x; });
    var up = L.mirror[0], down = L.mirror[1], nei = L.neither || { values: [] };
    var u = c.t('unit-size'), ug = c.t('unit-gap'), small = c.size('tick');
    var lw = 0;
    [up, down].forEach(function (v) { lw = Math.max(lw, c.measure((cats[v] || {}).label || v, 'label', 600) + 22); });
    if (L.count_label) lw = Math.max(lw, c.measure(L.count_label, 'tick'));
    if (nei.label) lw = Math.max(lw, c.measure(nei.label, 'label', 600));
    // a ring around a square at the edge reaches past the square by 0.4 of a unit and its stroke; the columns leave room (KR5)
    var Wc = W - (L.ring ? Math.ceil(u * 0.4 + c.t('line-baseline')) + 1 : 0);
    var x0 = c.phone ? 0 : Math.ceil(lw + 14), cw = (Wc - x0) / Math.max(1, groups.length);
    var per = Math.max(1, Math.floor((cw - 2 + ug) / (u + ug)));
    var cell = {};
    rows.forEach(function (r) { var k = gkey(r) + '\u0000' + r[ec]; (cell[k] = cell[k] || []).push(r); });
    // the ringed entry is drawn last in its stack, at the stack's foot, so its leader runs straight to its words (E28)
    if (L.ring) Object.keys(cell).forEach(function (k) {
      var l = cell[k], i = l.findIndex(function (r) { return r[ek] === L.ring.key; });
      if (i >= 0) l.push(l.splice(i, 1)[0]);
    });
    var nrows = function (v) { var m = 0; groups.forEach(function (g) { m = Math.max(m, Math.ceil((cell[g + '\u0000' + v] || []).length / per)); }); return m; };
    var nUp = nrows(up), nDown = nrows(down);
    var ring = L.ring || null, ringBox = null;
    var draw_unit = function (r, x, y, style) {
      K.parts.styled(c, x, y, u, u, STY[style] || STY.solid, { kind: 'unit', data: { key: r[ek], field: ec, value: r[ec] } });
      if (ring && r[ek] === ring.key) ringBox = [x, y];
    };
    var colx = function (gi, j, n) { var used = Math.min(per, n); return x0 + gi * cw + (cw - used * (u + ug) + ug) / 2 + (j % per) * (u + ug); };
    var y = 0;
    if (c.phone) {
      [up, down].forEach(function (v, i) {
        var x = i ? c.measure((cats[up] || {}).label || up, 'tick', 600) + 40 : 0, st = STY[(cats[v] || {}).style] || STY.solid;
        // the second entry takes its own line where the two would not fit side by side (D3-93)
        if (i && x + 18 + c.measure((cats[v] || {}).label || v, 'tick', 600) > W) { x = 0; y += 22; }
        c.rect(x, y + 2, 12, 12, { fill: st.fill === 'surface' ? 'surface' : st.fill, mark: false });
        if (st.stroke) c.rect(x + 0.5, y + 2.5, 11, 11, { stroke: st.stroke, mark: false });
        c.text(x + 18, y + 13, (cats[v] || {}).label || v, { role: 'tick', weight: 600 });
      });
      y += 26;
    }
    if (L.count_label) {
      if (!c.phone) c.text(0, y + small, L.count_label, { role: 'tick' });
      groups.forEach(function (g, gi) {
        var n = rows.filter(function (r) { return gkey(r) === g; }).length;
        c.text(x0 + gi * cw + cw / 2, y + small, K.fmt(n, 'integer'), { role: 'tick', anchor: 'middle', tnum: true });
      });
      y += small + 14;
    }
    var midTop = y + nUp * (u + ug) + 4;
    if (!c.phone) {
      var tu = c.text(18, midTop - 6, (cats[up] || {}).label || up, { role: 'label', weight: 600 });
      var su = STY[(cats[up] || {}).style] || STY.solid;
      c.rect(0, tu.y + 1, 12, 12, { fill: su.fill === 'surface' ? 'surface' : su.fill, mark: false });
      if (su.stroke) c.rect(0.5, tu.y + 1.5, 11, 11, { stroke: su.stroke, mark: false });
    }
    groups.forEach(function (g, gi) {
      var list = cell[g + '\u0000' + up] || [];
      list.forEach(function (r, j) { draw_unit(r, colx(gi, j, list.length), midTop - (Math.floor(j / per) + 1) * (u + ug), (cats[up] || {}).style); });
    });
    c.line(x0, midTop + 1, W, midTop + 1, { stroke: 'baseline', width: c.t('line-hairline'), mark: false });
    var labY = midTop + small + 6;
    var right = -1e9;
    groups.forEach(function (g, gi) {
      var tw = c.measure(g, 'tick'), cx = Math.min(Math.max(x0 + gi * cw + cw / 2, x0 + tw / 2), W - tw / 2);
      if (cx - tw / 2 < right + 4) return;
      c.text(cx, labY, g, { role: 'tick', anchor: 'middle' });
      right = cx + tw / 2;
    });
    var midBot = labY + 8;
    c.line(x0, midBot, W, midBot, { stroke: 'baseline', width: c.t('line-hairline'), mark: false });
    if (!c.phone) {
      var sd = STY[(cats[down] || {}).style] || STY.solid;
      c.rect(0, midBot + 4, 12, 12, { fill: sd.fill === 'surface' ? 'surface' : sd.fill, mark: false });
      c.text(18, midBot + 15, (cats[down] || {}).label || down, { role: 'label', weight: 600 });
    }
    groups.forEach(function (g, gi) {
      var list = cell[g + '\u0000' + down] || [];
      list.forEach(function (r, j) { draw_unit(r, colx(gi, j, list.length), midBot + 4 + Math.floor(j / per) * (u + ug), (cats[down] || {}).style); });
    });
    var downEnd = midBot + 4 + nDown * (u + ug);
    y = downEnd + 18;
    if (ring && ringBox) {
      // the ring's words sit under the lower stack, on a leader up to the ringed square
      var rx = ringBox[0] + u / 2, ry = ringBox[1] + u / 2;
      c.circle(rx, ry, u * 0.9, { stroke: 'label', width: c.t('line-baseline'), kind: 'ring' });   // a mark, so the check sees it inside the drawing
      var ty = Math.max(downEnd, ry + u) + small + 8;
      var t = c.text(Math.min(W, rx + u), ty, ring.text, { role: 'tick', weight: 600, anchor: 'end' });
      c.line(rx, ry + u * 0.9, rx, t.y - 1, { stroke: 'leader', width: c.t('line-hairline'), mark: false });
      y = Math.max(y, t.y + t.h + 14);
      ring = null;
    }
    // the rest, in one band below, then their key
    if (nei.values && nei.values.length) {
      c.line(x0, y - 8, W, y - 8, { stroke: 'gridline', width: c.t('line-hairline'), mark: false });
      if (nei.label) c.text(0, y + small, nei.label, { role: 'label', weight: 600 });
      var nmax = 0;
      groups.forEach(function (g, gi) {
        var list = [];
        nei.values.forEach(function (v) { list = list.concat((cell[g + '\u0000' + v] || []).map(function (r) { return [r, v]; })); });
        nmax = Math.max(nmax, Math.ceil(list.length / per));
        list.forEach(function (p, j) { draw_unit(p[0], colx(gi, j, list.length), y + Math.floor(j / per) * (u + ug), (cats[p[1]] || {}).style); });
      });
      y += Math.max(1, nmax) * (u + ug) + 16;
      var kx = x0;
      nei.values.forEach(function (v) {
        var st = STY[(cats[v] || {}).style] || STY.solid, lab = (cats[v] || {}).label || v, w = Math.min(18 + c.measure(lab, 'tick') + 18, W - x0);
        if (kx + w > W) { kx = x0; y += 20; }
        if (st.pattern) { c.pattern(st.pattern, st.stroke); c.rect(kx, y, 12, 12, { pattern: st.pattern, mark: false }); }
        else c.rect(kx, y, 12, 12, { fill: st.fill === 'none' ? 'none' : st.fill, mark: false });
        if (st.stroke) c.rect(kx + 0.5, y + 0.5, 11, 11, { stroke: st.stroke, dash: st.dash, mark: false });
        var kb = c.text(kx + 18, y + 11, lab, { role: 'tick', max: W - kx - 18 });
        if (kb.h > c.size('tick') * 1.5) { y += kb.h - c.size('tick') + 4; kx = W; } else kx += w;
      });
      y += 22;
    }
    if (ring && ringBox) {
      var rx = ringBox[0] + u / 2, ry = ringBox[1] + u / 2;
      c.circle(rx, ry, u * 0.9, { stroke: 'label', width: c.t('line-baseline'), kind: 'ring' });   // a mark, so the check sees it inside the drawing
      var t = c.text(Math.min(W, rx + u), ry + u * 0.9 + small + 8, ring.text, { role: 'tick', weight: 600, anchor: 'end' });
      c.line(rx, ry + u * 0.9, Math.min(rx, t.x + t.w - 4), t.y - 1, { stroke: 'leader', width: c.t('line-hairline'), mark: false });
    }
    c.key((L.categories || []).map(function (x) { var st = STY[x.style] || STY.solid; return { fill: st.fill && st.fill !== 'none' && st.fill !== 'surface' ? st.fill : 'subject', pattern: !!(st.pattern || st.dash || st.stroke), direct: true }; }));
    c.height(y + 4);
  }
  K.register_chart({
    form: 'unit-chart', name: 'Unit Chart', family: 'composition',
    encode: { key: 'id', category: 'category', group: 'any?' },
    labels: ['categories', 'bins', 'count_label', 'mirror', 'neither', 'groups', 'ring'],
    phone: 'same',
    draw: function (c) {
      var rows = c.rows, ek = c.field('key'), ec = c.field('category'), eg = c.field('group', false), L = c.labels, W = c.width;
      var cats = L.categories || [], bins = L.bins || [];
      var gkey = function (r) {
        if (!eg) return '';
        var v = r[eg];
        for (var i = 0; i < bins.length; i++) if (bins[i].max !== undefined && +v <= +bins[i].max) return bins[i].label;
        return String(v);
      };
      var groups = [];
      rows.forEach(function (r) { var g = gkey(r); if (groups.indexOf(g) < 0) groups.push(g); });
      if (eg) groups.sort(function (a, b) { var ia = bins.findIndex(function (x) { return x.label === a; }), ib = bins.findIndex(function (x) { return x.label === b; }); if (ia >= 0 || ib >= 0) return (ia < 0 ? 99 : ia) - (ib < 0 ? 99 : ib); return a < b ? -1 : 1; });
      if (L.groups) {
        groups.forEach(function (g) { if (L.groups.indexOf(g) < 0) c.warn('labels.groups leaves out ' + g + ', which holds rows'); });
        groups = L.groups.map(String);
      }
      if (L.mirror) { mirrored(c, gkey, groups); return; }
      var u = c.t('unit-size'), ug = c.t('unit-gap');
      var lw = 0;
      cats.forEach(function (x) { lw = Math.max(lw, c.measure(x.label, 'label', 600) + 22); });
      var x0 = c.phone ? 0 : Math.ceil(lw + 16), cw = (W - x0) / Math.max(1, groups.length);
      var per = Math.max(1, Math.floor((cw - 4 + ug) / (u + ug)));
      var cell = {};
      rows.forEach(function (r) { var k = gkey(r) + '\u0000' + r[ec]; (cell[k] = cell[k] || []).push(r); });
      var y = c.phone ? 6 : 0;
      if (L.count_label) {
        c.text(c.phone ? 0 : 0, y + c.size('tick'), L.count_label, { role: 'tick' });
        y += c.phone ? c.size('tick') + 8 : 0;
      }
      groups.forEach(function (g, gi) {
        var n = rows.filter(function (r) { return gkey(r) === g; }).length;
        c.text(x0 + gi * cw + cw / 2, y + c.size('tick'), K.fmt(n, 'integer'), { role: 'tick', anchor: 'middle', tnum: true });
      });
      y += c.size('tick') + 14;
      cats.forEach(function (cat) {
        var st = STY[cat.style] || STY.solid, maxrows = 1;
        groups.forEach(function (g) { var m = (cell[g + '\u0000' + cat.value] || []).length; maxrows = Math.max(maxrows, Math.ceil(m / per)); });
        var bandH = maxrows * (u + ug) + 10;
        if (c.phone) { var cb = c.text(0, y + c.size('label'), cat.label, { role: 'label', weight: 600, max: W }); y = cb.bottom + 8; }
        else c.text(0, y + c.size('label') * 0.9, cat.label, { role: 'label', weight: 600, max: lw });
        groups.forEach(function (g, gi) {
          (cell[g + '\u0000' + cat.value] || []).forEach(function (r, j) {
            var col = j % per, rw = Math.floor(j / per);
            var x = x0 + gi * cw + (cw - Math.min(per, (cell[g + '\u0000' + cat.value] || []).length) * (u + ug) + ug) / 2 + col * (u + ug), yy = y + rw * (u + ug);
            K.parts.styled(c, x, yy, u, u, st, { kind: 'unit', data: { key: r[ek], field: ec, value: r[ec] } });
          });
        });
        y += bandH + 8;
        c.line(x0, y - 9, W, y - 9, { stroke: 'gridline', width: c.t('line-hairline'), mark: false });
      });
      var right = -1e9;
      groups.forEach(function (g, gi) {
        var tw = c.measure(g, 'tick'), cx = Math.min(Math.max(x0 + gi * cw + cw / 2, tw / 2), W - tw / 2);
        if (cx - tw / 2 < right + 6 && gi !== groups.length - 1) return;
        if (cx - tw / 2 < right + 6) return;
        c.text(cx, y + c.size('tick'), g, { role: 'tick', anchor: 'middle' });
        right = cx + tw / 2;
      });
      c.key(cats.map(function (x) { var s = STY[x.style] || STY.solid; return { fill: s.fill && s.fill !== 'none' && s.fill !== 'surface' ? s.fill : 'subject', pattern: !!(s.stroke || s.dash) || !!s.pattern, direct: true }; }));
      c.height(y + c.size('tick') + 6);
    }
  });
})(globalThis.OAChart);
