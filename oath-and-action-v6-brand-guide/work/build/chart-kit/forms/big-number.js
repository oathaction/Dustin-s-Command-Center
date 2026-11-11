/* Big number in context (coverage plan 3.9, core; S01). One figure set large with its caption, a few related shares as bars
 * on a 0 to 100 track beside it, and recorded votes as split bars with the threshold a vote needed. Party marks take neutral
 * inks with the party named on them (DR-48).
 * encode: key (id), value (number). labels: big_key, big_caption, bars_title, bars ([{key, label, party}]), bars_max,
 * votes_title, votes ([{label, date, tally, yes, no, needed, yes_words, no_words, short}]); yes_words and no_words take {v}.
 * formats: big, bars. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'big-number',
    name: 'Big Number In Context',
    family: 'gauges-and-indicators',
    encode: { key: 'id', value: 'number' },
    labels: ['big_key', 'big_caption', 'bars_title', 'bars', 'bars_max', 'votes_title', 'votes'],
    phone: 'differs',
    draw: function (c) {
      var rows = c.rows, ek = c.field('key'), ev = c.field('value'), f = c.spec.formats || {}, W = c.width;
      var by = {};
      rows.forEach(function (r) { by[r[ek]] = r; });
      var get = function (k) { if (!by[k]) { c.warn('no row with key ' + k); return null; } return by[k]; };
      var big = get(c.label('big_key'));
      var bigsize = c.size('big'), y = 0;
      var colw = c.phone ? W : Math.round(W * 0.42);
      if (big) {
        var bt = c.text(0, bigsize * 0.97, K.fmt(big[ev], f.big || 'number'), { role: 'big', weight: 800, data: { key: big[ek], field: ev, value: big[ev] } });
        var cap = c.text(0, bt.y + bt.h + 10 + c.size('label'), c.label('big_caption'), { role: 'label', weight: 600, max: Math.min(colw - 8, 260) });
        y = cap.y + cap.h;
      }
      // the bars beside the figure (below it on a phone)
      var bx = c.phone ? 0 : Math.round(W * 0.47), bw = W - bx, top = c.phone ? y + 34 : 4;
      var bars = c.labels.bars || [];
      var max = c.labels.bars_max || 100;
      if (bars.length) {
        c.text(bx, top + 10, c.label('bars_title'), { role: 'eyebrow', weight: 600, fill: 'secondary' });
        var yy = top + 22;
        var bh = c.t('bar-height');
        bars.forEach(function (b) {
          var r = get(b.key);
          if (!r) return;
          c.text(bx, yy + 16, b.label, { role: 'label', weight: 600 });
          var y0 = yy + 26, xs = K.scale.linear([0, max], [bx, bx + bw]);
          c.rect(bx, y0, bw, bh, { fill: 'track', mark: false });
          c.rect(bx, y0, xs(r[ev]) - bx, bh, { fill: 'party', kind: 'bar', axis: 'x', zero: bx, data: { key: r[ek], field: ev, value: r[ev], party: b.party || b.label } });
          c.text(xs(r[ev]) - 8, y0 + bh / 2 + c.size('label') * 0.35, K.fmt(r[ev], f.bars || 'percent:0'), { role: 'label', weight: 700, anchor: 'end', fill: 'label-on-subject' });
          yy = y0 + bh + 14;
        });
        c.text(bx, yy + 6, K.fmt(0, 'integer'), { role: 'tick' });
        c.text(bx + bw, yy + 6, K.fmt(max, f.bars || 'percent:0'), { role: 'tick', anchor: 'end' });
        y = Math.max(y, yy + 12);
      }
      // recorded votes: for, against, and the number needed
      var votes = c.labels.votes || [];
      if (votes.length) {
        y += 30;
        c.line(0, y, W, y, { stroke: 'gridline', width: c.t('line-hairline'), mark: false });
        y += 28;
        c.text(0, y, c.label('votes_title'), { role: 'eyebrow', weight: 600, fill: 'secondary' });
        y += 14;
        var vh = c.t('bar-height');
        votes.forEach(function (v) {
          var yes = get(v.yes), no = get(v.no), need = v.needed ? get(v.needed) : null;
          if (!yes || !no) return;
          var tot = yes[ev] + no[ev], xs = K.scale.linear([0, tot], [0, W]);
          var ly = y + c.size('label') + 6;
          var lb = c.text(0, ly, v.label, { role: 'label', weight: 600, max: c.phone ? W - 8 : W * 0.6 });
          if (v.tally) c.text(W, c.phone ? lb.y + lb.h + c.size('label') + 2 : ly, v.tally, { role: 'label', weight: 700, anchor: 'end' });
          if (v.date && !c.phone) c.text(W * 0.62, ly, v.date, { role: 'tick', anchor: 'middle' });
          var y0 = (c.phone ? lb.y + lb.h + c.size('label') + 10 : ly + 8);
          var mid = y0 + vh / 2 + c.size('label') * 0.35;
          var sp = v.split, parts = null;
          if (sp && c.extra[sp.dataset]) {
            parts = c.extra[sp.dataset].filter(function (r) { return Object.keys(sp.where || {}).every(function (k) { return String(r[k]) === String(sp.where[k]); }); });
            var sy = parts.reduce(function (a, r) { return a + (r[sp.yes] || 0); }, 0), sn = parts.reduce(function (a, r) { return a + (r[sp.no] || 0); }, 0);
            if (sy !== yes[ev] || sn !== no[ev]) c.warn('the party split of "' + v.label + '" gives ' + sy + ' to ' + sn + ', the totals ' + yes[ev] + ' to ' + no[ev]);
          } else if (sp) c.warn('split names dataset ' + sp.dataset + ', which the spec does not list');
          if (parts) {
            // each party's votes as its own segment in the one neutral ink of its side, its name and count on the mark
            var small = [], x = 0;
            [[sp.yes, 'party', 'label-on-subject'], [sp.no, 'light-fill', 'label']].forEach(function (side, si) {
              parts.forEach(function (r) {
                var n = r[side[0]] || 0;
                if (!n) return;
                var w = xs(n), words = String(v.party_words || '{party} {v}').replace('{party}', r[sp.party]).replace('{v}', K.fmt(n, 'integer'));
                c.rect(x, y0, w, vh, { fill: side[1], kind: x === 0 ? 'bar' : 'segment', axis: 'x', zero: 0, data: { key: (si ? no : yes)[ek] + '|' + r[sp.party], field: side[0], value: n, party: r[sp.party] } });
                if (x > 0) c.line(x, y0, x, y0 + vh, { stroke: 'surface', width: 2, mark: false });
                if (c.measure(words, 'label', 700) + 14 < w) c.text(si ? x + w - 7 : x + 7, mid, words, { role: 'label', weight: 700, fill: side[2], anchor: si ? 'end' : 'start' });
                else small.push([x + w / 2, words]);
                x += w;
              });
            });
            // segments too narrow for their words: the words in one row under the bar, each on an elbow leader from its segment
            var ty = y0 + vh + 14 + c.size('tick'), right = -1e9, rowsN = small.length ? 1 : 0;
            small.forEach(function (p) {
              var tw = c.measure(p[1], 'tick', 600), lx = Math.max(p[0] - 3, 0, right + 16);
              if (lx + tw > W) {
                if (right > -1e9 && W - tw < right + 16) { ty += c.size('tick') + 8; rowsN++; right = -1e9; }
                lx = Math.min(Math.max(p[0] - 3, 0, right + 16), W - tw);
              }
              c.text(lx, ty, p[1], { role: 'tick', weight: 600 });
              var top = ty - c.size('tick') - 3;
              c.line(p[0], y0 + vh + 1, p[0], top, { stroke: 'leader', width: c.t('line-hairline'), mark: false });
              if (lx > p[0] + 1) c.line(p[0], top, lx, top, { stroke: 'leader', width: c.t('line-hairline'), mark: false });
              right = lx + tw;
            });
            y = y0 + vh + (rowsN ? rowsN * (c.size('tick') + 8) + 10 : 0);
          } else {
            c.rect(0, y0, xs(yes[ev]), vh, { fill: 'subject', kind: 'bar', axis: 'x', zero: 0, data: { key: yes[ek], field: ev, value: yes[ev] } });
            c.rect(xs(yes[ev]), y0, W - xs(yes[ev]), vh, { fill: 'light-fill', kind: 'segment', data: { key: no[ek], field: ev, value: no[ev] } });
            c.text(8, mid, String(v.yes_words || '{v}').replace('{v}', K.fmt(yes[ev], 'integer')), { role: 'label', weight: 700, fill: 'label-on-subject' });
            c.text(W - 8, mid, String(v.no_words || '{v}').replace('{v}', K.fmt(no[ev], 'integer')), { role: 'label', weight: 700, anchor: 'end' });
            y = y0 + vh;
          }
          if (need) {
            var nx = xs(need[ev]);
            var nb = y;   // under the bar, and under any party words set beneath it
            c.line(nx, y0 - 6, nx, nb + 22, { stroke: 'label', width: c.t('line-hairline'), data: { key: need[ek], field: ev, value: need[ev] } });
            if (v.short) c.text(Math.min(nx, W - c.measure(v.short, 'label', 600)), nb + 22 + c.size('label'), v.short, { role: 'label', weight: 600, anchor: 'start' });
            y = nb + 22 + c.size('label') + 6;
          }
          y += 24;
        });
      }
      c.height(y);
    }
  });
})(globalThis.OAChart);
