/* Calendar (coverage plan 3.16, extended; S94). Dates that matter in one year: a year mark, twelve months in order with
 * each event its own square on its day (a picture, hidden from screen readers, since the list says every date), then the
 * dates as live HTML text (R4-3), one a row in date order, each with its day and weekday, what falls due, who acts and
 * the kind of date in words, with the consequence where the law states one; the table gives each date's section. An event the law attaches a consequence to takes a filled square in the
 * subject ink and, in the list and the key, its kind in words after a filled square (oac-h-sq-strong); any other takes
 * an open square edged in the subject ink and its words after an open square (oac-h-sq) (ruling (b); DD-I17). A day with several events stacks their squares.
 * encode: date (date), event (text), who (text, optional), consequence (text), weekday (text, optional).
 * labels: key (the line over the year mark that says what its squares mean), none (words a consequence opens with when the law states none, such as "None"), tags ({strong, plain}: the
 * kinds in words), months (twelve month names for the mark), consequence_words (the words a consequence prints in,
 * {consequence} for the column's words), who_words (default "for {who}"), mark_width (px, default 256). */
(function (K) {
  'use strict';
  var DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
  K.register_chart({
    form: 'calendar', name: 'Calendar', family: 'infographics',
    encode: { date: 'date', event: 'text', who: 'text?', consequence: 'text', weekday: 'text?' },
    labels: ['none', 'tags', 'months', 'consequence_words', 'who_words', 'mark_width', 'key'],
    phone: 'same',
    html: function (h) {
      var L = h.labels, ed = h.field('date'), ee = h.field('event'), ec = h.field('consequence');
      var f = function (n) { return h.encode[n] || null; }, eo = f('who'), ewd = f('weekday');
      var none = String(L.none || 'None'), tags = L.tags || {}, months = L.months || [];
      var strong = function (r) { return String(r[ec] || '').indexOf(none) !== 0; };
      var ymd = function (r) { var m = String(r[ed]).match(/^(\d{4})-(\d{2})-(\d{2})/); return m ? [+m[1], +m[2], +m[3]] : null; };
      var year = (ymd(h.rows[0]) || [2000])[0], leap = (year % 4 === 0 && year % 100 !== 0) || year % 400 === 0;
      var byday = {}; h.rows.forEach(function (r, i) { var e = ymd(r); if (e) (byday[e[1] + '-' + e[2]] = byday[e[1] + '-' + e[2]] || []).push(i); });
      var W = L.mark_width || 256, rowh = 26, lab = 34, pitch = (W - lab - 4) / 31, sq = Math.min(8, Math.floor(pitch)), top = 20;
      // the year mark: a month a row, a hairline for its days, each event a square on its day, stacked where a day holds several;
      // CD-S1 (fix pass after rounds 4 and 5): the days on a 1 to 31 scale, labeled once at the top at days 1, 15 and 31,
      // and each month's hairline ticked at its 1st, its 15th and its last day
      var mark = h.mark(W, top + 12 * rowh, function (c) {
        var dx = function (day) { return lab + (day - 1) * pitch + sq / 2; };
        c.text(dx(1), 13, '1', { role: 'tick', fill: 'secondary', anchor: 'middle' });
        c.text(dx(15), 13, '15', { role: 'tick', fill: 'secondary', anchor: 'middle' });
        c.text(lab + 30 * pitch + sq, 13, '31', { role: 'tick', fill: 'secondary', anchor: 'end' });
        // the twelve names in one text, a line each, and every month's hairline and ticks in one path
        c.text(0, top + rowh / 2 + 4.5, months.join(' '), { role: 'tick', fill: 'secondary', max: 1, leading: rowh });
        var d = '', tk = '';
        for (var m = 0; m < 12; m++) {
          var md = DAYS[m] + (m === 1 && leap ? 1 : 0), yl = top + m * rowh + rowh / 2;
          d += 'M' + lab + ',' + (yl + 0.5) + 'h' + K.round((md - 1) * pitch + sq);
          [1, 15, md].forEach(function (day) { tk += 'M' + (Math.round(dx(day) - 0.5) + 0.5) + ',' + (yl - 3) + 'v7'; });
        }
        c.path(d, { fill: 'none', stroke: 'gridline', width: 1, mark: false });
        c.path(tk, { fill: 'none', stroke: 'gridline', width: 1, mark: false });
        // the squares, filled ones in one path and open ones in another, each square a closed run of four sides
        var stack = {}, sq_f = [], sq_o = [], R = K.round;
        h.rows.forEach(function (r) {
          var e = ymd(r); if (!e || e[0] !== year) return;
          var key = e[1] + '-' + e[2], k = stack[key] = (stack[key] || 0) + 1, n = (byday[key] || []).length;
          var x = lab + (e[2] - 1) * pitch, y0 = top + (e[1] - 1) * rowh + rowh / 2 - (n * sq + (n - 1) * 2) / 2 + (k - 1) * (sq + 2);
          if (strong(r)) sq_f.push([x, y0, sq]); else sq_o.push([x + 0.75, y0 + 0.75, sq - 1.5]);
        });
        var run = function (q) { return q.map(function (b) { return 'M' + R(b[0]) + ',' + R(b[1]) + 'h' + b[2] + 'v' + b[2] + 'h-' + b[2] + 'z'; }).join(''); };
        var pts = function (q) { return q.map(function (b) { return [[b[0], b[1]], [b[0] + b[2], b[1]], [b[0] + b[2], b[1] + b[2]], [b[0], b[1] + b[2]]]; }); };
        var box = function (q) { var x0 = Math.min.apply(null, q.map(function (b) { return b[0]; })), y0 = Math.min.apply(null, q.map(function (b) { return b[1]; })); return [x0, y0, Math.max.apply(null, q.map(function (b) { return b[0] + b[2]; })) - x0, Math.max.apply(null, q.map(function (b) { return b[1] + b[2]; })) - y0]; };
        if (sq_f.length) c.path(run(sq_f), { fill: 'subject', pts: pts(sq_f), closed: true }, box(sq_f));
        if (sq_o.length) c.path(run(sq_o), { fill: 'surface', stroke: 'subject', width: 1.5, pts: pts(sq_o), closed: true }, box(sq_o));
      });
      // the list: one item a day, each event on it with its kind in words; who acts where the event's words do not name it
      var days = [];
      h.rows.forEach(function (r, i) { var e = ymd(r), key = e ? e[1] + '-' + e[2] : String(i); if (!byday[key + '#']) { byday[key + '#'] = true; days.push(key); } });
      var items = days.map(function (key) {
        var evs = byday[key], r0 = h.rows[evs[0]];
        var when = (ewd && r0[ewd] ? r0[ewd] + ', ' : '') + h.fmt(r0[ed], 'date').replace(/, \d{4}$/, '');
        return '<li class="oac-h-item"' + h.row(evs) + '><p class="oac-h-name"><time datetime="' + h.esc(String(r0[ed]).slice(0, 10)) + '">' + h.words(when) + '</time></p>' +
          evs.map(function (i) {
            // who acts, unless the event's words name it already (its first word, less a plural s)
            var r = h.rows[i], s = strong(r), who = eo && r[eo] ? String(r[eo]) : '', named = who && String(r[ee]).indexOf(who.replace(/^The /, '').split(' ')[0].replace(/s$/, '')) >= 0;
            var cons = s ? String(L.consequence_words || '{consequence}').split('{consequence}').join(r[ec]) : '';
            return '<p class="oac-h-body">' + h.words(r[ee]) + (who && !named ? ' ' + h.words(String(L.who_words || 'for {who}').split('{who}').join(who.charAt(0).toLowerCase() + who.slice(1))) : '') + '</p><p class="oac-h-small"><span class="' +
              (s ? 'oac-h-sq-strong' : 'oac-h-sq') + '">' + h.words(s ? tags.strong || '' : tags.plain || '') + '</span></p>' + (cons ? '<p class="oac-h-small">' + h.words(cons) + '</p>' : '');
          }).join('') + '</li>';
      });
      // the key: a line on the squares, then the two kinds after the squares the list uses (DD-I17)
      // CR-S14 and CD-S1 (fix pass after rounds 4 and 5): each kind on a line of its own, so no entry parts from its square
      // and the two never run together at a desk
      return (L.key ? '<p class="oac-h-small">' + h.words(L.key) + '</p>' : '') +
        '<p class="oac-h-small"><span class="oac-h-sq-strong">' + h.words(tags.strong || '') + '</span></p><p class="oac-h-small"><span class="oac-h-sq">' + h.words(tags.plain || '') + '</span></p>' + mark + '<ol class="oac-h-dates" role="list">' + items.join('') + '</ol>';
    }
  });
})(globalThis.OAChart);
