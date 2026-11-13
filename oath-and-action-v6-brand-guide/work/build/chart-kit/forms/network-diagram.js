/* Network diagram (coverage plan 3.12, extended; S73). Who sends to whom: each source a box, links running from it to the
 * boxes of the nodes it sent to, every link's width its measure in one linear unit for the whole drawing (K.parts.flows),
 * with a key of widths; a link narrower than a pixel draws at 1 px, and the key says so. Links leave a source stacked in
 * the order of the nodes they reach, so none cross. Sources sit side by side from labels.side_by_side px (default 600) and
 * one under another below it, drawn alike on one unit. Rows a spec folds (labels.nodes) join one node; the table lists
 * each row. Inks (the data lead's round 3 ruling (b)): every node and link in the ink labels.ink names (the party-mark
 * ink for money spent to elect a candidate, Rule 14.6), node boxes outlined in it with the words in the text's ink.
 * encode: source (text), target (text), value (number), target_key (id, matched by labels.nodes), kind (category,
 * optional, matched by labels.nodes).
 * labels: nodes ([{source, keys: [target_key], kind: [kind], rest: true, name}], in drawing order: a row joins the first
 * node it matches; {n} in a name counts its rows), sources ({source: the box's name}), sub ({source: words under the
 * name, with {total} and {n}}), value ('{v}' words under a node's name; default '{v}'), unit (the measure one pixel of
 * width carries), key_steps ([measures] the key draws), key_title, key_hairline (words under the key, {v} the measure of
 * one pixel), ink (a color role; default 'party'), side_by_side (px).
 * formats: value, small (for a measure under 1 million; default the value's). Maker B, round 3. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'network-diagram', name: 'Network Diagram', family: 'relationships',
    encode: { source: 'text', target: 'text', value: 'number', target_key: 'id', kind: 'category?' },
    labels: ['nodes', 'sources', 'sub', 'value', 'unit', 'key_steps', 'key_title', 'key_hairline', 'ink', 'side_by_side'],
    phone: 'same',
    draw: function (c) {
      var P = K.parts, L = c.labels, f = c.spec.formats || {}, W = c.width;
      var es = c.field('source'), et = c.field('target'), ev = c.field('value'), ek = c.field('target_key'), ekd = c.field('kind', false);
      var specs = L.nodes || [], ink = L.ink || 'party', unit = +L.unit || 1, tk = c.size('tick');
      var fv = function (x) { return K.fmt(x, Math.abs(x) < 1e6 && f.small ? f.small : f.value || 'integer').replace(/ (million|billion)$/, ' $1'); };
      var v = function (x) { return String(L.value || '{v}').split('{v}').join(fv(x)); };
      // one block a source, in first-seen order, and one node a matching spec
      var blocks = [];
      c.rows.forEach(function (r) {
        var s = String(r[es]), b = blocks.filter(function (x) { return x.source === s; })[0];
        if (!b) { b = { source: s, nodes: [], total: 0, rows: 0 }; blocks.push(b); }
        var m = null;
        specs.some(function (sp, i) {
          if (sp.source !== undefined && String(sp.source) !== s) return false;
          var ok = sp.rest || (sp.keys && sp.keys.map(String).indexOf(String(r[ek])) >= 0) || (sp.kind && ekd && [].concat(sp.kind).indexOf(String(r[ekd])) >= 0);
          if (ok) m = i;
          return ok;
        });
        var id = m === null ? 'row:' + r[ek] : 'spec:' + m, nd = b.nodes.filter(function (x) { return x.id === id; })[0];
        if (!nd) { nd = { id: id, order: m === null ? 1e6 : m, spec: m === null ? null : specs[m], rows: [], value: 0 }; b.nodes.push(nd); }
        nd.rows.push(r); nd.value += r[ev]; b.total += r[ev]; b.rows++;
      });
      // one linear unit for every link in the drawing
      var links = [];
      blocks.forEach(function (b) {
        b.nodes.sort(function (p, q) { return p.order - q.order; });
        b.nodes.forEach(function (nd) {
          nd.name = String(nd.spec && nd.spec.name ? nd.spec.name : nd.rows[0][et]).split('{n}').join(String(nd.rows.length));
          links.push({ from: b.source, to: b.source + '>' + nd.id, value: nd.value, key: nd.name });
        });
      });
      var fl = P.flows(links, { unit: 1 / unit });
      fl.faults.forEach(function (x) { c.warn(x); });
      var y = 0;
      if (L.key_steps) {
        y += P.width_key(c, 0, y, 1 / unit, L.key_steps, { words: L.key_steps.map(function (s) { return fv(s); }), stroke: ink, len: 32, title: L.key_title, max: W });
        if (L.key_hairline) { var hb = c.text(0, y + tk * 0.9, String(L.key_hairline).split('{v}').join(fv(unit)), { role: 'tick', max: W }); y = hb.bottom; }
        y += 18;
      }
      var two = W >= (L.side_by_side || 600), pw = two ? Math.floor((W - 28) / 2) : W, gap = 10;
      var hw = Math.round(pw * (two ? 0.32 : 0.38)), rw = Math.round(pw * (two ? 0.42 : 0.46));
      var top = y, low = y;
      blocks.forEach(function (b, bi) {
        var x0 = two ? bi * (pw + 28) : 0, y0 = two ? top : low + (bi ? 28 : 0), rx = x0 + pw - rw;
        var hsub = (L.sub || {})[b.source];
        hsub = hsub ? String(hsub).split('{total}').join(v(b.total)).split('{n}').join(String(b.rows)) : undefined;
        var hname = String((L.sources || {})[b.source] || b.source);
        // the nodes' boxes, each as tall as its link or its words
        var ny = y0, items = b.nodes.map(function (nd) {
          var lw = Math.max(1, fl.px(nd.value)), sz = P.node_size(c, nd.name, { max: rw, sub: v(nd.value), sub_lines: 3, lines: 4, pad: [8, 6] });
          var it = { nd: nd, lw: lw, y: ny, h: Math.max(lw + 6, sz ? sz.h : 40) };
          ny += it.h + gap;
          return it;
        });
        var stack = items.reduce(function (s, it) { return s + it.lw; }, 0);
        var hs = P.node_size(c, hname, { max: hw, sub: hsub, sub_lines: 3, lines: 4, pad: [8, 6] });
        var hh = Math.max(stack + 6, hs ? hs.h : 60), ly = y0 + (hh - stack) / 2;
        // links first, then the boxes and their words over the links' ends
        items.forEach(function (it) {
          var ty = it.y + (it.h - it.lw) / 2;
          P.flow_band(c, x0 + hw, ly, rx, ty, it.lw, { fill: ink, edge: false, data: { key: it.nd.name, from: b.source, to: it.nd.name, value: it.nd.value } });
          if (it.nd.rows.length > 1) it.nd.rows.forEach(function (r) { c.datum(rx, ty + it.lw / 2, { data: { key: r[ek], field: ev, value: r[ev] } }); });
          ly += it.lw;
        });
        var opt = function (data, sub) { return { stroke: ink, width: 1.5, align: 'start', pad: [8, 6], sub: sub, sub_lines: 3, lines: 4, data: data }; };
        if (!P.node(c, { x: x0, y: y0, w: hw, h: hh }, hname, opt({ key: b.source, field: ev, value: b.total }, hsub))) c.warn('network-diagram: the words do not fit the box for ' + hname + ' at ' + W + ' px');
        items.forEach(function (it) {
          if (!P.node(c, { x: rx, y: it.y, w: rw, h: it.h }, it.nd.name, opt({ key: it.nd.name, field: ev, value: it.nd.value }, v(it.nd.value)))) c.warn('network-diagram: the words do not fit the box for ' + it.nd.name + ' at ' + W + ' px');
        });
        low = Math.max(low, ny - gap, y0 + hh);
      });
      c.height(low + 1);
    }
  });
})(globalThis.OAChart);
