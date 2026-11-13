/* Annotated illustration (coverage plan 3.16, extended; S93). A document page redrawn in vector with its own words, each
 * part marked by a numbered disc in the subject ink, and beside the page (under it on a phone) the callouts in the same
 * order: the number, the part's name in bold and what it tells a reader. The page is drawn from the rows, top to bottom,
 * as labels.layout sets it: a running head across the top, a main column and a margin column at its right, the page's
 * edge in the context ink, and a dashed rule across its foot where the drawing stops partway down the page, with words
 * that say so. Numbers sit in the page's
 * left gutter for the main column and outside its right edge for the margin. Where the margin column cannot hold
 * labels.margin_min px, the margin's parts follow the block they sit beside, set flush right. A word the page prints as a
 * dash is drawn as a rule one em wide (labels.dash_at), so no dash character prints.
 * The table lists the parts in reading order, with the words as printed.
 * encode: key (integer: the part's key; its number is its place in the sorted rows), part (text: its name), text (text: the words as printed), tells (text: what
 * it tells a reader).
 * labels: layout ([{key, slot: "head" | "main" | "margin", split (head: the separator between its pieces; the last piece
 * sets flush right), dash_at (head: the piece after which a rule one em wide joins the next), right_key (head: the part
 * whose number marks the flush-right piece), beside (margin: the key of the main block it sits beside), center (true),
 * weight, size ("label"), breaks ([words that start a new line]), lead (words set in bold at the block's start), gap (px
 * before)}]), page_max (px: the page's widest, default 400), margin_share (default 0.3), margin_min (px, default 84),
 * named (keys the title names), crop_words (the line under the dashed rule where the drawing crops the page). */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'annotated-illustration', name: 'Annotated Illustration', family: 'infographics',
    encode: { key: 'integer', part: 'text', text: 'text', tells: 'text' },
    labels: ['layout', 'page_max', 'margin_share', 'margin_min', 'named', 'crop_words'],
    phone: 'differs',
    draw: function (c) {
      var L = c.labels, W = c.width, ek = c.field('key'), ep = c.field('part'), et = c.field('text'), el = c.field('tells');
      // each part's number is its place in the rows as the spec sorts them, the order the parts sit on the page
      var by = {}, num = {}; c.rows.forEach(function (r, i) { by[String(r[ek])] = r; num[String(r[ek])] = i + 1; });
      var named = (L.named || []).map(String), tk = c.size('tick'), lh = Math.round(tk * 1.36), chip = 20, gut = chip + 8;
      var ty = function (w) { return K.typeset({ typography: c.spec.typography || { curl_quotes: true, nbsp: true } }, String(w).replace(/[ \t\n]+/g, ' ')); };
      // the page and the callouts: side by side where the callouts keep 220 px, else the callouts under the page
      var side = W >= 600, pw = side ? Math.min(L.page_max || 400, W - 240) : W, pin = 14, rx = side ? 0 : 0;
      var x0 = gut, x1 = pw - gut;   // the page's frame runs from x0 to x1; numbers sit outside it
      var inner = x1 - x0 - 2 * pin, mw = Math.round(inner * (L.margin_share || 0.3)), split = mw >= (L.margin_min || 84);
      var mainw = split ? inner - mw - 12 : inner, mx = x1 - pin - mw, tx = x0 + pin;
      var chipat = function (key, x, base) {
        var nm = named.indexOf(String(key)) >= 0, y = base - tk * 0.35;
        c.circle(x + chip / 2, y, chip / 2, { fill: 'subject', data: { key: String(key), field: 'part', value: key } });
        c.text(x + chip / 2, y + 4.4, String(num[String(key)]), { role: 'tick', weight: 700, anchor: 'middle', fill: 'label-on-subject' });
        return nm;
      };
      // the words of a block, as lines, with the lead in bold
      var block = function (b, x, y, w, anchor) {
        var r = by[String(b.key)]; if (!r) { c.warn('annotated-illustration: layout names no row ' + b.key); return y; }
        var s = ty(r[et]), pieces = [s];
        (b.breaks || []).forEach(function (br) { pieces = [].concat.apply([], pieces.map(function (p) { var i = p.indexOf(br); return i > 0 ? [p.slice(0, i).trim(), p.slice(i)] : [p]; })); });
        var role = b.size === 'label' ? 'label' : 'tick', first = null;
        pieces.forEach(function (p, i) {
          var wt = b.weight || 400, size = c.size(role), lead = b.lead && p.indexOf(b.lead) === 0;
          if (lead) { p = p.slice(b.lead.length).trim(); var lb = c.text(x, y + size * 0.93, b.lead, { role: role, weight: 700, fill: 'label', max: w, leading: Math.round(size * 1.36) }); if (first === null) first = y + size * 0.93; y = lb.bottom + 2; if (!p) return; }
          var ax = anchor === 'end' ? x + w : b.center ? x + w / 2 : x;
          var t = c.text(ax, y + size * 0.93, p, { role: role, weight: wt, max: w, leading: Math.round(size * 1.36), fill: 'label', anchor: anchor === 'end' ? 'end' : b.center ? 'middle' : 'start' });
          if (first === null) first = y + size * 0.93;
          y = t.bottom + (i < pieces.length - 1 ? 2 : 0);
        });
        b._base = first;
        return y;
      };
      var y = pin, frame_top = 0, blocks = L.layout || [], placed = {};
      blocks.forEach(function (b) {
        if (b.slot === 'margin') return;
        y += b.gap === undefined ? 10 : b.gap;
        var r = by[String(b.key)];
        if (b.slot === 'head' && r) {
          // the running head: its pieces at the left, a rule one em wide where the page prints a dash, the last flush right
          // pieces that pass the frame start a new line; the last piece takes a line of its own where it would touch
          var ps = String(r[et]).split(b.split || '; '), last = ty(ps.pop()), base = y + tk * 0.93, hx = tx, edge = x1 - pin, b0 = base;
          ps.forEach(function (p, i) {
            p = ty(p);
            var pw2 = c.measure(p, 'tick', 600);
            if (hx > tx && hx + pw2 > edge) { hx = tx; base += lh; }
            var t = c.text(hx, base, p, { role: 'tick', weight: 600, fill: 'label' });
            hx = t.x + t.w;
            if (i < ps.length - 1) {
              if (String(b.dash_at) === String(i + 1)) { c.line(hx + 2, base - tk * 0.3, hx + 2 + tk, base - tk * 0.3, { stroke: 'label', width: 1, mark: false }); hx += tk + 4; }
              else hx += 6;
            }
          });
          if (base > b0 || hx + 12 + c.measure(last, 'tick', 600) > edge) base += lh;
          c.text(edge, base, last, { role: 'tick', weight: 600, fill: 'label', anchor: 'end' });
          b._base = b0;
          if (b.right_key !== undefined) placed[String(b.right_key)] = { base: base, right: true };
          y = base + tk * 0.3;
        } else {
          y = block(b, tx, y, mainw);
        }
        placed[String(b.key)] = placed[String(b.key)] || { base: b._base, right: false };
        // margin blocks beside this one: in the margin column, or flush right under it
        var mb = blocks.filter(function (m) { return m.slot === 'margin' && String(m.beside) === String(b.key); });
        var my = (split ? b._base - tk * 0.93 : y + 4);
        mb.forEach(function (m) {
          my += m.gap === undefined ? (split ? 0 : 4) : m.gap;
          var ye = split ? block(m, mx, my, mw) : block(m, tx, my, mainw, 'end');
          placed[String(m.key)] = { base: m._base, right: true };
          my = ye + 6;
        });
        if (!split && mb.length) y = my - 6;
        if (split && mb.length) y = Math.max(y, my - 6);
      });
      var frame_bottom = y + pin + 10;
      // the page's edge, and across its foot a dashed rule where the drawing crops the page, with the words under it (DD-I6)
      c.path('M' + x0 + ',' + frame_bottom + 'V' + (frame_top + 0.5) + 'H' + x1 + 'V' + frame_bottom, { fill: 'none', stroke: 'context', width: 1, mark: false });
      c.line(x0, frame_bottom + 0.5, x1, frame_bottom + 0.5, { stroke: 'context', width: 1, dash: '4 3', mark: false });
      if (L.crop_words) frame_bottom = c.text(x0, frame_bottom + 8 + tk * 0.93, ty(L.crop_words), { role: 'tick', fill: 'secondary', max: x1 - x0, leading: lh }).bottom;
      // the numbers: the main column's in the left gutter, the margin's and the flush-right piece's outside the right edge
      Object.keys(placed).sort(function (a, b) { return num[a] - num[b]; }).forEach(function (key) {
        var p = placed[key]; if (p.base === undefined || p.base === null) return;
        chipat(key, p.right ? x1 + 6 : 0, p.base);
      });
      // the callouts
      var cx = side ? pw + 16 : 0, cw = side ? W - cx : W, cy = side ? 0 : frame_bottom + 20;
      c.rows.forEach(function (r) {
        var key = String(r[ek]), base = cy + c.size('label') * 0.93;
        chipat(key, cx, base);
        var t = c.text(cx + gut, base, ty(r[ep]), { role: 'label', weight: 700, max: cw - gut, fill: 'label' });
        var u = c.text(cx + gut, t.bottom + 1 + tk * 0.93, ty(r[el]), { role: 'tick', max: cw - gut, leading: lh, fill: 'secondary' });
        cy = u.bottom + 12;
      });
      c.height(Math.max(frame_bottom, cy - 12));
    }
  });
})(globalThis.OAChart);
