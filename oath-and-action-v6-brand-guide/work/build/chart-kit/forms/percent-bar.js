/* 100 percent bar (coverage plan 3.4, core; S10). One bar per row split into its parts' shares of the row's total, the first
 * part's share printed at the right; parts read in grayscale by step and pattern.
 * encode: category (text), parts (list of count columns, in order), total (number, optional; else the parts' sum).
 * labels: parts ([{field, label, fill, pattern}]; fill is a color role such as subject, mag-3, light-fill), share (words with
 * {p} and {total}), mark_at (a share, 0 to 100, drawn as a line across every bar), mark_label. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'percent-bar', name: 'One Hundred Percent Bar', family: 'composition',
    encode: { category: 'text', parts: 'list', total: 'number?' },
    labels: ['parts', 'share', 'mark_at', 'mark_label', 'share_head'],
    phone: 'same',
    draw: function (c) {
      var P = K.parts, rows = c.rows, ek = c.field('category'), parts = c.field('parts'), et = c.field('total', false);
      var W = c.width, L = c.labels, defs = L.parts || [], y = 0;
      var byf = {};
      defs.forEach(function (d) { byf[d.field] = d; });
      y += c.size('label') + 2;
      y += P.key(c, parts.map(function (p) { var d = byf[p] || {}; return { label: d.label || p, fill: d.pattern ? null : (d.fill || 'subject'), stroke: d.pattern ? 'subject' : null, pattern: d.pattern }; }), 0, y, W) + 14;
      if (L.share_head) { c.text(W, y - 6, L.share_head, { role: 'tick', anchor: 'end', fill: 'secondary' }); y += 8; }
      var lw = 0;
      rows.forEach(function (r) { lw = Math.max(lw, c.measure(r[ek], 'label', 600)); });
      var sw = 0;
      var share = function (r) {
        var tot = et ? r[et] : parts.reduce(function (s, p) { return s + (r[p] || 0); }, 0);
        return { tot: tot, p: tot ? Math.round(100 * (r[parts[0]] || 0) / tot) : 0 };
      };
      rows.forEach(function (r) { var s = share(r); sw = Math.max(sw, c.measure(String(L.share || '{p}%').replace('{p}', s.p).replace('{total}', s.tot), 'label', 700)); });
      var x0 = c.phone ? 0 : Math.ceil(lw + 20), x1 = W - sw - 14, bh = c.t(c.phone ? 'bar-phone-height' : 'bar-dense-height');
      var pitch = c.phone ? c.t('bar-phone-pitch') - 8 : c.t('bar-dense-pitch') - 12;
      rows.forEach(function (r, i) {
        var s = share(r), by = y + i * pitch + (c.phone ? c.size('label') + 6 : 0), x = x0;
        if (c.phone) c.text(0, by - 6, r[ek], { role: 'label', weight: 600 });
        else c.text(0, by + bh / 2 + c.size('label') * 0.35, r[ek], { role: 'label', weight: 600 });
        parts.forEach(function (p, j) {
          var v = r[p] || 0, w = s.tot ? (x1 - x0) * v / s.tot : 0, d = byf[p] || {};
          if (!w) return;
          if (d.pattern) {
            c.pattern(d.pattern, 'subject');
            c.rect(x, by, w, bh, { pattern: d.pattern, kind: j ? 'segment' : 'bar', axis: 'x', zero: x0, data: { key: r[ek], field: p, value: v } });
            c.rect(x + 0.5, by + 0.5, Math.max(0, w - 1), bh - 1, { stroke: 'subject', mark: false });
          } else c.rect(x, by, w, bh, { fill: d.fill || 'subject', kind: j ? 'segment' : 'bar', axis: 'x', zero: x0, data: { key: r[ek], field: p, value: v } });
          x += w;
        });
        var words = String(L.share || '{p}%').split('{p}').join(s.p).split('{total}').join(K.fmt(s.tot, 'integer'));
        var sp = words.indexOf(' '), first = sp > 0 ? words.slice(0, sp) : words, rest = sp > 0 ? words.slice(sp) : '';
        var ty = by + bh / 2 + c.size('label') * 0.35;
        var rb = rest ? c.text(W, ty, rest.replace(/^\s+/, ''), { role: 'label', weight: 400, anchor: 'end' }) : { x: W };
        c.text(rest ? rb.x - c.measure(' ', 'label') : W, ty, first, { role: 'label', weight: 700, anchor: 'end' });
      });
      var bottom = y + (rows.length - 1) * pitch + bh + (c.phone ? c.size('label') + 6 : 0);
      if (L.mark_at !== undefined) {
        var mx = x0 + (x1 - x0) * L.mark_at / 100;
        c.line(mx, y - 8, mx, bottom + 4, { stroke: 'label', width: c.t('line-hairline'), mark: false });
        if (L.mark_label) c.text(mx, y - 12, L.mark_label, { role: 'tick', anchor: 'middle', weight: 600 });
      }
      c.height(bottom + 6);
    }
  });
})(globalThis.OAChart);
