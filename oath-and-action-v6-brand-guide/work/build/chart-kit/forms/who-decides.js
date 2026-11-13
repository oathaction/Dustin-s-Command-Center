/* Who-decides diagram (coverage plan 3.11, core; S68; chapter 15 shares it). The bodies behind a decision, placed by
 * what they can do: a band of those who can change the rules above a band of those who apply them, in columns by level
 * (federal, regional, state, local, private). One node style for every body, a subject-ink edge with the text's ink
 * inside, the name in bold and any words in parentheses under it. Lines of authority (one body setting or approving
 * another's rules) run in the context ink and end in Rule 15.5's open diamond; they take no sign and close no loop (R3-6).
 * Each column takes the width its names need (A-S5): every column starts at 118 px and the width left over goes, a few
 * pixels at a time, to the column whose widening shortens the bands most, so a long name stops wrapping to five lines
 * beside an empty column; what no column can use is shared evenly. Narrower than five columns of 118 px, the bands run
 * down the page, each body a row under its level's name, and the lines of authority run in a lane at the left.
 * encode: who (text), level (category), changes (boolean: can change the rules), key (the body's own key, for links).
 * labels: levels ([values], the columns' order), level_words ({value: words}), bands ({true: words, false: words}),
 * authority ([{from: key, to: key}]), order ([keys]: the order bodies stack in a column; a body whose line leaves for
 * another column sits last, so its line leaves into the gap under the band). */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'who-decides', name: 'Who-Decides Diagram', family: 'structure',
    encode: { who: 'text', level: 'category', changes: 'boolean', key: 'integer' },
    labels: ['levels', 'level_words', 'bands', 'authority', 'order'],
    phone: 'differs',
    draw: function (c) {
      var L = c.labels, W = c.width, ew = c.field('who'), el = c.field('level'), ec = c.field('changes'), ek = c.field('key');
      var levels = L.levels || [], lw = L.level_words || {}, bands = L.bands || {}, cg = 12, pad = [8, 8], role = ['label'];
      var cw = (W - cg * (levels.length - 1)) / levels.length, wide = cw >= 118, size = c.size('label'), tick = c.size('tick');
      var split = function (r) { var s = String(r[ew]).replace(/[ \t\n]+/g, ' '), i; s = K.typeset({ typography: c.spec.typography || { curl_quotes: true, nbsp: true } }, s); i = s.indexOf(' ('); return i > 0 ? [s.slice(0, i), s.slice(i + 1)] : [s, null]; };
      var col = function (r) { return Math.max(0, levels.indexOf(String(r[el]))); };
      var ord = (L.order || []).map(String), rank = function (r) { var i = ord.indexOf(String(r[ek])); return i < 0 ? ord.length + r[ek] : i; };
      var band = function (v) { return c.rows.filter(function (r) { return !!r[ec] === v; }).sort(function (a, b) { return col(a) - col(b) || rank(a) - rank(b); }); };
      var at = {}, y = 0;
      var node = function (r, x, top, w, h, eyebrow) {
        var nm = split(r), words = nm[0];
        var nb = K.parts.node(c, { x: x, y: top, w: w, h: h }, words, { stroke: 'subject', align: 'start', lines: 8, pad: pad, sub: nm[1] || undefined, sub_lines: 4, weight: 600, roles: role, data: { key: String(r[ek]), field: 'who', value: r[ew] } });
        at[String(r[ek])] = { x: x, y: top, w: w, h: h };
        if (!nb) c.warn('who-decides: the words of ' + words + ' do not fit their box at ' + W + ' px');
        return nb;
      };
      var memo = {};
      var size_of = function (r, w) {
        var k = role[0] + '|' + r[ek] + '|' + w;
        if (!(k in memo)) { var nm = split(r); memo[k] = K.parts.node_size(c, nm[0], { max: w, min: w, lines: 8, pad: pad, sub: nm[1] || undefined, sub_lines: 4, weight: 600, roles: role }); }
        return memo[k];
      };
      // each column's width (A-S5): 118 px each, then the rest a step at a time to the column that shortens the bands most
      var ws = levels.map(function () { return cw; });
      var band_h = function (v, w2) {
        var hs = levels.map(function () { return 0; }), ns = levels.map(function () { return 0; });
        c.rows.forEach(function (r) { if (!!r[ec] !== v) return; var i = col(r), s = size_of(r, w2[i]); hs[i] += (s ? s.h : 999) + (ns[i]++ ? 22 : 0); });
        return Math.max.apply(null, hs);
      };
      var cost = function (w2) { return band_h(true, w2) + band_h(false, w2); };
      var share = function () {
        var avail = W - cg * (levels.length - 1), base = 118, step = 4;
        ws = levels.map(function () { return base; });
        var left = avail - base * levels.length, now = cost(ws);
        while (left >= step) {
          var best = -1, bd = 0, bgain = 0;
          levels.forEach(function (v, i) {
            // the least widening of this column, up to what is left, that shortens the bands
            for (var d = step; d <= left; d += step) {
              var w2 = ws.slice(); w2[i] += d;
              var g = now - cost(w2);
              if (g > 0) { if (best < 0 || g / d > bgain / bd) { best = i; bd = d; bgain = g; } break; }
            }
          });
          if (best < 0) break;
          ws[best] += bd; left -= bd; now -= bgain;
        }
        ws = ws.map(function (w) { return Math.floor((w + left / levels.length) * 100) / 100; });
      };
      // one size for every name: the label size where every name fits its column, else the tick size
      var fits = function () { return c.rows.every(function (r) { return !!size_of(r, ws[col(r)]); }); };
      if (wide) { share(); if (!fits()) { role = ['tick']; share(); if (!fits()) wide = false; } }
      var heading = function (x, yb, words, max) { return c.text(x, yb, words, { role: 'label', weight: 700, max: max }); };
      if (wide) {
        // column heads, then each band under its heading, set in the first column's width so a line of authority clears it
        var cx = function (i) { var x = 0; for (var j = 0; j < i; j++) x += ws[j] + cg; return x; };
        var hb = 0;
        levels.forEach(function (v, i) { hb = Math.max(hb, c.text(cx(i), tick * 0.95, lw[v] || v, { role: 'tick', weight: 600, fill: 'secondary', max: ws[i] }).bottom); });
        y = hb + 14;
        [true, false].forEach(function (v, bi) {
          var rows = band(v);
          if (!rows.length) return;
          var hd = heading(0, y + size * 0.93, bands[String(v)] || String(v), bi ? ws[0] : W);
          var top = hd.bottom + 10, stack = levels.map(function () { return top; });
          rows.forEach(function (r) {
            var i = col(r), s = size_of(r, ws[i]), h = s ? s.h : 60;
            node(r, cx(i), stack[i], ws[i], h);
            stack[i] += h + 22;
          });
          y = Math.max.apply(null, stack) - 22 + (bi ? 0 : 28);
        });
      } else {
        c.arrange('phone');
        var lane = (L.authority || []).length, ind = lane ? 10 + 9 * lane : 0, nw = W - ind;
        [true, false].forEach(function (v, bi) {
          var rows = band(v);
          if (!rows.length) return;
          if (bi) y += 16;
          var hd = heading(ind, y + size * 0.93, bands[String(v)] || String(v), nw);
          y = hd.bottom + 8;
          var last = null;
          rows.forEach(function (r) {
            // the level once over each run of bodies at that level
            var lv = String(r[el]), top = y;
            if (lv !== last) top = c.text(ind, y + tick * 0.95, lw[lv] || lv, { role: 'tick', weight: 600, fill: 'secondary', max: nw }).bottom + 3;
            last = lv;
            var s = size_of(r, nw), h = s ? s.h : 60;
            node(r, ind, top, nw, h);
            y = top + h + 12;
          });
        });
        y -= 12;
      }
      // lines of authority: drawn before nothing else crosses them; across, down from the body to the one it governs;
      // on a phone, out to a lane at the left and back in
      // lines of authority: across, down from the body that decides to the one it governs; on a phone, out to a lane at the
      // left and back in; each ends in Rule 15.5's open diamond (the kit's link, A-E4), with no sign
      (L.authority || []).forEach(function (a, i) {
        var f = at[String(a.from)], t = at[String(a.to)];
        if (!f || !t) { c.warn('labels.authority: no body with key ' + (f ? a.to : a.from)); return; }
        var o = { stroke: 'context', width: 1.5 }, od = { stroke: 'context', width: 1.5, arrow: 'diamond', data: { key: 'authority ' + a.from + '>' + a.to, from: String(a.from), to: String(a.to), value: 'authority' } };
        if (wide) {
          var fx = f.x + f.w / 2, tx = t.x + t.w / 2;
          if (Math.abs(fx - tx) < 1) K.parts.link(c, { x: fx, y: f.y + f.h }, { x: tx, y: t.y }, od);
          else {
            var bend = f.y + f.h + 12;
            K.parts.link(c, { x: fx, y: f.y + f.h }, { x: fx, y: bend }, o);
            K.parts.link(c, { x: fx, y: bend }, { x: tx, y: bend }, o);
            K.parts.link(c, { x: tx, y: bend }, { x: tx, y: t.y }, od);
          }
        } else {
          var lx = 4 + 9 * i, fy = f.y + Math.min(20, f.h / 2), ty = t.y + Math.min(20, t.h / 2);
          K.parts.link(c, { x: f.x, y: fy }, { x: lx, y: fy }, o);
          K.parts.link(c, { x: lx, y: fy }, { x: lx, y: ty }, o);
          K.parts.link(c, { x: lx, y: ty }, { x: t.x, y: ty }, od);
        }
      });
      c.height(y + 1);
    }
  });
})(globalThis.OAChart);
