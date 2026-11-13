/* Network diagram (coverage plan 3.12, extended; S73). Who sends to whom: each source a box at the left, links running
 * to the boxes of the nodes it sent to at the right, every link's width its measure in one unit for the whole drawing,
 * with a key that gives the unit. Links leave a source stacked in the order of the nodes they reach, so none cross.
 * Sources stack one under another; rows a spec folds (labels.nodes) join one node, and the table lists each row. The
 * same drawing serves a phone, its boxes narrower.
 * encode: source (text), target (text), value (number), target_key (id, matched by labels.nodes), kind (category,
 * optional, matched by labels.nodes).
 * labels: nodes ([{source, keys: [target_key], kind: [kind], rest: true, name}], in drawing order: a row joins the first
 * node it matches; {n} in a name counts its rows), sources ({source: the box's name}), sub ({source: words under the
 * name, with {total} and {n}}), value ('{v}' words under a node's name; default '{v}'), unit (the measure one pixel of
 * width carries), key ('{v}' words beside the key's link), key_value (the key link's measure), named (node names the
 * title names: the subject ink), fills ({node name, "links" or "boxes": color role}).
 * formats: value. Maker B, round 3. */
(function (K) {
  'use strict';
  // a link from x0 (y0 to y0 + h0) to x1 (y1 to y1 + h1), its edges eased, as points the checks can read
  var ribbon = function (x0, y0, h0, x1, y1, h1) {
    var n = 14, top = [], bot = [], ease = function (t) { return t * t * (3 - 2 * t); };
    for (var i = 0; i <= n; i++) {
      var t = i / n, x = x0 + (x1 - x0) * t, e = ease(t);
      top.push([x, y0 + (y1 - y0) * e]);
      bot.push([x, y0 + h0 + (y1 + h1 - y0 - h0) * e]);
    }
    var R = function (p) { return Math.round(p[0] * 10) / 10 + ',' + Math.round(p[1] * 10) / 10; };
    return 'M' + top.map(R).join('L') + 'L' + bot.reverse().map(R).join('L') + 'Z';
  };
  K.register_chart({
    form: 'network-diagram', name: 'Network Diagram', family: 'relationships',
    encode: { source: 'text', target: 'text', value: 'number', target_key: 'id', kind: 'category?' },
    labels: ['nodes', 'sources', 'sub', 'value', 'unit', 'key', 'key_value', 'named', 'fills'],
    phone: 'same',
    draw: function (c) {
      var L = c.labels, f = c.spec.formats || {}, W = c.width, ph = c.phone;
      var es = c.field('source'), et = c.field('target'), ev = c.field('value'), ek = c.field('target_key'), ekd = c.field('kind', false);
      var specs = L.nodes || [], fills = L.fills || {}, named = [].concat(L.named || []);
      var unit = +L.unit || 1, lb = c.size('label'), tk = c.size('tick'), pad = 6;
      var v = function (x) { return String(L.value || '{v}').split('{v}').join(K.fmt(x, f.value || 'integer')); };
      // group the rows: one block a source, in first-seen order, and one node a matching spec
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
      var lfill = fills.links || 'context', bfill = fills.boxes || 'track';
      // a box with its words inside, top left; returns its bottom. Named: the subject ink with light words
      var box = function (x, y, w, h, words, isn, data) {
        c.rect(x, y, w, h, { fill: isn ? 'subject' : bfill, kind: 'node', data: data });
        if (!isn) c.rect(x + 0.5, y + 0.5, w - 1, h - 1, { stroke: 'context', width: 1, mark: false });
        var ink = isn ? 'label-on-subject' : 'label', yy = y + pad;
        words.forEach(function (wd, i) {
          var b = c.text(x + pad, yy + (i ? tk : lb) * 0.86, wd, { role: i ? 'tick' : 'label', weight: i ? 400 : 700, max: w - 2 * pad, fill: ink, tnum: i > 0 });
          yy = b.bottom + 1;
        });
      };
      var words_h = function (words, w) {
        var h = 2 * pad;
        words.forEach(function (wd, i) { h += c.wrap(wd, i ? 'tick' : 'label', w - 2 * pad, i ? 400 : 700).length * Math.round((i ? tk : lb) * 1.25) + 1; });
        return Math.ceil(h);
      };
      var y = 0;
      // the key: one link of the key's measure, so a reader can size every link
      if (L.key_value) {
        var kh = L.key_value / unit, kw = 40;
        c.rect(0, y, kw, kh, { fill: lfill, mark: false });
        c.key([{ fill: lfill }]);
        c.text(kw + 8, y + kh / 2 + lb * 0.35, String(L.key || '{v}').split('{v}').join(K.fmt(L.key_value, f.value || 'integer')), { role: 'label', max: W - kw - 8 });
        y += Math.max(kh, lb * 1.3) + 20;
      }
      var hw = Math.round(W * (ph ? 0.33 : 0.27)), rw = Math.round(W * (ph ? 0.4 : 0.36)), rx = W - rw, gap = 10;
      blocks.forEach(function (b, bi) {
        b.nodes.sort(function (p, q) { return p.order - q.order; });
        var hwords = [String((L.sources || {})[b.source] || b.source)];
        var sub = (L.sub || {})[b.source];
        if (sub) hwords.push(String(sub).split('{total}').join(v(b.total)).split('{n}').join(String(b.rows)));
        // the nodes' boxes at the right, each as tall as its link or its words
        var ny = y, items = b.nodes.map(function (nd) {
          var name = String(nd.spec && nd.spec.name ? nd.spec.name : nd.rows[0][et]).split('{n}').join(String(nd.rows.length));
          var lh = Math.max(1, nd.value / unit), words = [name, v(nd.value)], bh = Math.max(lh + 8, words_h(words, rw));
          var it = { nd: nd, name: name, lh: lh, words: words, y: ny, h: bh };
          ny += bh + gap;
          return it;
        });
        var stack = items.reduce(function (s, it) { return s + it.lh; }, 0);
        var hh = Math.max(stack + 8, words_h(hwords, hw)), ly = y + (hh - stack) / 2;
        // links first, then the boxes over their ends
        items.forEach(function (it) {
          var isn = named.indexOf(it.name) >= 0, ty = it.y + (it.h - it.lh) / 2;
          c.path(ribbon(hw, ly, it.lh, rx, ty, it.lh), { fill: fills[it.name] || (isn ? 'subject' : lfill), kind: 'link', data: { key: it.name, field: ev, value: it.nd.value } },
            [hw, Math.min(ly, ty), rx - hw, Math.max(ly, ty) + it.lh - Math.min(ly, ty)]);
          if (it.nd.rows.length > 1) it.nd.rows.forEach(function (r) { c.datum(rx, ty + it.lh / 2, { data: { key: r[ek], field: ev, value: r[ev] } }); });
          ly += it.lh;
        });
        box(0, y, hw, hh, hwords, false, { key: b.source, field: ev, value: b.total });
        items.forEach(function (it) { box(rx, it.y, rw, it.h, it.words, named.indexOf(it.name) >= 0, { key: it.name, field: ev, value: it.nd.value }); });
        y = Math.max(ny - gap, y + hh) + (bi < blocks.length - 1 ? 28 : 0);
      });
      c.height(y + 1);
    }
  });
})(globalThis.OAChart);
