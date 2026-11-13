/* Roll-call grid (coverage plan 3.11, extended; S72). One square a member, every square in the party-mark ink: a yes
 * vote solid, a no vote in outline (1.2 px), a member not voting in the light fill, and a vacant seat as a ghost
 * outline. Each chamber is a panel headed by its vote, its date and the question and result in the record's words;
 * under it each party is a row of its own in a set order (Democrats first, then independents as the record lists them,
 * folded into no party, then Republicans; vacant seats between, S48's order), named in words with its count and how it
 * voted, its squares in that party's yes, no and not-voting order, row by row. Desk: the party's name at the left of its
 * squares; where that leaves under 20 squares a row, the name sits above them.
 * encode: chamber (category), party (category), vote (category: as recorded), roll (text: the vote's name),
 * date (date), question (text), result (text).
 * labels: chambers ([values]), seats ({chamber: seats}, so the vacant count is seats less members recorded),
 * parties ([values], the order), party_words ({value: [one, many]}), votes ([values], the order in a party),
 * vote_words ({value: words}), vacant ([one, many]), key ({yes, no, not, vacant}: the key's words), head (words with
 * {roll} and {date}), ask (words with {question} and {result}). */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'roll-call-grid', name: 'Roll-Call Grid', family: 'structure',
    encode: { chamber: 'category', party: 'category', vote: 'category', roll: 'text', date: 'date', question: 'text', result: 'text' },
    labels: ['chambers', 'seats', 'parties', 'party_words', 'votes', 'vote_words', 'vacant', 'key', 'head', 'ask'],
    phone: 'differs',
    draw: function (c) {
      var L = c.labels, W = c.width, E = {};
      ['chamber', 'party', 'vote', 'roll', 'date', 'question', 'result'].forEach(function (k) { E[k] = c.field(k); });
      var u = c.t('unit-size'), gp = c.t('unit-gap'), pitch = u + gp, size = c.size('label'), tick = c.size('tick');
      var votes = (L.votes || []).map(String), vw = L.vote_words || {}, pw = L.party_words || {}, KY = L.key || {};
      // words built here hold their dates with no-break spaces themselves, since the page carries the data's words already
      // set and does not set them again (parity)
      var ty = function (s) { return K.typeset({ typography: c.spec.typography || { curl_quotes: true, nbsp: true } }, String(s === null || s === undefined ? '' : s)); };
      var fill = function (t, o) { return String(t || '').replace(/\{(\w+)\}/g, function (_, k) { return o[k] === undefined ? '' : String(o[k]); }); };
      var nm = function (pair, n) { pair = [].concat(pair || ''); return n === 1 ? pair[0] : (pair[1] || pair[0]); };
      var lw = 0;
      // the label column: as wide as the widest party name with its count, where 12 squares a row still fit beside it
      (L.parties || []).concat(['vacant']).forEach(function (p) { lw = Math.max(lw, c.measure(nm(p === 'vacant' ? L.vacant : pw[p], 2) + ', 000', 'label', 700)); });
      lw = Math.ceil(lw) + 12;
      var side = W - lw >= 20 * pitch, gx = side ? lw : 0, per = Math.max(1, Math.floor((W - gx + gp) / pitch));
      if (!side) c.arrange('phone');
      var sq = function (x, y, kind, key) {
        var d = { key: key, field: 'vote', value: kind };
        if (kind === 'yes') c.rect(x, y, u, u, { fill: 'party', data: d });
        else if (kind === 'no') c.rect(x + 0.6, y + 0.6, u - 1.2, u - 1.2, { stroke: 'party', width: 1.2, data: d });
        else if (kind === 'vacant') c.rect(x + 0.5, y + 0.5, u - 1, u - 1, { stroke: 'ghost', width: 1, data: d });
        else c.rect(x, y, u, u, { fill: 'light-fill', data: d });
      };
      var kind_of = function (v) { var i = votes.indexOf(String(v)); return i === 0 ? 'yes' : i === 1 ? 'no' : 'not'; };
      // the key, once, over both panels
      var kh = K.parts.key(c, [{ label: KY.yes || 'Yes', fill: 'party' }, { label: KY.no || 'No', stroke: 'party' }, { label: KY.not || 'Not voting', fill: 'light-fill' }, { label: KY.vacant || 'Vacant', stroke: 'ghost' }], 0, size * 0.93, W);
      var y = kh + 10;
      (L.chambers || []).forEach(function (ch, ci) {
        var rows = c.rows.filter(function (r) { return String(r[E.chamber]) === String(ch); });
        if (!rows.length) return;
        var r0 = rows[0];
        if (ci) y += 22;
        c.line(0, y, W, y, { stroke: 'label', width: 1, mark: false });
        var hb = c.text(0, y + 8 + size * 0.93, ty(fill(L.head, { roll: r0[E.roll], date: K.fmt(r0[E.date], 'date'), chamber: ch })), { role: 'label', weight: 700, max: W });
        var ab = c.text(0, hb.bottom + 3 + tick * 0.93, ty(fill(L.ask, { question: r0[E.question], result: r0[E.result] })), { role: 'tick', fill: 'label', max: W });
        y = ab.bottom + 12;
        var groups = (L.parties || []).map(function (p) {
          var ms = rows.filter(function (r) { return String(r[E.party]) === String(p); });
          return { key: p, n: ms.length, kinds: ms.map(function (r) { return { k: kind_of(r[E.vote]), v: String(r[E.vote]) }; }) };
        }).filter(function (g) { return g.n; });
        var vac = Math.max(0, ((L.seats || {})[ch] || rows.length) - rows.length);
        // vacant seats sit between the first party and the rest
        if (vac) groups.splice(1, 0, { key: 'vacant', n: vac, kinds: Array.apply(null, Array(vac)).map(function () { return { k: 'vacant' }; }) });
        groups.forEach(function (g) {
          g.kinds.sort(function (a, b) { var o = ['yes', 'no', 'not', 'vacant']; return o.indexOf(a.k) - o.indexOf(b.k); });
          var name = g.key === 'vacant' ? nm(L.vacant, g.n) + ', ' + g.n : nm(pw[g.key], g.n) + ', ' + g.n;
          var cnt = {}; g.kinds.forEach(function (q) { cnt[q.v || q.k] = (cnt[q.v || q.k] || 0) + 1; });
          var sub = g.key === 'vacant' ? '' : votes.filter(function (v) { return cnt[v]; }).map(function (v) { return cnt[v] + ' ' + (vw[v] || v); }).join(', ');
          var top = y, nb = c.text(0, top + size * 0.93, ty(name), { role: 'label', weight: 700, max: side ? lw - 12 : W });
          var bottom = nb.bottom;
          if (sub) bottom = c.text(0, nb.bottom + 2 + tick * 0.93, ty(sub), { role: 'tick', fill: 'label', max: side ? lw - 12 : W }).bottom;
          var sy = side ? top + 3 : bottom + 6;
          g.kinds.forEach(function (q, i) { sq(gx + (i % per) * pitch, sy + Math.floor(i / per) * pitch, q.k, ch + ' ' + g.key + ' ' + i); });
          var sb = sy + Math.ceil(g.n / per) * pitch - gp;
          y = Math.max(side ? bottom : 0, sb) + 14;
        });
        y -= 14;
      });
      c.height(y + 1);
    }
  });
})(globalThis.OAChart);
