/* Social data card (coverage plan 3.16, core; S95). A still image for Substack, email and social posts (DR-49), drawn at
 * true size for each crop the spec names (spec.card.crops; DR-268: 1080 by 1350 and 1080 by 1080): the evidence word and
 * the grade line, the title, one other form drawn at card scale through c.inner (encode.of), so the inner form's 13 px words print at the
 * card's floor, and under a hairline the card's short source line. Every word stands at 36 px or more at true size
 * (R4-4: 13 px in a feed that shows the card at about a third of its size), the title larger. The inner form keeps its
 * own inks, key and words and reads labels.card_inner as c.card, with the height the crop leaves it. No red and blue on
 * any election card (DR-64); a web address joins once the site is settled (DR-55). A crop that cannot hold the inner
 * form says so (c.warn) and the kit fails what runs past its foot.
 * encode: of (the inner form's ID) and the inner form's own names. labels: the inner form's labels, plus card_source (the
 * card's short source line), card_note (the line over the source that says what a mark stands for), card_inner (options
 * the inner form reads as c.card), card_title ([px on a tall crop, px on a square one], default [56, 46]). */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'social-data-card', name: 'Social Data Card', family: 'infographics', inner: true,
    encode: { of: 'form' },
    labels: ['card_source', 'card_note', 'card_inner', 'card_title'],
    phone: 'same',
    draw: function (c) {
      var inner = K.forms[c.encode.of];
      if (!inner || !inner.draw || inner.form === 'social-data-card') throw new Error('social-data-card: encode.of names no other drawn form');
      var L = c.labels, W = c.width, H = c.crop ? c.crop.h : Math.round(W * 1.25), tall = H > W * 1.1;
      var min = c.min_text || 36, pad = Math.round(W / (tall ? 15 : 18)), cw = W - 2 * pad, lh = Math.round(min * 1.3), k = min / c.t('type-tick');
      var ts = (L.card_title || [56, 46])[tall ? 0 : 1], y = pad;
      var ev = c.text(pad, y + min * 0.8, c.spec.evidence_label || '', { role: 'eyebrow', size: min, weight: 700 });
      // the grade line under the evidence word, as the figure prints it (R4-4)
      if (c.spec.grade_line) ev = c.text(pad, ev.bottom + 6 + min * 0.8, c.spec.grade_line, { role: 'tick', size: min, fill: 'secondary', max: cw, leading: lh });
      var t = c.text(pad, ev.bottom + 20 + ts * 0.8, c.spec.title, { role: 'label', face: 'display', size: ts, weight: 800, max: cw, leading: Math.round(ts * 1.12) });
      y = t.bottom + (tall ? 40 : 28);
      // the foot first (the line that says what a mark is, then the source), so the inner form takes what the crop leaves
      var nb = function (w) { return w ? K.wrap(K.typeset(c.spec, w), min, cw, 400, 'reading').length * lh : 0; };
      var note = L.card_note || '', src = L.card_source || c.spec.source_line || '', nh = nb(note), sh = nb(src);
      var fy = H - pad - sh - 24, ny = fy - (note ? nh + 20 : 0), room = ny - (tall ? 32 : 24) - y;
      // the inner form's lowest words hang about 16 px under the height it fills, so it is given that much less
      var ih = c.inner(pad, y, cw, k, Object.assign({}, L.card_inner || {}, { height: (room - 18) / k }));
      if (ih > room + 0.5) c.warn('social-data-card: the inner form runs ' + Math.round(ih - room) + ' px past the room the ' + (c.crop ? c.crop.name : '') + ' crop leaves it');
      if (note) c.text(pad, ny + min * 0.93, note, { role: 'label', size: min, fill: 'label', max: cw, leading: lh });
      c.line(pad, fy, W - pad, fy, { stroke: 'gridline', width: 2, mark: false });
      c.text(pad, fy + 24 + min * 0.93, src, { role: 'tick', size: min, fill: 'secondary', max: cw, leading: lh });
      c.height(H);
    }
  });
})(globalThis.OAChart);
