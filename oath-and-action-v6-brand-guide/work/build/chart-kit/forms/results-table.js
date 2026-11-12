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
    labels: ['titles', 'lead', 'tag', 'apart_value', 'even_line', 'phone_from', 'phone_to'],
    phone: 'differs',
    draw: function (c) {
      var rows = c.rows, ek = c.field('key'), el = c.field('label'), ef = c.field('from'), et = c.field('to'), esh = c.field('shift'), esc = c.field('scope', false);
      var L = c.labels, f = c.spec.formats || {}, W = c.width, T = L.titles || {}, lead = L.lead || {}, size = c.size('tick');
      var words = function (v) { return (lead[v < 0 ? 'neg' : 'pos'] || '') + ' +' + K.fmt(Math.abs(v), f.margin || 'number:1'); };
      var nw = 0, tw_max = 0;
      rows.forEach(function (r) {
        nw = Math.max(nw, c.measure(r[el], 'label', 600));
        tw_max = Math.max(tw_max, c.measure(words(r[et]), 'tick', 700), c.measure(words(r[ef]), 'tick', 400));
      });
      // the two margins side by side only where each fits its half of its column; else the phone's stacked rows (D3-93)
      var narrow = c.phone || (W - Math.min(nw + 12, 150) - 90) / 4 - 6 < tw_max;
      nw = Math.min(nw + 12, narrow ? 112 : 150);
      var sw = narrow ? 64 : 90, mw = (W - nw - sw) / (narrow ? 1 : 2);
      if (narrow) nw = 0;
      var mx = Math.max.apply(null, rows.map(function (r) { return Math.max(Math.abs(r[ef]), Math.abs(r[et])); }));
      var y = 0, hb = c.t('results-bar');
      c.text(0, y + size, T.label || '', { role: 'tick', weight: 700 });
      if (!narrow) c.text(nw + mw / 2, y + size, T.to || '', { role: 'tick', weight: 700, anchor: 'middle' });
      if (!narrow) c.text(nw + mw + mw / 2, y + size, T.from || '', { role: 'tick', weight: 700, anchor: 'middle' });
      var sh = c.text(W, y + size, T.shift || '', { role: 'tick', weight: 700, anchor: 'end', max: narrow ? Math.max(sw, W * 0.5) : sw });
      y = Math.max(y + size, sh.y + sh.h) + 10;
      c.line(0, y, W, y, { stroke: 'baseline', width: c.t('line-baseline'), mark: false });
      var smax = Math.max.apply(null, rows.map(function (r) { return Math.abs(r[esh]); }));
      var cell = function (x0, w, v, yy, strong, key, field) {
        var mid = x0 + w / 2, len = (w / 2 - 6) * Math.abs(v) / mx, dir = v < 0 ? -1 : 1;
        c.line(mid, yy - 12, mid, yy + 12, { stroke: 'gridline', width: c.t('line-hairline'), mark: false });
        c.rect(dir < 0 ? mid - len : mid, yy + 4, len, hb, { fill: strong ? 'subject' : 'context', kind: 'bar', axis: 'x', zero: mid, data: { key: key, field: field, value: v, party: lead[v < 0 ? 'neg' : 'pos'] } });
        // the words sit over the bar on the leader's side, kept inside the cell
        var txt = words(v), tw = c.measure(txt, 'tick', strong ? 700 : 400);
        var tx = dir < 0 ? Math.max(mid - 4, x0 + tw) : Math.min(mid + 4, x0 + w - tw);
        c.text(tx, yy, txt, { role: 'tick', weight: strong ? 700 : 400, anchor: dir < 0 ? 'end' : 'start', fill: strong ? 'label' : 'secondary' });
      };
      var pitch = narrow ? 44 : 34;
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
        var nb = c.text(0, narrow ? y + 18 : yy, r[el], { role: 'label', weight: 600, size: c.size('tick') + 1, max: narrow ? W - sw - 10 : nw - 6 });
        if (tagged) {
          var tw = c.measure(L.tag, 'tick', 600) + 8, tgx = narrow ? nb.x + nb.w + 8 : 0, tgy = narrow ? y + 5 : yy + 5;
          c.rect(tgx + 0.5, tgy + 0.5, tw, 17, { stroke: 'label', mark: false }); c.text(tgx + 4, tgy + 13, L.tag, { role: 'tick', weight: 600 });
        }
        var cy = narrow ? y + 40 : yy;
        cell(narrow ? 0 : nw, narrow ? W - sw : mw, r[et], cy, true, r[ek], et);
        if (!narrow) cell(nw + mw, mw, r[ef], yy, false, r[ek], ef);
        else if (L.phone_from) c.text(0, cy + 26, String(L.phone_from).replace('{from}', words(r[ef])), { role: 'tick', fill: 'secondary' });
        var sy = narrow ? y + 18 : yy;
        var al = (sw - 40) * Math.abs(r[esh]) / smax, ax = W - sw + 6;
        K.parts.arrow(c, ax, ax + Math.max(al, 4), sy - 4, { data: { key: r[ek], field: esh, value: r[esh] } });
        c.text(ax + Math.max(al, 4) + 6, sy, K.fmt(Math.abs(r[esh]), f.shift || 'number:1'), { role: 'tick' });
        y += (narrow ? (L.phone_from ? 78 : 60) : pitch) + (tagged && !narrow ? 8 : 0);
        c.line(0, y, W, y, { stroke: 'gridline', width: c.t('line-hairline'), mark: false });
        if (apart) { y += 6; c.line(0, y, W, y, { stroke: 'baseline', width: c.t('line-baseline'), mark: false }); }
      });
      c.height(y + 4);
    }
  });
})(globalThis.OAChart);
