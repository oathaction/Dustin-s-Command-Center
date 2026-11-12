/* Step tracker (coverage plan 3.9, core; S62). One bill's six steps as chapter 11 draws them (Rules 11.1 to 11.3,
 * 11.5 and 11.6): numbered circles, filled for a step done, a heavy ring on the step the bill is at now, a fine ring on
 * a step ahead, and a step that never happened keeps its number under a slash. Each step gives its name, its state in
 * words with its date, and a note. Across the row where each step's sixth holds its date on one line (720 px for
 * dates in full), each mark at its sixth's left edge with its words flush left beneath, states and dates on shared
 * lines; narrower, the steps run down the page with the words beside each mark (Rule 11.6). The end words follow the marks.
 * Each step's date is the first action whose code the step lists; a step with no action before a later step done
 * never happened (Rule 11.2).
 * encode: date (date), code (code: the action's code), action (text).
 * labels: steps ([{name, codes, note}], six), states ({done, now, ahead, never}: the state words), became (end words
 * with {date}), now_words (end words while the bill moves, with {n} and {step}). */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'step-tracker', name: 'Step Tracker', family: 'gauges-and-indicators',
    encode: { date: 'date', code: 'code', action: 'text' },
    labels: ['steps', 'states', 'became', 'now_words'],
    phone: 'differs',
    draw: function (c) {
      var ed = c.field('date'), ec = c.field('code'), L = c.labels, W = c.width, steps = L.steps || [], S = L.states || {};
      var size = c.size('label'), tick = c.size('tick'), note = c.size('note'), nlh = c.t('type-note-leading');
      var hits = steps.map(function (st) {
        var m = c.rows.filter(function (r) { return (st.codes || []).map(String).indexOf(String(r[ec])) >= 0; })
          .sort(function (a, b) { return String(a[ed]) < String(b[ed]) ? -1 : 1; });
        return m[0] || null;
      });
      var last = -1; hits.forEach(function (h, i) { if (h) last = i; });
      var law = last === steps.length - 1, now = law ? steps.length : last + 1;
      var state = function (i) { return hits[i] ? 'done' : i < last ? 'never' : i === now ? 'now' : 'ahead'; };
      // across only where each step's sixth holds its date on one line
      var dw = 0; hits.forEach(function (h) { if (h) dw = Math.max(dw, c.measure(K.fmt(h[ed], 'date'), 'tick')); });
      var wide = W >= 552 && W / steps.length - 6 >= dw, d = wide ? 30 : 28, r = d / 2, nsize = 14;
      var mark = function (i, cx, cy) {
        var stt = state(i), n = String(i + 1), ty = cy + nsize * 0.36, data = { data: { key: 'step ' + n, field: 'state', value: stt } };
        if (stt === 'done') {
          c.circle(cx, cy, r, Object.assign({ fill: 'subject' }, data));
          c.text(cx, ty, n, { role: 'tick', size: nsize, weight: 700, anchor: 'middle', fill: 'label-on-subject' });
        } else {
          c.circle(cx, cy, r - (stt === 'now' ? 1.5 : 0.75), Object.assign({ fill: 'surface' }, data));
          c.circle(cx, cy, r - (stt === 'now' ? 1.5 : 0.75), { stroke: stt === 'now' ? 'subject' : 'context', width: stt === 'now' ? 3 : 1.5, mark: false });
          c.text(cx, ty, n, { role: 'tick', size: nsize, weight: stt === 'now' ? 700 : 600, anchor: 'middle', fill: stt === 'now' ? 'label' : 'secondary' });
          if (stt === 'never') c.line(cx - r * 0.6, cy + r * 0.6, cx + r * 0.6, cy - r * 0.6, { stroke: 'subject', width: 2, mark: false });
        }
      };
      var sword = function (i) { var w = S[state(i)] || state(i); return hits[i] ? w + ', ' + K.fmt(hits[i][ed], 'date') : w; };
      var reached = function (i) { return i < now; };
      var bottom = 0;
      if (wide) {
        // across: a sixth of the row a step, each mark at its column's left edge with the words flush left under it, the
        // joining rule heavy as far as the bill has come. The names share a top, and every state, date and note starts on
        // one line across the row, however many lines a name takes (BC S11)
        var pitch = W / steps.length, cy = r + 2, mw = pitch - 8, col = function (i) { return pitch * i; };
        for (var i = 1; i < steps.length; i++) {
          var xa = col(i - 1) + d + 1, xb = col(i) + 1, on = reached(i);
          c.rect(xa, cy - (on ? 1 : 0.5), xb - xa, on ? 2 : 1, { fill: on ? 'subject' : 'context', mark: false });
        }
        var nlh2 = Math.round(size * 1.25), nlines = 1;
        steps.forEach(function (st) { nlines = Math.max(nlines, c.wrap(st.name, 'label', mw, 700).length); });
        var ny = cy + r + 8 + size, sy = ny + (nlines - 1) * nlh2 + c.size('label') * 0.136 + 2 + tick * 0.95;
        var dy = sy + tick * 0.136 + 1 + tick * 0.95, ny2 = dy + tick * 0.136 + 4 + note * 0.95;
        steps.forEach(function (st, i) {
          var x0 = col(i);
          mark(i, x0 + r + 1, cy);
          c.text(x0, ny, st.name, { role: 'label', weight: 700, max: mw, leading: nlh2 });
          // the state and its date each take a line, the date held whole
          c.text(x0, sy, S[state(i)] || state(i), { role: 'tick', max: mw, fill: 'label' });
          if (hits[i]) c.text(x0, dy, K.fmt(hits[i][ed], 'date').replace(/ /g, '\u00a0'), { role: 'tick', fill: 'label' });
          var bb = { bottom: dy + tick * 0.136 };
          if (st.note) bb = c.text(x0, ny2, st.note, { role: 'note', max: mw, leading: nlh, fill: 'secondary' });
          bottom = Math.max(bottom, bb.bottom);
        });
      } else {
        // down the page: marks on a rule at the left, the words beside each (the phone's arrangement, RS-S3)
        c.arrange('phone');
        var x = r + 1, tx = d + 14, mw2 = W - tx, y = 2, cys = [];
        steps.forEach(function (st, i) {
          var cy2 = y + r;
          cys.push(cy2);
          var nb = c.text(tx, cy2 - r + size * 0.95 + 4, st.name, { role: 'label', weight: 700, max: mw2 });
          var sb = c.text(tx, nb.bottom + 2 + tick * 0.95, sword(i), { role: 'tick', max: mw2, fill: 'label' });
          var bb = sb;
          if (st.note) bb = c.text(tx, sb.bottom + 4 + note * 0.95, st.note, { role: 'note', max: mw2, leading: nlh, fill: 'secondary' });
          y = Math.max(cy2 + r, bb.bottom) + 16;
        });
        for (var k = 1; k < cys.length; k++) { var on2 = reached(k); c.rect(x - (on2 ? 1 : 0.5), cys[k - 1] + r, on2 ? 2 : 1, cys[k] - cys[k - 1] - d, { fill: on2 ? 'subject' : 'context', mark: false }); }
        steps.forEach(function (st, i) { mark(i, x, cys[i]); });
        bottom = y - 16;
      }
      // the end words
      var words = law ? String(L.became || '').split('{date}').join(K.fmt(hits[last][ed], 'date'))
        : String(L.now_words || '').split('{n}').join(String(now + 1)).split('{step}').join((steps[now] || {}).name || '');
      if (words) bottom = c.text(0, bottom + 14 + size, words, { role: 'label', weight: 600, max: W }).bottom;
      c.height(bottom + 4);
    }
  });
})(globalThis.OAChart);
