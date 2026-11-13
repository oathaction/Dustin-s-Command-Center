/* Comparison cards (coverage plan 3.16, core; S91). Two or three options side by side, one card each, every card one
 * width and one height with a hairline edge and no fill, its name first and then the same fields in the same order, as
 * live HTML text (R4-3): a list of cards whose fields are a term and its value. One card a row on a phone. No ink by
 * option (the data lead's round 4 ruling (b)). A field the law leaves empty prints the file's own words.
 * encode: key (the row's key), name (text: the option's name).
 * labels: fields ([{field, label, format (a kit format, default text), notes ({key: a line printed under that card's
 * value})}]), in the order every card prints them. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'comparison-cards', name: 'Comparison Cards', family: 'infographics',
    encode: { key: 'id', name: 'text' },
    labels: ['fields'],
    phone: 'same',
    html: function (h) {
      var ek = h.field('key'), en = h.field('name'), fs = h.labels.fields || [];
      return '<ul class="oac-h-cards" role="list">' + h.rows.map(function (r, i) {
        return '<li class="oac-h-item"' + h.row(i) + '><p class="oac-h-name">' + h.words(r[en]) + '</p><dl class="oac-h-fields">' +
          fs.map(function (f) {
            var v = r[f.field], note = (f.notes || {})[String(r[ek])];
            return '<dt class="oac-h-k">' + h.words(f.label) + '</dt><dd class="oac-h-v">' + h.words(h.fmt(v, f.format || 'text')) +
              (note ? '<p class="oac-h-small">' + h.words(note) + '</p>' : '') + '</dd>';
          }).join('') + '</dl></li>';
      }).join('') + '</ul>';
    }
  });
})(globalThis.OAChart);
