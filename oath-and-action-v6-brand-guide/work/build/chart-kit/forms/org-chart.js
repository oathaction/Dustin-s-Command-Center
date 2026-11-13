/* Org chart (coverage plan 3.11, extended; S69). Who sits under whom inside one body: the body's box at the top, a line
 * at the left down to each group of its units (a heading with the group's count), and each unit as a card: its box,
 * named, with the count of the units under it, and under it, set in, each of those by name on a row of its own, rows
 * parted by hairline rules with no box each, joined to the card by elbow links in the context ink (the kit's tree part,
 * indent layout). Every box takes a subject-ink edge, all one ink. Cards fill as many columns of 220 px as the width
 * holds, in the data's order down the first column, then the next, the columns as even in height as the order allows
 * (BC-S7); a phone draws one column. A group's count reads every row (c.all_rows where the kit draws only a part).
 * encode: unit (text: the unit's name), unit_key (id, optional: the unit's name keys it where left out), group (category), sub (text: the sub-unit's name, empty on the
 * unit's own row).
 * labels: root (the body's name), groups ({value: words}, in order; {n} the count), drop ([prefixes left off a unit's
 * name, the table keeping it whole]), count ({one, many}: words under a unit's name with {n}), none (words for a unit
 * with no sub-units). */
(function (K) {
  'use strict';
  // BC-S7: cut a list of heights, in order, into at most k runs, one a column, so the tallest column is as short as it
  // can be, then fill each column in turn up to that height, so the first columns are the fuller; returns each item's
  // column
  function K_split(hs, k, gap) {
    var n = hs.length, pre = [0];
    hs.forEach(function (h, i) { pre.push(pre[i] + h); });
    var run = function (i, j) { return j > i ? pre[j] - pre[i] + gap * (j - i - 1) : 0; };
    var best = [];
    for (var j = 0; j <= n; j++) best[j] = run(0, j);
    for (var p = 1; p < k; p++) {
      var nb = [];
      for (var j2 = 0; j2 <= n; j2++) { nb[j2] = Infinity; for (var i = 0; i <= j2; i++) nb[j2] = Math.min(nb[j2], Math.max(best[i], run(i, j2))); }
      best = nb;
    }
    var m = best[n] + 1e-6, out = [], col = 0, st = 0;
    for (var q = 0; q < n; q++) { if (q > st && run(st, q + 1) > m && col < k - 1) { col++; st = q; } out[q] = col; }
    return out;
  }
  K.register_chart({
    form: 'org-chart', name: 'Org Chart', family: 'structure',
    encode: { unit: 'text', unit_key: 'id?', group: 'category', sub: 'text' },
    labels: ['root', 'groups', 'drop', 'count', 'none'],
    phone: 'differs',
    draw: function (c) {
      var L = c.labels, W = c.width, eu = c.field('unit'), ek = c.field('unit_key', false) || c.field('unit'), eg = c.field('group'), es = c.field('sub');
      var spine = 12, ind = 28, cg = 16, vg = 16, sub_in = 16, P = K.parts, cnt = L.count || {};
      // one space between words, then the spec's typography, so a name measures as it prints in Node and on the page, where
      // the table carries the printed words (D3-519)
      var one = function (s) { return K.typeset({ typography: c.spec.typography || { curl_quotes: true, nbsp: true } }, String(s).replace(/[ \t\n]+/g, ' ')); };
      var short = function (s) { s = one(s); (L.drop || []).forEach(function (p) { if (s.indexOf(p) === 0) s = s.slice(p.length); }); return s.charAt(0).toUpperCase() + s.slice(1); };
      // the units in the data's order, each with its sub-units
      var units = [], by = {};
      c.rows.forEach(function (r) {
        var k = String(r[ek]);
        if (!by[k]) { by[k] = { key: k, name: r[eu], group: String(r[eg]), subs: [] }; units.push(by[k]); }
        if (r[es]) by[k].subs.push(r);
      });
      // a group's count reads every row, where the kit draws only the first rows (a desk's phone drawing)
      var all_n = {}, seen = {};
      (c.all_rows || c.rows).forEach(function (r) { var k = String(r[ek]); if (!seen[k]) { seen[k] = 1; all_n[String(r[eg])] = (all_n[String(r[eg])] || 0) + 1; } });
      var ncol = Math.max(1, Math.floor((W - ind + cg) / (220 + cg))), cw = (W - ind - cg * (ncol - 1)) / ncol;
      if (ncol === 1) c.arrange('phone');
      var box = function (b, words, o) { return P.node(c, b, words, Object.assign({ stroke: 'subject', align: 'start', lines: 6, sub_lines: 3 }, o)); };
      var szo = { lines: 6, sub_lines: 3 };
      // the root
      var rs = P.node_size(c, one(L.root || ''), Object.assign({ max: Math.min(W, 360), named: true }, szo)) || { w: Math.min(W, 360), h: 40 };
      var rb = { x: 0, y: 0, w: rs.w, h: rs.h };
      var y = rb.h + 18, heads = [];
      Object.keys(L.groups || {}).forEach(function (g) {
        var us = units.filter(function (u) { return u.group === g; });
        if (!us.length) return;
        var hb = c.text(ind, y + c.size('label') * 0.93, String(L.groups[g]).split('{n}').join(String(all_n[g] || us.length)), { role: 'label', weight: 700, max: W - ind });
        heads.push(y + c.size('label') * 0.6);
        // each card laid out first, so the columns can be cut in order and balanced by height
        var cards = us.map(function (u) {
          var n = u.subs.length;
          var words = one(n ? String(n === 1 ? cnt.one : cnt.many).split('{n}').join(String(n)) : (L.none || ''));
          var items = [{ id: u.key, parent: null, words: short(u.name), sub: words || undefined, named: true }].concat(u.subs.map(function (r, j) {
            return { id: u.key + '.' + j, parent: u.key, words: one(r[es]), role: 'tick' };
          }));
          items.forEach(function (it) {
            var w = cw - (it.parent ? sub_in : 0);
            var s = P.node_size(c, it.words, Object.assign({ max: w, min: w, named: it.named, sub: it.sub, roles: it.parent ? ['tick'] : ['label'], pad: it.parent ? [0, 4] : [10, 7], weight: it.parent ? 400 : 700 }, szo));
            it.w = w; it.h = s ? s.h : 40;
          });
          var t2 = P.tree(items, { dir: 'indent', indent: sub_in, row_gap: 1 });
          t2.faults.forEach(function (f) { c.warn(f); });
          return { u: u, t: t2 };
        });
        var at = K_split(cards.map(function (cd) { return cd.t.height; }), ncol, vg);
        var cols = []; for (var i = 0; i < ncol; i++) cols.push(hb.bottom + 10);
        cards.forEach(function (cd, k) {
          var ci = at[k], x = ind + ci * (cw + cg), t2 = cd.t, top = cols[ci];
          t2.links.forEach(function (l) {
            var a = t2.by[l.from], b = t2.by[l.to], lx = x + a.x + 8;
            P.link(c, { x: lx, y: top + a.y + a.h }, { x: lx, y: top + b.y + b.h / 2 }, { stroke: 'context', width: 1 });
            P.link(c, { x: lx, y: top + b.y + b.h / 2 }, { x: x + b.x - 3, y: top + b.y + b.h / 2 }, { stroke: 'context', width: 1 });
          });
          var subs = t2.nodes.filter(function (nd) { return nd.item.parent; });
          // a hairline rule between one sub-unit's row and the next (A-S4)
          subs.forEach(function (nd, j) {
            if (!j) return;
            var ry = top + nd.y - 0.5;
            c.line(x + nd.x, ry, x + nd.x + nd.w, ry, { stroke: 'gridline', width: 1, mark: false });
          });
          t2.nodes.forEach(function (nd) {
            var it = nd.item;
            var o = it.parent ? { fill: 'surface', stroke: false, roles: ['tick'], pad: [0, 4], weight: 400, text: 'label' } : { named: true, sub: it.sub, roles: ['label'], pad: [10, 7], weight: 700 };
            if (!box({ x: x + nd.x, y: top + nd.y, w: nd.w, h: nd.h }, it.words, Object.assign(o, { data: { key: it.id, field: it.parent ? 'sub' : 'unit', value: it.words } }))) c.warn('org-chart: the words of ' + it.words + ' do not fit their box at ' + W + ' px');
          });
          cols[ci] = top + t2.height + vg;
        });
        y = Math.max.apply(null, cols) - vg + 26;
      });
      // the root's line down the left to each group's heading
      heads.forEach(function (hy, i) {
        P.link(c, { x: spine, y: i ? heads[i - 1] : rb.h }, { x: spine, y: hy }, { stroke: 'context', width: 1 });
        P.link(c, { x: spine, y: hy }, { x: ind - 6, y: hy }, { stroke: 'context', width: 1 });
      });
      box(rb, L.root || '', { named: true, data: { key: 'root', field: 'root', value: L.root } });
      c.height(y - 26 + 1);
    }
  });
})(globalThis.OAChart);
