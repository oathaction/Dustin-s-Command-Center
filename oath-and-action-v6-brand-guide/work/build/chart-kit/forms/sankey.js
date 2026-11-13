/* Sankey (coverage plan 3.13, extended; S76). Money into one node and out of it: each line in at the left a band into
 * the node, each line out a band from it to the right, every band's width its dollars in one linear unit
 * (K.parts.flows), with a key band; a band under a pixel draws at 1 px. Lines on each side stack in the data's order;
 * lines a spec groups (labels.groups) sit apart by a gap under their group's name. A line of zero draws no band; the
 * table and a note keep it. The node may take in more or less than it sends where the record does not balance
 * (labels.open); the note gives the remainder.
 * Inks (the data lead's round 3 ruling (b)): the node outlined in the subject ink; flows in the light fill with the
 * context edge; the flow the title names (labels.named) in the subject ink; the lines labels.track names (cash on hand)
 * and grouped lines in the track ink with the context edge. No red: a flow is an area.
 * encode: side (category: labels.in marks a line in, any other value a line out), key (id), category (text), value.
 * labels: in (default "in"), node (the node's name), names ({key: printed name}), short ({key: name under 480 px}),
 * groups ({key: group name}), track ([keys]), named ([keys]), max_px (the node's height, default 360; 300 on a phone),
 * key_steps ([measures]), key_title, key_hairline (words under the key, {v} the measure of one pixel), open (true: the
 * node need not balance).
 * formats: value, value_phone (under 480 px), key. Maker B, round 3. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'sankey', name: 'Sankey', family: 'flow',
    encode: { side: 'category', key: 'id', category: 'text', value: 'number' },
    labels: ['in', 'node', 'names', 'short', 'groups', 'track', 'named', 'max_px', 'key_steps', 'key_title', 'key_hairline', 'open'],
    phone: 'same',
    draw: function (c) {
      var P = K.parts, L = c.labels, f = c.spec.formats || {}, W = c.width, ph = W < 480;
      var es = c.field('side'), ek = c.field('key'), ec = c.field('category'), ev = c.field('value');
      var names = L.names || {}, short = L.short || {}, groups = L.groups || {}, track = [].concat(L.track || []).map(String), named = [].concat(L.named || []).map(String);
      var lb = c.size('label'), tk = c.size('tick'), inv = String(L.in || 'in'), NODE = '\u0000node';
      var fv = function (x) { return K.fmt(x, (ph && f.value_phone) || f.value || 'integer').replace(/ (million|billion)$/, ' $1'); };
      var nm = function (r) { var k = String(r[ek]); return ph && short[k] !== undefined ? short[k] : names[k] !== undefined ? names[k] : r[ec]; };
      var rows = c.rows.filter(function (r) { return r[ev] > 0; });
      var links = rows.map(function (r) { var i = String(r[es]) === inv; return { from: i ? String(r[ek]) : NODE, to: i ? NODE : String(r[ek]), value: r[ev], key: String(r[ek]), row: r }; });
      var fl = P.flows(links, { max_px: L.max_px || (ph ? 420 : 440), open: L.open ? [NODE] : [] });
      fl.faults.forEach(function (x) { c.warn(x); });
      var y = 0;
      if (L.key_steps) {
        y += P.width_key(c, 0, y, fl.unit, L.key_steps, { words: L.key_steps.map(function (s) { return '$' + K.fmt(s, f.key || f.value || 'integer'); }), stroke: 'context', len: 32, title: L.key_title, max: W });
        if (L.key_hairline) y = c.text(0, y + tk * 0.9, String(L.key_hairline).split('{v}').join('$' + K.fmt(1 / fl.unit, f.key || f.value || 'integer')), { role: 'tick', max: W }).bottom;
        y += 16;
      }
      // the node's name over the node, centered, then the two sides under it
      var vmax = 0;
      rows.forEach(function (r) { vmax = Math.max(vmax, c.measure('$' + fv(r[ev]), 'tick', 700, true)); });
      var cw = Math.max(Math.round(W * (ph ? 0.37 : 0.27)), Math.ceil(vmax) + 10), bw = Math.round(W * 0.5 - cw - 7), nx = cw + bw, nw = 14;
      var nb = c.text(W / 2, y + lb * 0.95, L.node || '', { role: 'label', weight: 700, anchor: 'middle', max: W });
      var top = Math.ceil(nb.bottom) + 10;
      // one side's items: slots as tall as their band or their words, a gap before each group
      var side = function (isin) {
        var ls = fl.links.filter(function (l) { return (l.to === NODE) === isin; }), yy = top, last = null, out = [];
        ls.forEach(function (l) {
          var g = groups[l.key] || null, w = Math.max(1, l.w), r = l.row.row || l.row;
          if (g !== last && (g || last)) yy += 12;
          var gh = 0;
          if (g && g !== last) gh = Math.ceil(c.wrap(g, 'tick', cw - 8, 700).length * Math.round(tk * 1.25)) + 4;
          var words = [nm(r), '$' + fv(l.value)];
          var th = Math.ceil(c.wrap(words[0], 'label', cw - 8, 400).length * lb * 1.25 + tk * 1.25) + 2;
          out.push({ l: l, r: r, g: g !== last ? g : null, gy: yy, y: yy + gh, h: Math.max(w, th), w: w, words: words });
          yy += gh + Math.max(w, th) + 8;
          last = g;
        });
        return { items: out, bottom: yy - 8 };
      };
      var L_ = side(true), R_ = side(false);
      var ins = L_.items.reduce(function (s, it) { return s + it.w; }, 0), outs = R_.items.reduce(function (s, it) { return s + it.w; }, 0);
      var nh = Math.max(ins, outs), ny = top + Math.max(0, (Math.max(L_.bottom, R_.bottom) - top - nh) / 2);
      ny = Math.min(ny, top + (ph ? 120 : 80));
      var ink = function (k) { return named.indexOf(k) >= 0 ? 'subject' : track.indexOf(k) >= 0 || groups[k] ? 'track' : 'light-fill'; };
      // bands first, then the node over their ends, then the words
      [[L_, true], [R_, false]].forEach(function (sd) {
        var at = ny;
        sd[0].items.forEach(function (it) {
          var by = it.y + (it.h - it.w) / 2, fill = ink(it.l.key), sub = fill === 'subject';
          // a band too thin to show its two edges apart takes the context ink whole, which reads at 3 to 1 alone
          if (!sub && it.w < 3) { fill = 'context'; sub = true; }
          var data = { key: it.l.key, from: it.l.from === NODE ? 'node' : it.l.from, to: it.l.to === NODE ? 'node' : it.l.to, value: it.l.value };
          if (sd[1]) P.flow_band(c, cw, by, nx, at, it.w, { fill: fill, edge: sub ? false : 'context', data: data });
          else P.flow_band(c, nx + nw, at, W - cw, by, it.w, { fill: fill, edge: sub ? false : 'context', data: data });
          at += it.w;
          it.by = by;
        });
      });
      c.rect(nx, ny, nw, nh, { fill: 'surface', kind: 'node', data: { key: 'node', field: ev, value: Math.max(fl.nodes[NODE].in, fl.nodes[NODE].out) } });
      c.rect(nx + 0.75, ny + 0.75, nw - 1.5, nh - 1.5, { stroke: 'subject', width: 1.5, mark: false });
      var bottom = ny + nh;
      [[L_, true], [R_, false]].forEach(function (sd) {
        sd[0].items.forEach(function (it) {
          var x = sd[1] ? cw - 8 : W - cw + 8, an = sd[1] ? 'end' : 'start', wt = named.indexOf(it.l.key) >= 0 ? 700 : 400;
          if (it.g) c.text(sd[1] ? cw - 8 : W - cw + 8, it.gy + tk * 0.9, it.g, { role: 'tick', weight: 700, anchor: an, max: cw - 8, fill: 'label' });
          var ty = it.y + Math.max(0, (it.h - (it.h > it.w ? it.h : it.w)) / 2) + lb * 0.86;
          var t1 = c.text(x, ty, it.words[0], { role: 'label', weight: wt, anchor: an, max: cw - 8 });
          var t2 = c.text(x, t1.bottom + tk * 0.9, it.words[1], { role: 'tick', weight: wt, anchor: an, tnum: true, fill: 'label' });
          bottom = Math.max(bottom, t2.bottom, it.y + it.h);
        });
      });
      c.height(bottom + 2);
    }
  });
})(globalThis.OAChart);
