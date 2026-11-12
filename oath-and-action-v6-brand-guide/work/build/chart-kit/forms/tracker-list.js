/* Tracker list (coverage plan 3.15, core; S40). Bills in a list, drawn as chapter 11 draws a list of bills (Rules 11.1 to
 * 11.5): the bill's number and name lead each row, with a second line under them; six numbered circles run across, filled
 * as far as the bill has come, a heavy ring on the step it is at now and a fine ring on the steps ahead; a step that never
 * happened keeps its number under a slash; a bill that became law fills all six. The status words follow the marks. Where
 * the row is 552 px or wider each step takes a sixth of it with its name under its circle; narrower, the circles start on
 * the text edge and the step names move into a key after the list (Rule 11.5).
 * encode: key (the bill number), name (text), step (integer, 1 to 6: the step the bill is at now), law (text, optional: a
 * value here means the bill became law), skipped (text, optional: step numbers that never happened, such as "2"),
 * status (text: words for where it stands), date (date: the status's date).
 * labels: steps (the six step names), now ("Step {n} of 6: {step}."), detail (words after it while a bill moves, with
 * {status} and {date}), sub (the second line, with {column} placeholders), became ("Became law on {date}, Public Law {law}."), key_title (the key's head on narrow rows). */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'tracker-list',
    name: 'Tracker List',
    family: 'tables-and-plain-words',
    encode: { key: 'id', name: 'text', step: 'integer', law: 'text?', skipped: 'text?', status: 'text', date: 'date' },
    labels: ['steps', 'now', 'became', 'detail', 'sub', 'key_title'],
    phone: 'differs',
    draw: function (c) {
      var rows = c.rows, ek = c.field('key'), en = c.field('name'), es = c.field('step'), el = c.field('law', false);
      var esk = c.field('skipped', false), est = c.field('status'), ed = c.field('date');
      var W = c.width, L = c.labels, steps = L.steps || ['1', '2', '3', '4', '5', '6'];
      var wide = W >= 552, size = c.size('label'), tick = c.size('tick'), lh = Math.round(size * 1.3);
      var d = wide ? 30 : 26, r = d / 2, nsize = d >= 28 ? 14 : 13;
      var pitch = wide ? W / 6 : Math.min(60, (W - d) / 5), x0 = wide ? pitch / 2 : r;
      var fill = function (t, row, n) {
        return String(t || '').replace(/\{n\}/g, n).replace(/\{step\}/g, steps[n - 1] || '')
          .replace(/\{date\}/g, K.fmt(row[ed], 'date')).replace(/\{law\}/g, el ? (row[el] || '') : '')
          .replace(/\{status\}/g, String(row[est] || ''));
      };
      var y = 0;
      c.line(0, y, W, y, { stroke: 'gridline', width: c.t('line-hairline'), mark: false });
      rows.forEach(function (row) {
        var law = el && row[el] !== null && row[el] !== undefined && String(row[el]) !== '';
        var now = law ? 7 : row[es], skip = String(esk ? row[esk] || '' : '').split(/[ ,;]+/).filter(Boolean).map(Number);
        // the bill's number and name, then its second line
        var top = y + 16, nb = c.text(0, top + size, String(row[ek]) + ', ' + String(row[en]), { role: 'label', weight: 600, max: W });
        var yy = nb.bottom - size * 0.241;
        if (L.sub) { var sb = c.text(0, yy + tick + 6, K.parts.fill(c, L.sub, row), { role: 'tick', fill: 'secondary', max: W }); yy = sb.bottom - tick * 0.241; }
        // the six steps
        var cy = yy + 12 + r, namebot = cy + r;
        for (var i = 1; i < 6; i++) {
          var reached = i + 1 <= now;
          var xa = x0 + (i - 1) * pitch + r, xb = x0 + i * pitch - r;
          c.rect(xa, cy - (reached ? 1 : 0.5), xb - xa, reached ? 2 : 1, { fill: reached ? 'subject' : 'context', mark: false });
        }
        for (var n = 1; n <= 6; n++) {
          var cx = x0 + (n - 1) * pitch, ty = cy + nsize * 0.36;
          var data = { data: { key: row[ek] + '|' + n, field: es, value: n } };
          if (skip.indexOf(n) >= 0 && n < now) {
            c.circle(cx, cy, r - 0.75, Object.assign({ fill: 'surface' }, data));
            c.circle(cx, cy, r - 0.75, { stroke: 'context', width: 1.5, mark: false });
            c.text(cx, ty, String(n), { role: 'tick', size: nsize, weight: 600, anchor: 'middle', fill: 'secondary' });
            c.line(cx - r * 0.6, cy + r * 0.6, cx + r * 0.6, cy - r * 0.6, { stroke: 'subject', width: 2, mark: false });
          } else if (n < now) {
            c.circle(cx, cy, r, Object.assign({ fill: 'subject' }, data));
            c.text(cx, ty, String(n), { role: 'tick', size: nsize, weight: 700, anchor: 'middle', fill: 'label-on-subject' });
          } else if (n === now) {
            c.circle(cx, cy, r - 1.5, Object.assign({ fill: 'surface' }, data));
            c.circle(cx, cy, r - 1.5, { stroke: 'subject', width: 3, mark: false });
            c.text(cx, ty, String(n), { role: 'tick', size: nsize, weight: 700, anchor: 'middle', fill: 'label' });
          } else {
            c.circle(cx, cy, r - 0.75, Object.assign({ fill: 'surface' }, data));
            c.circle(cx, cy, r - 0.75, { stroke: 'context', width: 1.5, mark: false });
            c.text(cx, ty, String(n), { role: 'tick', size: nsize, weight: 600, anchor: 'middle', fill: 'secondary' });
          }
          if (wide) { var nb2 = c.text(cx, cy + r + 6 + tick, steps[n - 1], { role: 'tick', anchor: 'middle', max: pitch - 10, fill: n <= now ? 'label' : 'secondary' }); namebot = Math.max(namebot, nb2.bottom); }
        }
        // the status words
        var sy = (wide ? namebot + 8 : cy + r + 8) + size;
        var words = law ? fill(L.became, row, 6) : fill(L.now, row, now) + ' ' + fill(L.detail, row, now);
        var stb = c.text(0, sy, words, { role: 'label', max: W });
        y = stb.bottom + 14;
        c.line(0, y, W, y, { stroke: 'gridline', width: c.t('line-hairline'), mark: false });
      });
      // on narrow rows the step names move into a key after the list
      if (!wide) {
        var kw = (L.key_title ? L.key_title + ' ' : '') + steps.map(function (s, i) { return (i + 1) + ' ' + s; }).join(', ');
        var kb = c.text(0, y + 14 + tick, kw, { role: 'tick', fill: 'secondary', max: W });
        y = kb.bottom;
      }
      c.height(y + 2);
    }
  });
})(globalThis.OAChart);
