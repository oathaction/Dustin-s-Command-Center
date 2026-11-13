/* Network diagram (coverage plan 3.12, extended; S73). Who sends to whom: each source a bar, links running from it to the
 * bars of the nodes it sent to, every bar and link as tall or wide as its measure in one linear unit for the whole drawing
 * (K.parts.flows), with a key of widths; a link narrower than a pixel draws at 1 px, and the key may say so. Links leave a
 * source stacked in the order of the nodes they reach, so none cross. Each source's words head its block; each
 * receiver's name and measure sit beside its bar (the data lead's MB-3: a node's size is its measure, never its words).
 * Sources sit side by side from labels.side_by_side px (default 680) and one under another below it, drawn alike on one
 * unit. Rows a spec folds (labels.nodes) join one node; the table lists each row or groups them. Inks (the data lead's
 * round 3 ruling (b), as its review fix pass corrects it for B-S1): every bar solid in the ink labels.ink names (the
 * party-mark ink for money spent to elect a candidate, Rule 14.6), every link in the light fill with a 1 px edge in that
 * ink (RF-2), as the Sankey draws its bands, so the links read apart from the bars they join, and the key of widths
 * draws its bands the same way (BC-S2); the words in the text's ink.
 * encode: source (text), target (text), value (number), target_key (id, matched by labels.nodes), kind (category,
 * optional, matched by labels.nodes), line (category, optional: with labels.lines, only rows of those values draw).
 * labels: nodes ([{source, keys: [target_key], kind: [kind], rest: true, name}], in drawing order: a row joins the first
 * node it matches; {n} in a name counts its rows), sources ({source: the block's heading, with {total}}), sub ({source: words under the
 * heading, with {total} and {n}}), value ('{v}' words under a node's name; default '{v}'), unit (the measure one pixel of
 * width carries), key_steps ([measures] the key draws), key_title, key_hairline (words under the key, {v} the measure of
 * one pixel), ink (a color role; default 'party'), side_by_side (px), lines ([values of encode.line] drawn).
 * formats: value, small (for a measure under 1 million; default the value's), key (the key's measures). Maker B, round 3. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'network-diagram', name: 'Network Diagram', family: 'relationships',
    encode: { source: 'text', target: 'text', value: 'number', target_key: 'id', kind: 'category?', line: 'category?' },
    labels: ['nodes', 'sources', 'sub', 'value', 'unit', 'key_steps', 'key_title', 'key_hairline', 'ink', 'side_by_side', 'lines'],
    phone: 'same',
    draw: function (c) {
      var P = K.parts, L = c.labels, f = c.spec.formats || {}, W = c.width;
      var es = c.field('source'), et = c.field('target'), ev = c.field('value'), ek = c.field('target_key'), ekd = c.field('kind', false), eln = c.field('line', false);
      var keep = eln && L.lines ? [].concat(L.lines).map(String) : null;
      var specs = L.nodes || [], ink = L.ink || 'party', unit = +L.unit || 1, tk = c.size('tick');
      var fv = function (x) { return K.fmt(x, Math.abs(x) < 1e6 && f.small ? f.small : f.value || 'integer').replace(/ (million|billion)$/, ' $1'); };
      var v = function (x) { return String(L.value || '{v}').split('{v}').join(fv(x)); };
      var kv = function (x) { return String(L.value || '{v}').split('{v}').join(K.fmt(x, f.key || f.value || 'integer').replace(/ (million|billion)$/, '\u00a0$1')); };
      // one block a source, in first-seen order, and one node a matching spec
      var blocks = [];
      c.rows.forEach(function (r) {
        if (keep && keep.indexOf(String(r[eln])) < 0) return;   // a row of another measure: the table keeps it, the drawing does not
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
        y += P.width_key(c, 0, y, 1 / unit, L.key_steps, { words: L.key_steps.map(function (s) { return kv(s); }), band: 'light-fill', edge: ink, len: 32, title: L.key_title, max: W });
        if (L.key_hairline) { var hb = c.text(0, y + tk * 0.9, String(L.key_hairline).split('{v}').join(kv(unit)), { role: 'tick', max: W }); y = hb.bottom; }
        y += 18;
      }
      // side by side where both fit, else one under another. Every node is a bar as tall as its dollars in the links'
      // unit, never a box whose size a reader could take for a measure (the data lead's MB-3): each source's words head
      // its block over its bar, and each receiver's name and dollars sit beside its bar
      var two = W >= (L.side_by_side || 680), pw = two ? Math.floor((W - 28) / 2) : W, gap = 10, bw = 12, lb = c.size('label');
      var bx = Math.round(pw * (two ? 0.4 : W < 420 ? 0.34 : 0.4)), lw = pw - bx - bw - 8;
      var top = y, low = y;
      // each source's words over its block; side by side, every block's bars start under the deepest heading, so the two
      // sides' bars share one top
      var head = function (b, x0, y0) {
        var hsub = (L.sub || {})[b.source];
        hsub = hsub ? String(hsub).split('{total}').join(v(b.total)).split('{n}').join(String(b.rows)) : undefined;
        var nb = c.text(x0, y0 + lb * 0.95, String((L.sources || {})[b.source] || b.source).split('{total}').join(v(b.total)), { role: 'label', weight: 700, max: pw });
        if (hsub) nb = c.text(x0, nb.bottom + tk * 0.95, hsub, { role: 'tick', max: pw, fill: 'label' });
        return Math.ceil(nb.bottom) + 12;
      };
      var shared = two ? Math.max.apply(null, blocks.map(function (b, bi) { return head(b, bi * (pw + 28), top); })) : 0;
      blocks.forEach(function (b, bi) {
        var x0 = two ? bi * (pw + 28) : 0, y0 = two ? top : low + (bi ? 28 : 0), rx = x0 + bx;
        y0 = two ? shared : head(b, x0, y0);
        // each receiver's slot: as tall as its bar or its words, whichever is taller
        var ny = y0, items = b.nodes.map(function (nd) {
          var h = Math.max(1, fl.px(nd.value)), nl = c.wrap(nd.name, 'label', lw, 600).length;
          var it = { nd: nd, h: h, y: ny, s: Math.max(h, Math.ceil(nl * Math.round(lb * 1.25) + tk * 1.25 + 2)) };
          ny += it.s + gap;
          return it;
        });
        var ly = y0;
        // links first, then the bars over their ends, then the words beside the bars
        items.forEach(function (it) {
          P.flow_band(c, x0 + bw, ly, rx, it.y, it.h, { fill: 'light-fill', edge: ink, edge_width: 1, data: { key: it.nd.name, from: b.source, to: it.nd.name, value: it.nd.value } });
          if (it.nd.rows.length > 1) it.nd.rows.forEach(function (r) { c.datum(rx, it.y + it.h / 2, { data: { key: r[ek], field: ev, value: r[ev] } }); });
          ly += it.h;
        });
        c.rect(x0, y0, bw, ly - y0, { fill: ink, kind: 'node', data: { key: b.source, field: ev, value: b.total } });
        items.forEach(function (it) {
          c.rect(rx, it.y, bw, it.h, { fill: ink, kind: 'node', data: { key: it.nd.name, field: ev, value: it.nd.value } });
          var t = c.text(rx + bw + 8, it.y + lb * 0.8, it.nd.name, { role: 'label', weight: 600, max: lw });
          c.text(rx + bw + 8, t.bottom + tk * 0.95, v(it.nd.value), { role: 'tick', fill: 'label', tnum: true, max: lw });
        });
        low = Math.max(low, ny - gap, ly);
      });
      c.height(low + 1);
    }
  });
})(globalThis.OAChart);
