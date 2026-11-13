/* Step-by-step (coverage plan 3.16, core; S92). What a reader does, in order: one numbered step a row, its action in
 * bold, what it takes, the time the law allows and the law's section, as live HTML text (R4-3). The numbers and the line
 * joining them are the one drawing part, set by the list's own CSS (a counter on a disc in the subject ink); an optional
 * step takes an outlined disc and says it is optional in words (the data lead's round 4 ruling (b)). A step another acts
 * at names who acts.
 * encode: key (the row's key), path (category: labels.main marks a step every request takes), step (text: the action),
 * what (text, optional), who (text, optional), limit (text, optional: the time the law allows), basis (text, optional:
 * the section).
 * labels: main (default "main"), branches ({key: the words that open an optional step, as "Optional: ..."}), you (the
 * who value that means the reader, printed nowhere), limit_words (the words a limit prints in, {limit} for the column's
 * words; default "{limit}"), stop (a mark set after a what line that ends without one, as "."). */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'step-by-step', name: 'Step-by-Step', family: 'infographics',
    encode: { key: 'id', path: 'category', step: 'text', what: 'text?', who: 'text?', limit: 'text?', basis: 'text?' },
    labels: ['main', 'branches', 'you', 'limit_words', 'stop'],
    phone: 'same',
    html: function (h) {
      var L = h.labels, ek = h.field('key'), ep = h.field('path'), es = h.field('step');
      var f = function (n) { var c = h.encode[n]; return c ? c : null; };
      var ew = f('what'), eo = f('who'), el = f('limit'), eb = f('basis'), mv = String(L.main || 'main'), B = L.branches || {};
      var p = function (cls, w) { return w ? '<p class="' + cls + '">' + h.words(w) + '</p>' : ''; };
      return '<ol class="oac-h-steps" role="list">' + h.rows.map(function (r, i) {
        var opt = String(r[ep]) !== mv, k = String(r[ek]);
        return '<li class="oac-h-item' + (opt ? ' oac-h-branch' : '') + '"' + h.row(i) + '>' +
          p('oac-h-small', opt ? B[k] : '') +
          p('oac-h-name', r[es]) +
          p('oac-h-small', eo && r[eo] && String(r[eo]) !== String(L.you) ? r[eo] : '') +
          p('oac-h-body', ew && r[ew] ? String(r[ew]) + (L.stop && !/[.?!]$/.test(String(r[ew])) ? L.stop : '') : '') +
          (el && r[el] ? '<p class="oac-h-small">' + String(L.limit_words || '{limit}').split('{limit}').map(function (w) { return h.words(w); }).join('<strong>' + h.words(r[el]) + '</strong>') + '</p>' : '') +
          p('oac-h-src', eb ? r[eb] : '') + '</li>';
      }).join('') + '</ol>';
    }
  });
})(globalThis.OAChart);
