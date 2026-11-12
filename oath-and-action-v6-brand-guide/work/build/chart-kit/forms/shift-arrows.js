/* Shift arrows (coverage plan 3.2, core; S11). One arrow per row from its earlier value (the dot) to its later value (the
 * tip), on one scale with a labeled center; the nation's row set apart above the states (DR-64); party direction in words and
 * position, neutral inks (DR-48, DR-58). On a phone each row becomes a lollipop of the shift's size from zero (DR-64).
 * encode: key (code), label (text), from (number), to (number), shift (number), scope (category, optional; the value in
 * labels.apart_value is set apart above the rest). labels: left, right (the two sides' words), center ("Even"), apart_value,
 * tag (words for a row whose sign changed), domain ([lo, hi]), skip ([a, b]: an axis break that skips a to b), phone_value
 * (words with {to} and {lead}), lead ({neg, pos}: the leader's name by sign). formats: value, shift. */
(function (K) {
  'use strict';
  function arrow(c, x1, x2, y, o) {
    var hl = c.t(c.phone ? 'arrow-phone-head-length' : 'arrow-head-length'), hw = c.t(c.phone ? 'arrow-phone-head-half-width' : 'arrow-head-half-width');
    var dir = x2 >= x1 ? 1 : -1, len = Math.abs(x2 - x1);
    // an arrow shorter than its head draws the head alone, never a tail dot under it, which reads as a diamond (brand KS4)
    if (len < hl + 2) { c.polygon([[x2, y], [x2 - dir * hl, y - hw], [x2 - dir * hl, y + hw]], { fill: 'subject', kind: 'arrow', data: o.data }); return; }
    c.circle(x1, y, c.t('arrow-tail-radius'), { fill: 'subject', mark: false });
    if (len > hl) c.line(x1, y, x2 - dir * hl, y, { stroke: 'subject', width: c.t('arrow-shaft'), mark: false });
    var b = x2 - dir * Math.min(hl, Math.max(len, hl * 0.6));
    c.polygon([[x2, y], [b, y - hw], [b, y + hw]], { fill: 'subject', kind: 'arrow', data: o.data });
  }
  K.parts.arrow = arrow;
  K.register_chart({
    form: 'shift-arrows', name: 'Shift Arrows', family: 'shift-and-swing',
    encode: { key: 'code', label: 'text', from: 'number', to: 'number', shift: 'number', scope: 'category?' },
    labels: ['left', 'right', 'center', 'apart_value', 'tag', 'domain', 'skip', 'phone_value', 'lead', 'axis_unit', 'how', 'side_note'],
    phone: 'differs',
    draw: function (c) {
      var rows = c.rows, ek = c.field('key'), el = c.field('label'), ef = c.field('from'), et = c.field('to'), esh = c.field('shift'), esc = c.field('scope', false);
      var L = c.labels, f = c.spec.formats || {}, W = c.width, size = c.size('label');
      var apart = rows.filter(function (r) { return esc && String(r[esc]) === String(L.apart_value); });
      var rest = rows.filter(function (r) { return apart.indexOf(r) < 0; });
      var tagged = function (r) { return L.tag && (r[ef] < 0) !== (r[et] < 0); };
      if (c.phone) {
        var all = apart.concat(rest.slice().sort(function (a, b) { return Math.abs(b[esh]) - Math.abs(a[esh]); }));
        var mx = Math.max.apply(null, all.map(function (r) { return Math.abs(r[esh]); }));
        var nk = K.nice(0, mx, 2), xs = K.scale.linear([0, nk[1]], [0, W * 0.62]), y = size;
        K.ticks(0, nk[1], 2).forEach(function (t) { c.text(xs(t), y, K.fmt(t, 'integer'), { role: 'tick', anchor: t ? 'middle' : 'start' }); });
        y += 22;
        all.forEach(function (r, i) {
          if (i === apart.length && apart.length) { c.line(0, y - 8, W, y - 8, { stroke: 'gridline', width: c.t('line-hairline'), mark: false }); y += 6; }
          var nb = c.text(0, y + size * 0.8, r[el], { role: 'label', weight: 700 }), extra = 0;
          if (L.phone_value) {
            var lead = (L.lead || {})[r[et] < 0 ? 'neg' : 'pos'] || '';
            var pv = String(L.phone_value).replace('{lead}', lead).replace('{to}', K.fmt(Math.abs(r[et]), f.value || 'signed:1').replace(/^[+−]/, '+'));
            // the value moves under the name when the two would touch on one line (D3-93)
            if (nb.w + c.measure(pv, 'tick') + 12 > W) { extra = 18; c.text(0, y + size * 0.8 + extra, pv, { role: 'tick' }); }
            else c.text(W, y + size * 0.8, pv, { role: 'tick', anchor: 'end' });
          }
          y += extra;
          var ly = y + size + 12, xe = xs(Math.abs(r[esh]));
          c.line(0, ly, xe, ly, { stroke: 'subject', width: c.t('arrow-shaft'), mark: false });
          c.circle(xe, ly, c.t('dot-vertex-radius'), { fill: 'subject', data: { key: r[ek], field: esh, value: r[esh] } });
          var vb = c.text(xe + 8, ly + size * 0.35, K.fmt(Math.abs(r[esh]), f.shift || 'number:1'), { role: 'label' });
          if (tagged(r)) { var tw = c.measure(L.tag, 'tick', 600) + 10; c.rect(vb.x + vb.w + 10, ly - 9, tw, 18, { fill: 'surface', mark: false }); c.rect(vb.x + vb.w + 10.5, ly - 8.5, tw - 1, 17, { stroke: 'label', mark: false }); c.text(vb.x + vb.w + 15, ly + 4.5, L.tag, { role: 'tick', weight: 600 }); }
          y += c.t('shift-axis-phone-lollipop-pitch');
        });
        c.height(y);
        return;
      }
      // desktop: a signed axis, optionally skipping a stretch so one far value fits
      var dlo = Math.min.apply(null, rows.map(function (r) { return Math.min(r[ef], r[et]); })), dhi = Math.max.apply(null, rows.map(function (r) { return Math.max(r[ef], r[et]); }));
      // the axis runs to the tick past the farthest value, so no arrow runs off the scale (CD KS5)
      var dom = L.domain ? L.domain.slice() : [dlo, dhi];
      dom = [Math.min(dom[0], Math.floor(dlo / 10) * 10), Math.max(dom[1], Math.ceil(dhi / 10) * 10)];
      var skip = L.skip, gap = c.t('shift-axis-break-gap');
      var span = (dom[1] - dom[0]) - (skip ? (skip[1] - skip[0]) : 0);
      var x0 = 8, x1 = W - 8, unit = (x1 - x0 - (skip ? gap : 0)) / span;
      var xs2 = function (v) {
        if (!skip || v >= skip[1]) return x1 - (dom[1] - v) * unit;
        if (v <= skip[0]) return x0 + (v - dom[0]) * unit;
        return x0 + (skip[0] - dom[0]) * unit + gap / 2;
      };
      // the scale narrows until every label on the right side of its arrow fits the drawing, so no label flips to the
      // left for want of room (CD KR3); a few passes, as each narrowing moves the arrows
      for (var pass = 0; pass < 4; pass++) {
        var over = 0;
        rows.forEach(function (r) {
          if (r[et] < 0) return;
          var lab = K.fmt(Math.abs(r[esh]), f.shift || 'number:1') + ' ' + r[el];
          over = Math.max(over, Math.max(xs2(r[ef]), xs2(r[et])) + 8 + c.measure(lab, 'label', 600) - W);
        });
        if (over <= 0.5) break;
        x1 -= over + 1;
        unit = (x1 - x0 - (skip ? gap : 0)) / span;
      }
      var ty = c.size('tick');
      c.text(x0, ty, L.left || '', { role: 'tick', weight: 600 });
      c.text(x1, ty, L.right || '', { role: 'tick', weight: 600, anchor: 'end' });
      var ticks = K.ticks(dom[0], dom[1], 0, 10).filter(function (t) { return !skip || t <= skip[0] || t >= skip[1]; });
      var tyy = ty + 22;
      ticks.forEach(function (t) {
        var w = t === 0 ? (L.center || '0') : K.fmt(Math.abs(t), 'integer');
        // a tick word at an edge sets flush with that edge rather than dropping (CD KR3)
        var tw = c.measure(w, 'tick'), xx = xs2(t), an = xx + tw / 2 > W ? 'end' : xx - tw / 2 < 0 ? 'start' : 'middle';
        c.text(an === 'end' ? W : an === 'start' ? 0 : xx, tyy, w, { role: 'tick', anchor: an });
      });
      if (skip) { var sx = x0 + (skip[0] - dom[0]) * unit + gap / 2; c.text(sx, tyy, '//', { role: 'tick', anchor: 'middle', weight: 700 }); }
      var pitch = c.t('shift-axis-pitch'), y = tyy + 22;
      var row = function (r, yy) {
        var a = xs2(r[ef]), b = xs2(r[et]);
        arrow(c, a, b, yy, { data: { key: r[ek], field: esh, value: r[esh] } });
        c.datum(a, yy, { data: { key: r[ek], field: ef, value: r[ef] } });
        var right = r[et] >= 0, val = K.fmt(Math.abs(r[esh]), f.shift || 'number:1');
        var tx = right ? Math.max(a, b) + 8 : Math.min(a, b) - 8;
        var lab = right ? val + ' ' + r[el] : r[el] + ' ' + val;
        var lw = c.measure(lab, 'label', 600);
        if (right && tx + lw > W) { tx = Math.min(a, b) - 8; right = false; lab = r[el] + ' ' + val; }
        if (!right && tx - lw < 0) { tx = Math.max(a, b) + 8; right = true; lab = val + ' ' + r[el]; }
        var t = c.text(tx, yy + size * 0.35, lab, { role: 'label', weight: 600, anchor: right ? 'start' : 'end' });
        if (tagged(r)) {
          var tw = c.measure(L.tag, 'tick', 600) + 10, tx2 = right ? t.x + t.w + 10 : t.x - 10 - tw;
          c.rect(tx2 + 0.5, yy - 8.5, tw - 1, 17, { stroke: 'label', mark: false });
          c.text(tx2 + 5, yy + 4.5, L.tag, { role: 'tick', weight: 600 });
        }
      };
      apart.forEach(function (r) { row(r, y); y += pitch; });
      if (apart.length) { c.line(0, y - 6, W, y - 6, { stroke: 'gridline', width: c.t('line-hairline'), mark: false }); y += 10; }
      var ztop = y - 12, firstRow = y, rowY = {};
      rest.forEach(function (r) { rowY[r[ek]] = y; row(r, y); y += pitch; });
      // the reading aid in the empty upper right (E19): a sample arrow at the chart's own scale, its years and its words
      var hw = L.how;
      if (hw) {
        var hx = xs2(0) + 22, hwid = W - hx - 8, hy = firstRow;
        // the block starts at the first row from which its whole box is clear of the rows' labels (D3-93)
        var bh = (hw.title ? c.size('tick') + 14 : 0) + (hw.sample ? 46 : 0);
        [].concat(hw.text || []).forEach(function (t) { bh += K.wrap(t, c.size('tick'), hwid, 400).length * Math.round(c.size('tick') * 1.25) + 8; });
        var hit = function (yy) { return c.texts.some(function (t) { return t.x + t.w > hx - 4 && t.x < W && t.y + t.h > yy - 4 && t.y < yy + bh + 4; }); };
        while (hit(hy) && hy < y) hy += pitch;
        if (hw.title) { c.text(hx, hy + c.size('tick'), hw.title, { role: 'eyebrow', weight: 700, fill: 'secondary' }); hy += c.size('tick') + 14; }
        if (hw.sample) {
          var sp = hw.sample, a0 = hx + 4, a1 = hx + 4 + (xs2(sp.to) - xs2(sp.from));
          arrow(c, a0, a1, hy + 8, { data: {} });
          c.marks = c.marks.filter(function (m) { return m.kind !== 'arrow' || (m.data && m.data.key); });
          if (sp.value) c.text(a1 + 8, hy + 8 + c.size('label') * 0.35, sp.value, { role: 'label' });
          if (sp.from_label) c.text(a0, hy + 30, sp.from_label, { role: 'tick' });
          // the later year sits centered under the tip, moved right where it would touch the earlier one
          if (sp.to_label) {
            var fw = sp.from_label ? c.measure(sp.from_label, 'tick') : 0, tw2 = c.measure(sp.to_label, 'tick');
            c.text(Math.max(a1, a0 + fw + 8 + tw2 / 2), hy + 30, sp.to_label, { role: 'tick', anchor: 'middle' });
          }
          hy += 46;
        }
        [].concat(hw.text || []).forEach(function (t) { var b = c.text(hx, hy + c.size('tick'), t, { role: 'tick', max: hwid }); hy = b.y + b.h + 8; });
      }
      // a side note left of the center line, beside the row it names (E19)
      var sn = L.side_note;
      if (sn && rowY[sn.near] !== undefined) {
        var sx1 = xs2(0) - 24, swid = Math.min(260, sx1 - 8), sx0 = sx1 - swid, sy = rowY[sn.near] + c.size('tick') * 0.35;
        if (sn.title) { var st = c.text(sx0, sy, sn.title, { role: 'tick', weight: 700, max: swid }); sy = st.y + st.h + 4 + c.size('tick') * 0.77; }
        [].concat(sn.text || []).forEach(function (t) { var b = c.text(sx0, sy, t, { role: 'tick', fill: 'secondary', max: swid }); sy = b.y + b.h + 6 + c.size('tick') * 0.77; });
      }
      c.line(xs2(0), ztop, xs2(0), y - pitch + 10, { stroke: 'baseline', width: c.t('line-baseline'), mark: false });
      y += 8;
      ticks.forEach(function (t, i) {
        var w = t === 0 ? (L.center || '0') : K.fmt(Math.abs(t), 'integer') + (i === ticks.length - 1 && L.axis_unit ? ' ' + L.axis_unit : '');
        var tw = c.measure(w, 'tick'), xx = xs2(t), an = xx + tw / 2 > W ? 'end' : xx - tw / 2 < 0 ? 'start' : 'middle';
        c.text(an === 'end' ? W : an === 'start' ? 0 : xx, y, w, { role: 'tick', anchor: an });
      });
      c.height(y + 4);
    }
  });
})(globalThis.OAChart);
