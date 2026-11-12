/* One sentence (coverage plan 3.15, core; S42). A finding a sentence states faster than any chart. The drawing is the
 * sentence itself, labels.sentence (the spec's title, word for word) set in the title face and wrapped to the width, so it doubles as the still image for
 * posts and cards. The spec's "show" prints the evidence label, this drawing, the source line and the folded table, and
 * leaves out the printed title so the sentence appears once. encode: value (number, a figure the sentence cites).
 * labels: sentence. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'one-sentence',
    name: 'One Sentence',
    family: 'tables-and-plain-words',
    encode: { value: 'number' },
    labels: ['sentence'],
    phone: 'same',
    draw: function (c) {
      var W = c.width, size = c.t(c.phone ? 'type-title-phone-size' : 'type-title-size');
      var lead = c.t(c.phone ? 'type-title-phone-leading' : 'type-title-leading');
      var tb = c.text(0, size, c.label('sentence'), { role: 'big', size: size, weight: 800, face: 'display', max: W, leading: lead, fill: 'label' });
      // the figures the sentence cites, recorded for the checks at the sentence's place (no extra marks)
      c.rows.forEach(function (r) { c.datum(0, size, { data: { key: r[c.field('value')], field: c.field('value'), value: r[c.field('value')] } }); });
      c.height(tb.bottom + 4);
    }
  });
})(globalThis.OAChart);
