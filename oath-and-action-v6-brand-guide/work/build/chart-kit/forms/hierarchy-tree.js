/* Hierarchy tree (coverage plan 3.11, extended; S70). Parts nested inside parts, with a count on every node so each level
 * sums: the root's box at the top, a line at the left down to each group of its children (a heading with the group's
 * count), and each child as a card: its box, named, with its own count and the sum of the counts under it, and under it,
 * set in and joined by elbow links in the context ink, one row a place, each row naming the place's leaves with their
 * counts. A leaf at labels.apart_level (a court of another kind) sits on a box of the track ink with a context edge
 * and its words. Children listed in labels.apart sit in a group of their own after the others, named. Every box takes a
 * subject-ink edge, all one ink. Cards fill as many columns of 210 px as the width holds, in the data's order down the
 * first column, then the next, the columns as even in height as the order allows (BC-S7); a phone draws one column.
 * A group's count reads every row (c.all_rows where the kit draws only a part).
 * encode: name (text), parent (text: the parent's name), level (category), count (integer), place (text: the leaves'
 * grouping, such as a state).
 * labels: root_sub (words under the root's name, {n}), groups ({main, apart}: headings with {n}), apart ([names]),
 * card_sub (words under a child's name: {n} its count, {d} the sum under it), card_sub_none (the same for a child with
 * no leaves), drop ([prefixes left off names]),
 * single (words a leaf with no name of its own drops, such as "District of"), shared_level and shared_words (a count
 * shared by several leaves, {n}), apart_level and apart_words, note_field (a field whose words go under a child with no
 * leaves). */
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
    form: 'hierarchy-tree', name: 'Hierarchy Tree', family: 'structure',
    encode: { name: 'text', parent: 'text', level: 'category', count: 'integer', place: 'text' },
    labels: ['root_sub', 'groups', 'apart', 'card_sub', 'card_sub_none', 'drop', 'single', 'shared_level', 'shared_words', 'apart_level', 'apart_words', 'note_field'],
    phone: 'differs',
    draw: function (c) {
      var L = c.labels, W = c.width, en = c.field('name'), ep = c.field('parent'), el = c.field('level'), ec = c.field('count'), eg = c.field('place');
      var P = K.parts, spine = 12, ind = 28, cg = 16, vg = 16, sub_in = 16, G = L.groups || {}, apart = (L.apart || []).map(String);
      var ty = function (s) { return K.typeset({ typography: c.spec.typography || { curl_quotes: true, nbsp: true } }, String(s).replace(/[ \t\n]+/g, ' ')); };
      var short = function (s) { s = String(s); (L.drop || []).forEach(function (p) { if (s.indexOf(p) === 0) s = s.slice(p.length); }); return s; };
      var fill = function (t, o) { return String(t || '').replace(/\{(\w)\}/g, function (_, k) { return o[k] === undefined ? '' : String(o[k]); }); };
      var root = c.rows.filter(function (r) { return !r[ep]; })[0];
      if (!root) { c.warn('hierarchy-tree: no row without a parent'); return; }
      var kids = c.rows.filter(function (r) { return String(r[ep]) === String(root[en]); });
      // where the kit draws only the first rows (a desk's phone drawing, c.all_rows every row), a child whose leaves are
      // not all among them is left out, so no card prints a part of its count as the whole
      var all = c.all_rows || c.rows;
      kids = kids.filter(function (k) { return c.rows.filter(function (r) { return String(r[ep]) === String(k[en]); }).length === all.filter(function (r) { return String(r[ep]) === String(k[en]); }).length; });
      var leaves = function (k) { return c.rows.filter(function (r) { return String(r[ep]) === String(k[en]); }); };
      var ncol = Math.max(1, Math.floor((W - ind + cg) / (210 + cg))), cw = (W - ind - cg * (ncol - 1)) / ncol;
      if (ncol === 1) c.arrange('phone');
      var szo = { lines: 6, sub_lines: 4 };
      var rsub = ty(fill(L.root_sub, { n: root[ec] })), rname = ty(root[en]);
      var rs = P.node_size(c, rname, Object.assign({ max: Math.min(W, 360), named: true, sub: rsub }, szo)) || { w: Math.min(W, 360), h: 48 };
      var rb = { x: 0, y: 0, w: rs.w, h: rs.h }, y = rb.h + 18, heads = [];
      // a place's row: its name, then each leaf's own name (less the place) and count
      var row_words = function (place, ls) {
        var parts = ls.map(function (r) {
          if (L.shared_level && String(r[el]) === String(L.shared_level)) return fill(L.shared_words, { n: r[ec] }).replace(/ /g, '\u00a0');
          var sg = (L.single || 'District of') + ' ' + place, nm = short(r[en]);
          nm = nm === place ? '' : nm.split(' ' + sg).join('').split(sg).join('').trim();
          return (nm ? nm + '\u00a0' : '') + r[ec];   // a leaf's name holds its count
        });
        var odd = L.apart_level && ls.some(function (r) { return String(r[el]) === String(L.apart_level); });
        return { words: ty(place + ': ' + parts.join(', ') + (odd && L.apart_words ? ', ' + L.apart_words : '')), odd: odd };
      };
      var group = function (list, head, list_n) {
        if (!list.length) return;
        var hb = c.text(ind, y + c.size('label') * 0.93, fill(head, { n: list_n === undefined ? list.length : list_n }), { role: 'label', weight: 700, max: W - ind });
        heads.push(y + c.size('label') * 0.6);
        // each card laid out first, so the columns can be cut in order and balanced by height
        var cards = list.map(function (k) {
          var ls = leaves(k), d = ls.reduce(function (s, r) { return s + (+r[ec] || 0); }, 0);
          var places = [], byp = {};
          ls.forEach(function (r) { var p = String(r[eg]); if (!byp[p]) { byp[p] = []; places.push(p); } byp[p].push(r); });
          var sub = ty(fill(ls.length ? L.card_sub : (L.card_sub_none || L.card_sub), { n: k[ec], d: d })) + (!ls.length && L.note_field && k[L.note_field] ? '. ' + ty(k[L.note_field]) : '');
          var items = [{ id: 'k', parent: null, words: ty(short(k[en])), sub: sub, head: true }].concat(places.map(function (p, j) {
            var rw = row_words(p, byp[p]);
            return { id: 'p' + j, parent: 'k', words: rw.words, odd: rw.odd, place: p };
          }));
          items.forEach(function (it) {
            var w = cw - (it.head ? 0 : sub_in);
            var s = P.node_size(c, it.words, Object.assign({ max: w, min: w, named: it.head, sub: it.sub, roles: it.head ? ['label'] : ['tick'], pad: it.head ? [10, 7] : (it.odd ? [8, 4] : [0, 3]), weight: it.head ? 700 : 400 }, szo));
            it.w = w; it.h = s ? s.h : 30;
          });
          var t2 = P.tree(items, { dir: 'indent', indent: sub_in, row_gap: 2 });
          t2.faults.forEach(function (f) { c.warn(f); });
          return { k: k, t: t2 };
        });
        var at = K_split(cards.map(function (cd) { return cd.t.height; }), ncol, vg);
        var cols = []; for (var i = 0; i < ncol; i++) cols.push(hb.bottom + 10);
        cards.forEach(function (cd, n) {
          var ci = at[n], x = ind + ci * (cw + cg), k = cd.k, t = cd.t, top = cols[ci];
          t.links.forEach(function (l) {
            var a = t.by[l.from], b = t.by[l.to], lx = x + 8, my = top + b.y + b.h / 2;
            P.link(c, { x: lx, y: top + a.y + a.h }, { x: lx, y: my }, { stroke: 'context', width: 1 });
            P.link(c, { x: lx, y: my }, { x: x + b.x - 3, y: my }, { stroke: 'context', width: 1 });
          });
          t.nodes.forEach(function (nd) {
            var it = nd.item, b = { x: x + nd.x, y: top + nd.y, w: nd.w, h: nd.h };
            var o = it.head ? { stroke: 'subject', named: true, sub: it.sub, roles: ['label'], pad: [10, 7], weight: 700 }
              : it.odd ? { fill: 'track', stroke: 'context', roles: ['tick'], pad: [8, 4], weight: 400 }
                : { fill: 'surface', stroke: false, roles: ['tick'], pad: [0, 3], weight: 400, text: 'label' };
            if (it.odd) o.text = 'label';
            if (!P.node(c, b, it.words, Object.assign({ align: 'start', data: { key: it.head ? String(k[en]) : it.place, field: it.head ? 'court' : 'place', value: it.words } }, szo, o))) c.warn('hierarchy-tree: the words of ' + it.words + ' do not fit their box at ' + W + ' px');
          });
          cols[ci] = top + t.height + vg;
        });
        y = Math.max.apply(null, cols) - vg + 26;
      };
      // a group's count reads every row, where the kit draws only the first rows (a desk's phone drawing)
      var all_kids = (c.all_rows || c.rows).filter(function (r) { return String(r[ep]) === String(root[en]); });
      group(kids.filter(function (k) { return apart.indexOf(String(k[en])) < 0; }), G.main, all_kids.filter(function (k) { return apart.indexOf(String(k[en])) < 0; }).length);
      group(kids.filter(function (k) { return apart.indexOf(String(k[en])) >= 0; }), G.apart, all_kids.filter(function (k) { return apart.indexOf(String(k[en])) >= 0; }).length);
      heads.forEach(function (hy, i) {
        P.link(c, { x: spine, y: i ? heads[i - 1] : rb.h }, { x: spine, y: hy }, { stroke: 'context', width: 1 });
        P.link(c, { x: spine, y: hy }, { x: ind - 6, y: hy }, { stroke: 'context', width: 1 });
      });
      P.node(c, rb, rname, Object.assign({ stroke: 'subject', named: true, sub: rsub, align: 'start', data: { key: 'root', field: 'court', value: rname } }, szo));
      c.height(y - 26 + 1);
    }
  });
})(globalThis.OAChart);
