/* By-the-numbers panel (coverage plan 3.16, core; S90). Four to six facts, each a figure set large with its words after
 * it in one sentence, and the table it comes from on a line of its own, as live HTML text (R4-3): a list of facts that
 * reflows, which a reader can search and copy. No mark, no fill, no ink by fact (the data lead's round 4 ruling (b)).
 * A fact may stand for several rows (the three revenue shares in one sentence); its figure is one row's value.
 * encode: key (the row's key), value (number), source (text: the table or file each row comes from).
 * labels: facts ([{rows: [keys the fact stands for], figure: the key whose value prints large, format (a kit format),
 * scale (a multiplier, as 1000 for a value held in thousands), before, after (words around the figure), words (the rest
 * of the sentence)}]), in reading order. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'by-the-numbers', name: 'By-the-Numbers Panel', family: 'infographics',
    encode: { key: 'id', value: 'number', source: 'text' },
    labels: ['facts'],
    phone: 'same',
    html: function (h) {
      var ek = h.field('key'), ev = h.field('value'), es = h.field('source'), at = {};
      h.rows.forEach(function (r, i) { at[String(r[ek])] = i; });
      return '<ul class="oac-h-facts" role="list">' + (h.labels.facts || []).map(function (f) {
        var ks = [].concat(f.rows || [f.figure]).map(String).filter(function (k) { return at[k] !== undefined; });
        var r = h.rows[at[String(f.figure)]];
        if (!r) throw new Error('by-the-numbers: labels.facts names no row ' + f.figure);
        // the figure keeps its unit on its line with a no-break space ("$994.9 billion")
        var fig = ((f.before || '') + h.fmt(r[ev] * (f.scale || 1), f.format || 'number') + (f.after || '')).replace(/(\d) (?=\S)/g, '$1 ');
        var src = [];
        ks.forEach(function (k) { var s = h.rows[at[k]][es]; if (s && src.indexOf(s) < 0) src.push(s); });
        return '<li class="oac-h-item"' + h.row(ks.map(function (k) { return at[k]; })) + '><p class="oac-h-body"><span class="oac-h-big">' +
          h.words(fig) + '</span> ' + h.words(f.words || '') + '</p><p class="oac-h-src">' + h.words(src.join('; ')) + '</p></li>';
      }).join('') + '</ul>';
    }
  });
})(globalThis.OAChart);
