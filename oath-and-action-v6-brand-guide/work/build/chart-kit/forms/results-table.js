/* Results table with margin cells (coverage plan 3.15, core; S15). One row per state: the later margin with the leader named,
 * a bar from the center line toward the leader's side, the earlier margin in gray, and the shift as an arrow; party named
 * in words, neutral inks (DR-48, DR-58); a row whose leader changed carries a tag; the nation's row set apart (DR-64).
 * encode: key (code), label (text), from (number), to (number), shift (number), scope (category, optional).
 * labels: titles ({label, to, from, shift}), lead ({neg, pos}), tag, apart_value, even_line (words on the line where the
 * leader changes, optional). formats: margin, shift. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'results-table', name: 'Results Table', family: 'tables-and-plain-words',
    encode: { key: 'code', label: 'text', from: 'number', to: 'number', shift: 'number', scope: 'category?' },
    labels: ['titles', 'lead', 'tag', 'apart_value', 'even_line'],
    phone: 'differs',
    draw: function (c) {
      var rows = c.rows, ek = c.field('key'), el = c.field('label'), ef = c.field('from'), et = c.field('to'), esh = c.field('shift'), esc = c.field('scope', false);
      var L = c.labels, f = c.spec.formats || {}, W = c.width, T = L.titles || {}, lead = L.lead || {}, size = c.size('tick');
      var words = function (v) { return (lead[v < 0 ? 'neg' : 'pos'] || '') + ' +' + K.fmt(Math.abs(v), f.margin || 'number:1'); };
      var nw = 0;
      rows.forEach(function (r) { nw = Math.max(nw, c.measure(r[el], 'label', 600)); });
      nw = Math.min(nw + 12, c.phone ? 112 : 150);
      var sw = c.phone ? 64 : 90, mw = (W - nw - sw) / (c.phone ? 1 : 2);
      if (c.phone) nw = 0;
      var mx = Math.max.apply(null, rows.map(function (r) { return Math.max(Math.abs(r[ef]), Math.abs(r[et])); }));
      var y = 0, hb = c.t('results-bar');
      c.text(0, y + size, T.label || '', { role: 'tick', weight: 700 });
      if (!c.phone) c.text(nw + mw / 2, y + size, T.to || '', { role: 'tick', weight: 700, anchor: 'middle' });
      if (!c.phone) c.text(nw + mw + mw / 2, y + size, T.from || '', { role: 'tick', weight: 700, anchor: 'middle' });
      var sh = c.text(W, y + size, T.shift || '', { role: 'tick', weight: 700, anchor: 'end', max: sw });
      y = Math.max(y + size, sh.y + sh.h) + 10;
      c.line(0, y, W, y, { stroke: 'baseline', width: c.t('line-baseline'), mark: false });
      var smax = Math.max.apply(null, rows.map(function (r) { return Math.abs(r[esh]); }));
      var cell = function (x0, w, v, yy, strong, key, field) {
        var mid = x0 + w / 2, len = (w / 2 - 6) * Math.abs(v) / mx, dir = v < 0 ? -1 : 1;
        c.line(mid, yy - 12, mid, yy + 12, { stroke: 'gridline', width: c.t('line-hairline'), mark: false });
        c.rect(dir < 0 ? mid - len : mid, yy + 4, len, hb, { fill: strong ? 'subject' : 'context', kind: 'bar', axis: 'x', zero: mid, data: { key: key, field: field, value: v, party: lead[v < 0 ? 'neg' : 'pos'] } });
        var txt = words(v);
        c.text(dir < 0 ? mid - 4 : mid + 4, yy, txt, { role: 'tick', weight: strong ? 700 : 400, anchor: dir < 0 ? 'end' : 'start', fill: strong ? 'label' : 'secondary' });
      };
      var pitch = c.phone ? 44 : 34;
      var prev = null;
      rows.forEach(function (r, i) {
        var apart = esc && String(r[esc]) === String(L.apart_value);
        if (prev !== null && !apart && L.even_line && (prev < 0) !== (r[et] < 0)) {
          y += 8;
          c.line(0, y, W, y, { stroke: 'baseline', width: c.t('line-baseline'), mark: false });
          y += 4;
          var ev = c.text(W / 2, y + size + 2, L.even_line, { role: 'tick', weight: 600, anchor: 'middle', max: W - 20 });
          y = ev.y + ev.h + 2;
        }
        if (!apart) prev = r[et];
        var yy = y + pitch / 2 + 2;
        var tagged = L.tag && (r[ef] < 0) !== (r[et] < 0);
        var nb = c.text(0, c.phone ? y + 18 : yy, r[el], { role: 'label', weight: 600, size: c.size('tick') + 1, max: c.phone ? W - sw - 10 : nw - 6 });
        if (tagged) {
          var tw = c.measure(L.tag, 'tick', 600) + 8, tgx = c.phone ? nb.x + nb.w + 8 : 0, tgy = c.phone ? y + 5 : yy + 5;
          c.rect(tgx + 0.5, tgy + 0.5, tw, 17, { stroke: 'label', mark: false }); c.text(tgx + 4, tgy + 13, L.tag, { role: 'tick', weight: 600 });
        }
        var cy = c.phone ? y + 40 : yy;
        cell(c.phone ? 0 : nw, c.phone ? W - sw : mw, r[et], cy, true, r[ek], et);
        if (!c.phone) cell(nw + mw, mw, r[ef], yy, false, r[ek], ef);
        var sy = c.phone ? y + 18 : yy;
        var al = (sw - 40) * Math.abs(r[esh]) / smax, ax = W - sw + 6;
        K.parts.arrow(c, ax, ax + Math.max(al, 4), sy - 4, { data: { key: r[ek], field: esh, value: r[esh] } });
        c.text(ax + Math.max(al, 4) + 6, sy, K.fmt(Math.abs(r[esh]), f.shift || 'number:1'), { role: 'tick' });
        y += (c.phone ? 60 : pitch) + (tagged && !c.phone ? 8 : 0);
        c.line(0, y, W, y, { stroke: 'gridline', width: c.t('line-hairline'), mark: false });
        if (apart) { y += 6; c.line(0, y, W, y, { stroke: 'baseline', width: c.t('line-baseline'), mark: false }); }
      });
      c.height(y + 4);
    }
  });
})(globalThis.OAChart);
