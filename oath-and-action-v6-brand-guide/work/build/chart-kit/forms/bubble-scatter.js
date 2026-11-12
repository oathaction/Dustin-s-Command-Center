/* Bubble chart (coverage plan 3.6, extended; S55). The scatter plot with named points with a third measure as each
 * circle's area (D2-124), largest drawn first and each kept apart by an outline of the ground; a key of two or three
 * circle sizes sits over the plot. It draws through scatter-named's drawing, so the two forms place names, scales and
 * the reference point the same way (the kit loads every form before it draws).
 * encode: key (code), label (text), x (number), y (number), size (number).
 * labels, formats and scale: as scatter-named, with size_key ([values]), size_key_label ("{value}") and size_key_title.
 * On a phone the same arrangement draws narrower, with smaller circles. Maker B, round 2. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'bubble-scatter',
    name: 'Bubble Scatter',
    family: 'correlation',
    encode: { key: 'code', label: 'text', x: 'number', y: 'number', size: 'number' },
    labels: ['named', 'point', 'labeled', 'names', 'reference', 'reference_label', 'x_axis', 'y_axis', 'size_key', 'size_key_label', 'size_key_title', 'sub', 'sub_short'],
    phone: 'same',
    draw: function (c) {
      var base = K.forms['scatter-named'];
      if (!base) throw new Error('bubble-scatter draws through scatter-named; load forms/scatter-named.js');
      base.draw(c);
    }
  });
})(globalThis.OAChart);
