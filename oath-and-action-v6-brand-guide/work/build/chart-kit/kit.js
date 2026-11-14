/* Oath & Action chart kit, the shared renderer (Phase 3, round 0; contract 1 in
 * work/handoffs/phase-3/20261111_Round-0-Engineer-Notes.md).
 *
 * A classic script with no library and no build step. It defines one global, OAChart, in a browser page and in Node
 * alike. Load metrics.js first, then this file, then each form in forms/. It draws a chart as SVG from a spec, the data
 * rows and the page's tokens, and writes the figure around it: words from the spec, and a table equivalent as live text.
 * Color comes only from kit.css classes, which read oa.chart.* tokens; sizes come from the same tokens. The kit holds no
 * reader-facing words: those come from the spec and from words.json (passed in as opts.words).
 */
(function (root) {
  'use strict';
  var K = root.OAChart = root.OAChart || {};
  K.contract = 1;
  K.version = '0.3.0';
  K.forms = K.forms || {};
  var PHONE_MAX = 480;               // an artboard narrower than this draws the phone arrangement
  var ARTBOARDS = { reading: 'artboard-reading', mid: 'artboard-mid', wide: 'artboard-wide' };
  var ROLES = ['subject', 'context', 'secondary', 'baseline', 'gridline', 'label', 'point', 'point-keyline', 'band', 'track', 'light-fill',
    'land', 'party', 'leader', 'chip-fill', 'chip-label', 'surface', 'label-on-subject', 'sequential-outline',
    'seq-1', 'seq-2', 'seq-3', 'seq-4', 'seq-5', 'div-1', 'div-2', 'div-3', 'div-4', 'div-5', 'mag-1', 'mag-2', 'mag-3', 'mag-4',
    'cat-1', 'cat-2', 'cat-3', 'cat-4', 'on-cat-1', 'on-cat-2', 'on-cat-3', 'beside-cat-4', 'ghost', 'none'];
  K.ROLES = ROLES;
  var TEXT_ROLES = { tick: 'type-tick', label: 'type-label', note: 'type-note', big: 'type-big', eyebrow: 'type-eyebrow' };

  // ------------------------------------------------------------------------------------------------------------
  // Small helpers
  // ------------------------------------------------------------------------------------------------------------
  function esc(s) {
    return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }
  K.esc = esc;
  function r1(v) { return Math.round(v * 10) / 10; }     // coordinates to a tenth of a pixel
  function r2(v) { return Math.round(v * 100) / 100; }
  K.round = r1;
  function isnum(v) { return typeof v === 'number' && isFinite(v); }

  // ------------------------------------------------------------------------------------------------------------
  // Number and date formats (the only words the kit writes: digits, signs, separators and month names)
  // ------------------------------------------------------------------------------------------------------------
  var MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  var MINUS = '−';
  function group(n) {
    var s = String(Math.abs(n));
    var p = s.split('.');
    p[0] = p[0].replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    return p.join('.');
  }
  // RB-G1 (round 2): numbers round half away from zero on their decimal value, not the binary one: 12.35 to one place is
  // 12.4, though the double nearest 12.35 sits just under it. A value is read as its 15 significant digits, the most a
  // double holds exactly, so one computed by a division (dollars over 1e9) rounds as its decimal does.
  function dround(a, nd) {
    nd = nd || 0;
    if (!isFinite(a)) return a;
    var s = a.toPrecision(15);
    if (/e/i.test(s)) return Math.round(a * Math.pow(10, nd)) / Math.pow(10, nd);
    return Math.round(Number(s + 'e' + nd)) / Math.pow(10, nd);
  }
  K.dround = dround;
  function fixed(v, nd) { var p = dround(Math.abs(v), nd).toFixed(nd || 0).split('.'); p[0] = p[0].replace(/\B(?=(\d{3})+(?!\d))/g, ','); return p.join('.'); }
  function signed(v, txt) { return (v > 0 ? '+' : v < 0 ? MINUS : '') + txt; }
  K.fmt = function (v, format) {
    if (v === null || v === undefined || v === '') return '';
    var f = String(format || 'text'), nd = 0, m = f.match(/^([a-z-]+):(\d+)$/);
    if (m) { f = m[1]; nd = +m[2]; }
    switch (f) {
      case 'text': return String(v);
      case 'integer': return (v < 0 ? MINUS : '') + group(dround(Math.abs(v), 0));
      case 'number': return (v < 0 ? MINUS : '') + fixed(v, nd);
      case 'percent': return (v < 0 ? MINUS : '') + fixed(v, nd) + '%';
      // round 3 (maker B's S65): a share held as a fraction, printed as a percent: 0.9368 as "93.7%" with fraction-percent:1
      case 'fraction-percent': return (v < 0 ? MINUS : '') + fixed(dround(v * 100, 12), nd) + '%';
      case 'signed': return signed(v, fixed(v, nd));
      case 'points': return (v < 0 ? MINUS : '') + fixed(v, nd);
      // dollars (R-B2, round 1): $2,000 and −$2,000; signed-dollars +$2,000; dollars:2 keeps cents
      case 'dollars': return (v < 0 ? MINUS : '') + '$' + fixed(v, nd);
      case 'signed-dollars': return signed(v, '$' + fixed(v, nd));
      // billions (R-B7, round 1): a value in dollars as 173.2 billion; billions-value prints 173.2 for a column headed in billions
      case 'billions': return (v < 0 ? MINUS : '') + fixed(v / 1e9, nd) + ' billion';
      case 'billions-value': return (v < 0 ? MINUS : '') + fixed(v / 1e9, nd);
      // millions (ED-E7, round 1 fix pass): a count or amount as 5.7 million; millions-value prints 5.7 for an axis or column
      // headed in millions
      case 'millions': return (v < 0 ? MINUS : '') + fixed(v / 1e6, nd) + ' million';
      case 'millions-value': return (v < 0 ? MINUS : '') + fixed(v / 1e6, nd);
      // A-E2 (round 2): a column held in millions printed in billions, 36,104,000 as 36,104.0 billion; the -value form bare
      case 'billions-from-millions': return (v < 0 ? MINUS : '') + fixed(v / 1e3, nd) + ' billion';
      case 'billions-value-from-millions': return (v < 0 ? MINUS : '') + fixed(v / 1e3, nd);
      case 'compact-thousands':
      case 'signed-compact-thousands': {
        var a = Math.abs(v) * 1000, sg = f === 'signed-compact-thousands' ? (v > 0 ? '+' : v < 0 ? MINUS : '') : (v < 0 ? MINUS : '');
        if (a >= 1e6) return sg + dround(a / 1e6, a >= 1e7 ? 0 : 1).toFixed(a >= 1e7 ? 0 : 1) + ' million';
        return sg + group(dround(a / 1000, 0) * 1000);
      }
      case 'thousands': return (v < 0 ? MINUS : '') + group(m ? dround(Math.abs(v), 0) * 1000 : dround(Math.abs(v) * 1000, 0));
      case 'signed-thousands': return m ? signed(dround(Math.abs(v), 0) === 0 ? 0 : v, group(dround(Math.abs(v), 0) * 1000)) : signed(v, group(dround(Math.abs(v) * 1000, 0)));
      case 'month': { var mm = String(v).match(/^(\d{4})-(\d{2})/); return mm ? MONTHS[+mm[2] - 1] + ' ' + mm[1] : String(v); }
      case 'month-short': { var ms = String(v).match(/^(\d{4})-(\d{2})/); return ms ? MONTHS[+ms[2] - 1].slice(0, 3) + ' ' + ms[1] : String(v); }
      case 'date': { var d = String(v).match(/^(\d{4})-(\d{2})-(\d{2})/); return d ? MONTHS[+d[2] - 1] + ' ' + (+d[3]) + ', ' + d[1] : String(v); }
      case 'year': return String(v).slice(0, 4);
      default: return String(v);
    }
  };
  K.minus = MINUS;

  // ------------------------------------------------------------------------------------------------------------
  // Text measurement from metrics.js, the same in Node and in a browser
  // ------------------------------------------------------------------------------------------------------------
  var MET = null;
  function metrics() {
    if (MET) return MET;
    var M = root.OAChartMetrics;
    if (!M) throw new Error('OAChart: load metrics.js before kit.js');
    var idx = {};
    for (var i = 0; i < M.chars.length; i++) idx[M.chars[i]] = i;
    MET = { idx: idx, faces: M.faces, vertical: M.vertical };
    return MET;
  }
  function face_key(face, weight, tnum) {
    if (face === 'display') return 'Inter Tight|800';
    var w = weight >= 700 ? 700 : weight >= 600 ? 600 : 400;
    return 'Inter|' + w + (tnum ? '|tnum' : '');
  }
  K.measure = function (text, size, weight, face, tnum) {
    var m = metrics(), adv = m.faces[face_key(face, weight || 400, tnum)], s = String(text), w = 0;
    var fallback = adv[m.idx.n];
    for (var i = 0; i < s.length; i++) {
      var j = m.idx[s[i] === '\u00a0' ? ' ' : s[i]];   // a no-break space is as wide as a space
      w += j === undefined ? fallback : adv[j];
    }
    return w * size / 1000;
  };
  K.wrap = function (text, size, max, weight, face, pretty) {
    // lines break at spaces only, so a no-break space holds two words together
    var words = String(text).split(/[ \t\r\n]+/), lines = [], cur = '';
    for (var i = 0; i < words.length; i++) {
      var t = cur ? cur + ' ' + words[i] : words[i];
      if (cur && K.measure(t, size, weight, face) > max) { lines.push(cur); cur = words[i]; } else cur = t;
    }
    if (cur) lines.push(cur);
    // the design director's orphan guard (round 4), for a spec that sets typography.pretty: a last line of one word takes
    // the line above's last word where it fits, the line above keeping two or more (a global guard would move 56 signed-off
    // specs' drawings, so it is opt-in)
    var n = lines.length, pw = n > 1 && !/ /.test(lines[n - 1]) ? lines[n - 2].split(' ') : [];
    if (pretty && pw.length > 2 && K.measure(pw[pw.length - 1] + ' ' + lines[n - 1], size, weight, face) <= max) lines.splice(n - 2, 2, pw.slice(0, -1).join(' '), pw[pw.length - 1] + ' ' + lines[n - 1]);
    return lines;
  };

  // ------------------------------------------------------------------------------------------------------------
  // Tokens: numbers from tokens.css. In a browser the figure's computed style; in Node a map the CLI builds.
  // ------------------------------------------------------------------------------------------------------------
  function token_reader(source) {
    // source: a map {--oa-name: value} or a function name -> value
    var get = typeof source === 'function' ? source : function (n) { return source[n]; };
    var cache = {};
    var t = function (name) {
      if (name in cache) return cache[name];
      var v = get('--oa-chart-' + name);
      if (v === undefined || v === null || String(v).trim() === '') throw new Error('OAChart: token --oa-chart-' + name + ' is missing from tokens.css');
      var n = parseFloat(String(v));
      cache[name] = isNaN(n) ? String(v).trim() : n;
      return cache[name];
    };
    t.raw = function (name) { return get(name); };
    return t;
  }
  K.token_reader = token_reader;

  // ------------------------------------------------------------------------------------------------------------
  // Data: CSV, types, the spec's rows
  // ------------------------------------------------------------------------------------------------------------
  K.parse_csv = function (text) {
    // R3-3 (round 3): a line that holds only "" is a row with one empty cell (a one-column island's missing value), kept;
    // a line with nothing on it is still skipped
    var rows = [], row = [], cell = '', q = false, i = 0, s = String(text).replace(/^﻿/, ''), quoted = false;
    for (; i < s.length; i++) {
      var ch = s[i];
      if (q) {
        if (ch === '"') { if (s[i + 1] === '"') { cell += '"'; i++; } else q = false; } else cell += ch;
      } else if (ch === '"') { q = true; quoted = true; }
      else if (ch === ',') { row.push(cell); cell = ''; }
      else if (ch === '\n' || ch === '\r') {
        if (ch === '\r' && s[i + 1] === '\n') i++;
        row.push(cell); cell = '';
        if (row.length > 1 || row[0] !== '' || quoted) rows.push(row);
        row = []; quoted = false;
      } else cell += ch;
    }
    if (cell !== '' || row.length) { row.push(cell); rows.push(row); }
    var head = rows.shift() || [];
    return rows.map(function (r) { var o = {}; head.forEach(function (h, j) { o[h] = r[j] === undefined ? '' : r[j]; }); return o; });
  };
  K.type_rows = function (rows, columns) {
    // columns: the sidecar's {name: {type}}; numbers become numbers, empty cells null
    return rows.map(function (r) {
      var o = {};
      for (var k in r) {
        var v = r[k], t = columns && columns[k] && columns[k].type;
        if (v === '' || v === null || v === undefined) { o[k] = null; continue; }
        if (t === 'number' || t === 'integer') o[k] = typeof v === 'number' ? v : parseFloat(v);
        else if (t === 'boolean') o[k] = v === true || v === 'true' || v === '1' || v === 1;
        else if (t === 'year') o[k] = typeof v === 'number' ? v : parseInt(v, 10);
        else o[k] = typeof v === 'string' ? v : String(v);
      }
      return o;
    });
  };
  K.time = function (v) {
    // a date, month or year as a number of years, so one axis serves all three
    if (isnum(v)) return v;
    var s = String(v), m;
    if ((m = s.match(/^(\d{4})-(\d{2})-(\d{2})/))) {
      var y = +m[1], start = Date.UTC(y, 0, 1), end = Date.UTC(y + 1, 0, 1);
      return y + (Date.UTC(y, +m[2] - 1, +m[3]) - start) / (end - start);
    }
    if ((m = s.match(/^(\d{4})-(\d{2})$/))) return +m[1] + (+m[2] - 1) / 12;
    if ((m = s.match(/^(\d{4})$/))) return +m[1];
    return NaN;
  };

  // ------------------------------------------------------------------------------------------------------------
  // Scales and ticks
  // ------------------------------------------------------------------------------------------------------------
  function nice_step(span, count) {
    var raw = span / Math.max(1, count), mag = Math.pow(10, Math.floor(Math.log10(raw))), f = raw / mag;
    return (f <= 1 ? 1 : f <= 2 ? 2 : f <= 2.5 ? 2.5 : f <= 5 ? 5 : 10) * mag;
  }
  K.ticks = function (lo, hi, count, step) {
    step = step || nice_step(hi - lo, count || 5);
    var out = [];
    for (var v = Math.ceil(lo / step - 1e-9) * step; v <= hi + step * 1e-9; v += step) out.push(Math.abs(v) < step * 1e-9 ? 0 : r2(v));
    return out;
  };
  K.nice = function (lo, hi, count) {
    var step = nice_step(hi - lo, count || 5);
    var out = [Math.floor(lo / step + 1e-9) * step, Math.ceil(hi / step - 1e-9) * step];
    out.step = step;
    return out;
  };
  K.scale = {
    linear: function (d, r) {
      var f = function (v) { return r[0] + (v - d[0]) / (d[1] - d[0] || 1) * (r[1] - r[0]); };
      f.domain = d; f.range = r;
      f.invert = function (p) { return d[0] + (p - r[0]) / (r[1] - r[0] || 1) * (d[1] - d[0]); };
      return f;
    },
    sqrt: function (max_value, max_radius) {
      // a circle's area in proportion to its value (D2-124)
      var f = function (v) { return v > 0 ? Math.sqrt(v / max_value) * max_radius : 0; };
      f.max_value = max_value; f.max_radius = max_radius;
      return f;
    },
    band: function (keys, r, pad) {
      var n = keys.length, step = (r[1] - r[0]) / Math.max(1, n), bw = step * (1 - (pad === undefined ? 0.2 : pad));
      var f = function (k) { var i = keys.indexOf(k); return r[0] + step * i + (step - bw) / 2; };
      f.bandwidth = bw; f.step = step; f.keys = keys;
      return f;
    }
  };

  // ------------------------------------------------------------------------------------------------------------
  // The drawing context a form draws through
  // ------------------------------------------------------------------------------------------------------------
  function Ctx(spec, rows, opts) {
    this.spec = spec;
    this.rows = rows;
    // A-E8 (round 3 fix pass): where the kit draws only the first rows (a desk's phone part), every row, so a form's counts
    // and scales read the whole set (c.all_rows || c.rows); null otherwise
    this.all_rows = opts.all_rows || null;
    this.width = opts.width;
    this.phone = opts.width < PHONE_MAX;
    this.ground = opts.ground || 'newsprint';
    this.t = opts.t;
    this.uid = opts.uid || ('oac' + Math.floor(Math.random() * 1e6));
    this.labels = spec.labels || {};
    this.encode = spec.encode || {};
    this.annotations = spec.annotations || [];
    this.extra = opts.extra || {};
    this._els = [];
    this._defs = [];
    this.texts = [];
    this.marks = [];
    this.leaders = [];
    this.cells = [];   // D3-1546 (round 4): c.cell's boxes, read by checks.js
    this.warnings = [];
    this.ink = [];   // K-S2 (round 1 fix pass): the box of every shape drawn, marks or not, so the check finds one outside the drawing
    this._tf = 0;
    this._m = null;   // R3-2 (round 3): the affine of the moved or scaled group being drawn, [a, d, e, f] (x' = a x + e, y' = d y + f)
    this._seq = 0;   // the order shapes and words are drawn in, so the checks know what a halo knocks out (AX S2)
    this._h = 0;
    this._arr = null;
    this._job = null;
  }
  K.Ctx = Ctx;
  var SHAPE_LIFT = 12;
  var HALO_SEQ = 0;
  // BC S1, AX S2 (round 2 fix pass): does a shape's stroke cross a word's box (less 1.5 px a side)? Lines, a path's points,
  // a rect's or polygon's outline, a circle's ring. Shared with checks.js, which fails what the halo cannot clear.
  K.QUIET_STROKES = ['gridline', 'baseline', 'label', 'context', 'secondary'];
  K.stroke_crosses = function (b, t) {
    var x0 = t.x + 1.5, x1 = t.x + t.w - 1.5, y0 = t.y + 1.5, y1 = t.y + t.h - 1.5;
    if (x1 <= x0 || y1 <= y0 || b.x > x1 || b.x + b.w < x0 || b.y > y1 || b.y + b.h < y0) return false;
    if (b.ring) {
      var cx = b.ring[0], cy = b.ring[1], r = b.ring[2], nx = Math.max(x0, Math.min(cx, x1)), ny = Math.max(y0, Math.min(cy, y1));
      var far = Math.max(Math.hypot(x0 - cx, y0 - cy), Math.hypot(x1 - cx, y0 - cy), Math.hypot(x0 - cx, y1 - cy), Math.hypot(x1 - cx, y1 - cy));
      return Math.hypot(nx - cx, ny - cy) < r && r < far;
    }
    var segs = [];
    if (b.seg) segs.push(b.seg);
    else if (b.subs) b.subs.forEach(function (pts) {
      for (var i = 0; i + 1 < pts.length; i++) segs.push([pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1]]);
      if ((b.kind === 'polygon' || b.closed) && pts.length > 2) segs.push([pts[pts.length - 1][0], pts[pts.length - 1][1], pts[0][0], pts[0][1]]);
    });
    else if (b.kind === 'rect') segs.push([b.x, b.y, b.x + b.w, b.y], [b.x + b.w, b.y, b.x + b.w, b.y + b.h], [b.x + b.w, b.y + b.h, b.x, b.y + b.h], [b.x, b.y + b.h, b.x, b.y]);
    return segs.some(function (sg) { return seg_hits_box(sg[0], sg[1], sg[2], sg[3], x0, y0, x1, y1); });
  };
  // a filled shape that covers the whole of a word's box (a dot drawn over its connector, a knockout)
  K.covers = function (s, t) {
    var x0 = t.x + 1.5, x1 = t.x + t.w - 1.5, y0 = t.y + 1.5, y1 = t.y + t.h - 1.5, cs = [[x0, y0], [x1, y0], [x0, y1], [x1, y1]];
    if (s.ring) return cs.every(function (p) { return Math.hypot(p[0] - s.ring[0], p[1] - s.ring[1]) <= s.ring[2]; });
    if (s.poly) return cs.every(function (p) { return K.in_poly(s.poly, p[0], p[1]); });
    return s.x <= x0 && s.y <= y0 && s.x + s.w >= x1 && s.y + s.h >= y1;
  };
  // a stroke drawn before the word that crosses it and no filled shape drawn between them covers
  K.crossed_by = function (c_ink, t, test) {
    var solids = c_ink.filter(function (s) { return s.fill && s.fill !== 'none' && s.a > 0; });
    return c_ink.filter(function (b) {
      return b.stroke && !b.strike && test(b) && K.stroke_crosses(b, t) &&
        !solids.some(function (s) { return s.seq > b.seq && s.seq < t.seq && K.covers(s, t); });
    });
  };
  // a shape's box for the drawing-edge check
  // CD A-M2 (round 2 fix pass): with its painted area (a, the fill's) and stroke length (len), so the checks measure the
  // share of a view a color covers; o.stroke and o.width ride along
  // R3-2 (round 3): a shape inside a moved or scaled group (c.group({transform: 'translate(x,y) scale(k)'}), a map's
  // projection) is read through the group's transform, so the red share, crossing and edge checks reach it; only a group
  // whose transform the kit cannot read (a rotation) is still left out. R3-5: o.link marks a link between nodes, which the
  // layout guard reads as a line no word may sit under
  Ctx.prototype._ink = function (kind, x, y, w, h, o, geo) {
    if (this._tf) return;
    var g = geo || {}, M = this._m, poly = o && o._poly;
    var rec = { kind: kind, x: x, y: y, w: w, h: h, role: (o && (o.fill || o.stroke)) || '', fill: o && o.fill, plate: !!(o && o.cls && /\boac-fc-plate\b/.test(o.cls)), poly: poly,
      stroke: o && o.stroke, sw: o && o.stroke ? (+o.width || 1) : 0, a: g.a === undefined ? w * h : g.a, len: g.len === undefined ? 2 * (w + h) : g.len,
      seq: this._seq++, seg: g.seg, subs: g.subs, ring: g.ring, dash: !!(o && o.dash), strike: !!(o && o.strike), link: !!(o && o.link) };
    if (M) K.map_ink(rec, M);
    this.ink.push(rec);
  };
  // R3-2: one record mapped through an axis-aligned affine [a, d, e, f]: its box, points, ring, paint and stroke width
  K.map_ink = function (b, M) {
    var a = M[0], d = M[1], e = M[2], f = M[3], k = Math.sqrt(Math.abs(a * d));
    var pt = function (q) { return [a * q[0] + e, d * q[1] + f]; };
    var mv = function (S) { return S.map(function (pts) { return pts.map(pt); }); };
    var x0 = a * b.x + e, x1 = a * (b.x + b.w) + e, y0 = d * b.y + f, y1 = d * (b.y + b.h) + f;
    b.x = Math.min(x0, x1); b.w = Math.abs(x1 - x0); b.y = Math.min(y0, y1); b.h = Math.abs(y1 - y0);
    if (b.a !== undefined) b.a *= Math.abs(a * d);
    if (b.len !== undefined) b.len *= k;
    if (b.sw) b.sw *= k;
    if (b.seg) b.seg = pt(b.seg.slice(0, 2)).concat(pt(b.seg.slice(2, 4)));
    if (b.ring) b.ring = pt(b.ring).concat([b.ring[2] * k]);
    var same = b.subs && b.subs === b.poly;
    if (b.subs) b.subs = mv(b.subs);
    if (b.poly) b.poly = same ? b.subs : mv(b.poly);
    if (b.r !== undefined) b.r *= k;
    return b;
  };
  // R3-2: the affine a transform attribute gives, or null where it holds anything but translate and scale
  K.parse_transform = function (t) {
    var s = String(t || '').trim(), M = [1, 1, 0, 0], re = /(translate|scale)\(\s*(-?[\d.]+(?:e-?\d+)?)(?:[\s,]+(-?[\d.]+(?:e-?\d+)?))?\s*\)\s*/gy, m, at = 0;
    if (!s) return null;
    while ((m = re.exec(s))) {
      var p = +m[2], q = m[3] === undefined ? (m[1] === 'scale' ? p : 0) : +m[3];
      // the new step applies first, inside the steps before it: x' = M (step x)
      if (m[1] === 'translate') { M = [M[0], M[1], M[0] * p + M[2], M[1] * q + M[3]]; }
      else { M = [M[0] * p, M[1] * q, M[2], M[3]]; }
      at = re.lastIndex;
    }
    return at === s.length ? M : null;
  };
  // the area inside each subpath (shoelace) and the length along them, for a path's paint
  function poly_geo(subs, closed) {
    var a = 0, len = 0;
    (subs || []).forEach(function (pts) {
      var s = 0;
      for (var i = 0; i < pts.length; i++) {
        var p = pts[i], q = pts[(i + 1) % pts.length];
        s += p[0] * q[1] - q[0] * p[1];
        if (i + 1 < pts.length || closed) len += Math.sqrt((q[0] - p[0]) * (q[0] - p[0]) + (q[1] - p[1]) * (q[1] - p[1]));
      }
      a += Math.abs(s) / 2;
    });
    return { a: a, len: len };
  }
  K.poly_geo = poly_geo;
  // the box of a path drawn with absolute M, L, H and V commands only (lines and areas); null for curves
  function path_box(d) {
    if (/[^MLHVZ0-9.,\s+eE-]/.test(d)) return null;
    var re = /([MLHVZ])([^MLHVZ]*)/g, m, x = 0, y = 0, x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
    while ((m = re.exec(d))) {
      var n = (m[2].match(/-?(?:\d+\.?\d*|\.\d+)(?:e[-+]?\d+)?/gi) || []).map(Number);
      if (m[1] === 'H') n.forEach(function (v) { x = v; x0 = Math.min(x0, x); x1 = Math.max(x1, x); y0 = Math.min(y0, y); y1 = Math.max(y1, y); });
      else if (m[1] === 'V') n.forEach(function (v) { y = v; y0 = Math.min(y0, y); y1 = Math.max(y1, y); x0 = Math.min(x0, x); x1 = Math.max(x1, x); });
      else for (var i = 0; i + 1 < n.length; i += 2) { x = n[i]; y = n[i + 1]; x0 = Math.min(x0, x); x1 = Math.max(x1, x); y0 = Math.min(y0, y); y1 = Math.max(y1, y); }
    }
    return x0 <= x1 ? [x0, y0, x1 - x0, y1 - y0] : null;
  }
  // R3-5: the box of subpaths of [x, y]
  function pts_box(subs) {
    var x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
    for (var i = 0; i < subs.length; i++) for (var j = 0; j < subs[i].length; j++) {
      var q = subs[i][j];
      if (q[0] < x0) x0 = q[0]; if (q[0] > x1) x1 = q[0]; if (q[1] < y0) y0 = q[1]; if (q[1] > y1) y1 = q[1];
    }
    return x0 <= x1 ? [x0, y0, x1 - x0, y1 - y0] : null;
  }
  // A-E1 (round 2): the outline of a filled path of absolute M, L, H, V and Z commands, as subpaths of [x, y], so the fill
  // under a word is read from a band or an area as it is from a rect; null for curves
  function path_poly(d) {
    if (/[^MLHVZ0-9.,\s+eE-]/.test(d)) return null;
    var re = /([MLHVZ])([^MLHVZ]*)/g, m, x = 0, y = 0, subs = [], cur = null;
    var at = function () { if (!cur) { cur = []; subs.push(cur); } cur.push([x, y]); };
    while ((m = re.exec(d))) {
      var n = (m[2].match(/-?(?:\d+\.?\d*|\.\d+)(?:e[-+]?\d+)?/gi) || []).map(Number);
      if (m[1] === 'Z') { cur = null; continue; }
      if (m[1] === 'M') cur = null;
      if (m[1] === 'H') n.forEach(function (v) { x = v; at(); });
      else if (m[1] === 'V') n.forEach(function (v) { y = v; at(); });
      else for (var i = 0; i + 1 < n.length; i += 2) { x = n[i]; y = n[i + 1]; at(); }
    }
    return subs.length ? subs : null;
  }
  // even-odd across every subpath, as SVG fills a path by default (nonzero gives the same for the simple bands a form draws)
  K.in_poly = function (subs, px, py) {
    var inside = false;
    (subs || []).forEach(function (pts) {
      for (var i = 0, j = pts.length - 1; i < pts.length; j = i++) {
        var a = pts[i], b = pts[j];
        if ((a[1] > py) !== (b[1] > py) && px < (b[0] - a[0]) * (py - a[1]) / (b[1] - a[1]) + a[0]) inside = !inside;
      }
    });
    return inside;
  };
  function attrs(o) {
    var s = '';
    for (var k in o) if (o[k] !== undefined && o[k] !== null && o[k] !== false) s += ' ' + k + '="' + esc(o[k]) + '"';
    return s;
  }
  function cls_of(o) {
    var c = [];
    if (o.fill) c.push('oac-f-' + o.fill);
    if (o.stroke) c.push('oac-s-' + o.stroke);
    if (o.cls) c.push(o.cls);
    // AX S3 (round 2 fix pass): fc: 'total' gives a total or a subtotal (a waterfall's) its own paint in forced colors, the
    // ground with a 2 px CanvasText outline, so it never takes a step's ink
    if (o.fc === 'total') c.push('oac-fc-total');
    // AX-S1 (round 3 fix pass): 'region', a map's merged fill, takes no edge in forced colors (map_mesh draws the lines);
    // 'muted', a light fill with no edge that must stay apart from an outline (S72's "did not vote"), takes GrayText with
    // no edge; 'forced', a mark drawn for forced colors only (S74's authority cell's second edge), hidden otherwise
    if (o.fc === 'region' || o.fc === 'muted' || o.fc === 'forced') c.push('oac-fc-' + o.fc);
    return c.join(' ') || undefined;
  }
  function data_of(o, base) {
    var d = o.data || {};
    for (var k in d) if (d[k] !== undefined && d[k] !== null) base['data-' + k] = d[k];
    // ED-E15 (round 2): marks the title names together (ruling (c)) carry one job, so the red count reads them as one
    if (o.job !== undefined && o.job !== null) base['data-oa-job'] = o.job;
    return base;
  }
  Ctx.prototype.size = function (role) {
    var r = TEXT_ROLES[role] || 'type-label', s = this.t(r);
    if (role === 'big' && this.phone) s = this.t('type-big-phone');
    if (role === 'label' && this.phone) s = Math.max(this.t('type-phone-min'), Math.min(s, this.t('type-phone-min')));
    return s;
  };
  Ctx.prototype.measure = function (words, role, weight, tnum, open) {
    var size = typeof role === 'number' ? role : this.size(role || 'label');
    return K.measure(words, size, weight || 400, role === 'big' ? 'display' : 'reading', tnum) + (open && role === 'big' ? K.open_space(words, size) : 0);
  };
  // BC S12 (round 2 fix pass): a big figure that holds words ("At least 17", "87% and 88%") may set them in open tracking,
  // c.text(..., {role: 'big', open: true}): no tightening and a tenth of an em more at each word space (kit.css
  // .oac-t-open), so its words read apart at 1x; c.measure(words, 'big', weight, tnum, true) measures it so
  K.OPEN_WORD_SPACE = 0.1;
  K.open_space = function (line, size) { var n = (String(line).match(/[ \u00a0]/g) || []).length; return n * K.OPEN_WORD_SPACE * size; };
  Ctx.prototype.wrap = function (words, role, max, weight) {
    return K.wrap(words, this.size(role || 'note'), max, weight || 400, role === 'big' ? 'display' : 'reading', (this.spec.typography || {}).pretty);
  };
  Ctx.prototype._push = function (s) { (this._grp || this._els).push(s); };
  Ctx.prototype.group = function (o) {
    var self = this, prev = this._grp, buf = [], pjob = this._job, pm = this._m;
    // R3-2: a translate and scale group maps its shapes into the drawing for the checks; any other transform hides them
    var gm = o && o.transform ? K.parse_transform(o.transform) : null, tf = !!(o && o.transform) && !gm;
    if (gm) this._m = pm ? [pm[0] * gm[0], pm[1] * gm[1], pm[0] * gm[2] + pm[2], pm[1] * gm[3] + pm[3]] : gm;
    this._grp = buf;
    if (tf) this._tf++;
    if (o && o.job !== undefined && o.job !== null) this._job = o.job;
    return {
      end: function () {
        self._grp = prev;
        self._job = pjob;
        self._m = pm;
        if (tf) self._tf--;
        var a = data_of(o || {}, { 'class': cls_of(o || {}), transform: o && o.transform });
        self._push('<g' + attrs(a) + '>' + buf.join('') + '</g>');
      }
    };
  };
  // R4-4 (round 4): a card draws its inner form (encode.of) in a scaled group at width w / k from x, y, so the inner form's
  // words print at k times their size and the checks read them there; o reaches the inner form as c.card. Returns the
  // height drawn, in the card's px.
  Ctx.prototype.inner = function (x, y, w, k, o) {
    var inner = K.forms[this.encode.of], sv = [this.width, this.phone, this._h, this.card], n0 = this.texts.length, ih;
    if (!inner || !inner.draw || inner === K.forms[this.spec.form]) throw new Error('a card names no other drawn form in encode.of');
    var g = this.group({ transform: 'translate(' + x + ',' + y + ') scale(' + k + ')' });
    this.width = Math.round(w / k); this.phone = this.width < PHONE_MAX; this.card = o || {}; this._h = 0;
    try { inner.draw(this); ih = this._h * k; } finally { g.end(); this.width = sv[0]; this.phone = sv[1]; this._h = sv[2]; this.card = sv[3]; }
    this.texts.slice(n0).forEach(function (b) { ih = Math.max(ih, (b.bottom !== undefined ? b.bottom : b.y + b.h) - y); });
    return ih;
  };
  // D3-1546 (round 4): a cell, a box that must hold every shape and word drawn while it is open (a tile's code, figure and
  // arrow) with o.spare px to spare on every side (default 1); checks.js fails one that leaves it. c.cell(null) closes it.
  Ctx.prototype.cell = function (x, y, w, h, o) {
    var b = this._cell;
    if (b) b.s1 = this._seq;
    this._cell = b = x === null || this._tf ? null : { x: x, y: y, w: w, h: h, s0: this._seq, s1: 1e9, o: o || {} };
    if (b) { if (this._m) K.map_ink(b, this._m); this.cells.push(b); }
  };
  Ctx.prototype.mark = function (m) {
    if (m.job === undefined || m.job === null) m.job = this._job;
    if (this._tf) return m;
    if (this._m) { K.map_ink(m, this._m); m.moved = true; }
    this.marks.push(m);
    return m;
  };
  Ctx.prototype.rect = function (x, y, w, h, o) {
    o = o || {};
    if (w < 0) { x += w; w = -w; }
    if (h < 0) { y += h; h = -h; }
    var a = data_of(o, { x: r1(x), y: r1(y), width: r1(w), height: r1(h), 'class': cls_of(o), rx: o.rx, 'stroke-width': o.width, 'stroke-dasharray': o.dash });
    if (o.pattern) a.fill = 'url(#' + this.uid + '-' + o.pattern + ')';
    this._push('<rect' + attrs(a) + '/>');
    this._ink('rect', x, y, w, h, o, { a: w * h, len: 2 * (w + h) });
    if (o.mark !== false) this.mark({ kind: o.kind || 'rect', x: x, y: y, w: w, h: h, fill: o.fill, fc: o.fc, stroke: o.stroke, data: o.data || {}, zero: o.zero, axis: o.axis, job: o.job });
  };
  // BC S16 (round 1 fix pass): a straight line of a whole-pixel width lands on the pixel grid, so it draws crisp at 1x: an
  // even width (2 px) on a whole pixel, an odd width (1 or 3 px) on a half pixel. Other widths (1.5 px) are left as drawn.
  K.snap = function (v, w) {
    w = +w;
    if (!(w > 0) || Math.abs(w - Math.round(w)) > 1e-9) return v;
    return Math.round(w) % 2 ? Math.round(v - 0.5) + 0.5 : Math.round(v);
  };
  Ctx.prototype.line = function (x1, y1, x2, y2, o) {
    o = o || {};
    if (o.width) {
      if (x1 === x2) x1 = x2 = K.snap(x1, o.width);
      else if (y1 === y2) y1 = y2 = K.snap(y1, o.width);
    }
    var a = data_of(o, { x1: r1(x1), y1: r1(y1), x2: r1(x2), y2: r1(y2), 'class': cls_of(o), 'stroke-width': o.width, 'stroke-dasharray': o.dash });
    this._push('<line' + attrs(a) + '/>');
    this._ink('line', Math.min(x1, x2), Math.min(y1, y2), Math.abs(x2 - x1), Math.abs(y2 - y1), o, { a: 0, len: Math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1)), seg: [x1, y1, x2, y2] });
    // a leader is kept for the guard, which fails one that runs through a label (D3-93)
    if (o.stroke === 'leader' && !this._tf) {
      var Lm = this._m ? K.map_ink({ x: 0, y: 0, w: 0, h: 0, seg: [x1, y1, x2, y2] }, this._m).seg : [x1, y1, x2, y2];
      this.leaders.push({ x1: Lm[0], y1: Lm[1], x2: Lm[2], y2: Lm[3] });
    }
    if (o.mark !== false) this.mark({ kind: o.kind || 'line', x: Math.min(x1, x2), y: Math.min(y1, y2), w: Math.abs(x2 - x1), h: Math.abs(y2 - y1), stroke: o.stroke, data: o.data || {}, job: o.job });
  };
  Ctx.prototype.path = function (d, o, box) {
    o = o || {};
    var a = data_of(o, { d: d, 'class': cls_of(o), 'stroke-width': o.width, 'stroke-dasharray': o.dash });
    if (o.pattern) a.fill = 'url(#' + this.uid + '-' + o.pattern + ')';
    this._push('<path' + attrs(a) + '/>');
    // R3-5 (round 3): a curve (an arc, a flow band) may pass its points as o.pts, subpaths of [x, y], so the checks read it
    // as they read a path of straight lines; the element keeps its curve
    // (and a map's shapes pass the points they were drawn from, which saves reading the string again)
    var dd = String(d), given = o.pts || null, closed = given ? (o.closed !== undefined ? !!o.closed : /Z\s*$/i.test(dd)) : /Z/i.test(dd);
    var pb = given ? pts_box(given) : (path_box(dd) || box);
    // A-E1: a filled path keeps its outline, so a word set on it reads its fill (fill_under, the forced-colors check)
    var poly = o.fill && o.fill !== 'none' ? (given || path_poly(dd)) : null;
    // its paint: the area inside its outline and the length along it, read from its points (a curve: from its box)
    var pg = poly ? poly_geo(poly, true) : null;
    var pts = poly || given || path_poly(dd);
    if (!pg) { pg = pts ? poly_geo(pts, closed) : null; if (pg && !(o.fill && o.fill !== 'none')) pg.a = 0; }
    if (pg && pts) { pg.subs = pts; pg.closed = closed; }
    if (pb) this._ink('path', pb[0], pb[1], pb[2], pb[3], poly ? Object.assign({}, o, { _poly: poly }) : o, pg || { a: pb[2] * pb[3], len: pb[2] + pb[3] });
    if (box && o.mark !== false) this.mark({ kind: o.kind || 'path', x: box[0], y: box[1], w: box[2], h: box[3], fill: o.fill, fc: o.fc, stroke: o.stroke, data: o.data || {}, job: o.job, poly: poly || undefined });
  };
  Ctx.prototype.datum = function (x, y, o) {
    // a record for the checks at a point the drawing already inks (a line's vertex): no element, no bytes
    this.mark({ kind: 'datum', x: x, y: y, w: 0, h: 0, data: (o && o.data) || {} });
  };
  Ctx.prototype.circle = function (cx, cy, r, o) {
    o = o || {};
    var a = data_of(o, { cx: r1(cx), cy: r1(cy), r: r2(r), 'class': cls_of(o), 'stroke-width': o.width });
    this._push('<circle' + attrs(a) + '/>');
    this._ink('circle', cx - r, cy - r, 2 * r, 2 * r, o, { a: Math.PI * r * r, len: 2 * Math.PI * r, ring: [cx, cy, r] });
    if (o.mark !== false) this.mark({ kind: o.kind || 'circle', x: cx - r, y: cy - r, w: 2 * r, h: 2 * r, r: r, fill: o.fill, fc: o.fc, stroke: o.stroke, data: o.data || {}, area_of: o.area_of, row: o.row, job: o.job });
  };
  Ctx.prototype.polygon = function (pts, o) {
    o = o || {};
    var xs = pts.map(function (p) { return p[0]; }), ys = pts.map(function (p) { return p[1]; });
    var a = data_of(o, { points: pts.map(function (p) { return r1(p[0]) + ',' + r1(p[1]); }).join(' '), 'class': cls_of(o) });
    this._push('<polygon' + attrs(a) + '/>');
    var pgeo = poly_geo([pts], true); pgeo.subs = [pts]; pgeo.closed = true;
    this._ink('polygon', Math.min.apply(null, xs), Math.min.apply(null, ys), Math.max.apply(null, xs) - Math.min.apply(null, xs), Math.max.apply(null, ys) - Math.min.apply(null, ys), o, pgeo);
    if (o.mark !== false) this.mark({ kind: o.kind || 'polygon', x: Math.min.apply(null, xs), y: Math.min.apply(null, ys), w: Math.max.apply(null, xs) - Math.min.apply(null, xs), h: Math.max.apply(null, ys) - Math.min.apply(null, ys), fill: o.fill, fc: o.fc, data: o.data || {}, job: o.job });
  };
  // BC S1 (round 2 fix pass): the box c.text would give these words, drawn nothing, so a part can set a knockout under them
  Ctx.prototype.text_box = function (x, y, words, o) {
    o = o || {};
    if (this.spec.typography) words = K.typeset(this.spec, words);
    var role = o.role || 'label', size = o.size || this.size(role), weight = o.weight || 400, anchor = o.anchor || 'start';
    var face = o.face || (role === 'big' ? 'display' : 'reading');
    var lines = o.max ? K.wrap(words, size, o.max, weight, face, (this.spec.typography || {}).pretty) : [String(words)];
    var lh = o.leading || Math.round(size * (role === 'note' ? 1.36 : 1.25)), w = 0, open = !!o.open && face === 'display' && /[ \u00a0]/.test(String(words));
    lines.forEach(function (ln) { w = Math.max(w, K.measure(ln, size, weight, face, o.tnum) + (open ? K.open_space(ln, size) : 0)); });
    var x0 = anchor === 'middle' ? x - w / 2 : anchor === 'end' ? x - w : x;
    var vm = metrics().vertical[face === 'display' ? 'Inter Tight|800' : 'Inter|400'] || { ascent: 969, descent: 241 };
    var asc = size * vm.ascent / 1000, desc = size * vm.descent / 1000, half = (asc + desc - size) / 2;
    return { x: x0, y: y - asc + half, w: w, h: asc + desc - 2 * half + lh * (lines.length - 1), lines: lines.length, size: size };
  };
  Ctx.prototype.text = function (x, y, words, o) {
    // y is the baseline. o: role (tick, label, note, big, eyebrow), weight, anchor, fill, halo, tnum, max (wrap width)
    o = o || {};
    if (this.spec.typography) words = K.typeset(this.spec, words);   // D3-519
    var role = o.role || 'label', size = o.size || this.size(role), weight = o.weight || 400, anchor = o.anchor || 'start';
    var face = o.face || (role === 'big' ? 'display' : 'reading');
    var lines = o.max ? K.wrap(words, size, o.max, weight, face, (this.spec.typography || {}).pretty) : [String(words)];
    var lh = o.leading || Math.round(size * (role === 'note' ? 1.36 : 1.25));
    var self = this, w = 0, open = !!o.open && face === 'display' && /[ \u00a0]/.test(String(words));
    lines.forEach(function (ln) { w = Math.max(w, K.measure(ln, size, weight, face, o.tnum) + (open ? K.open_space(ln, size) : 0)); });
    var x0 = anchor === 'middle' ? x - w / 2 : anchor === 'end' ? x - w : x;
    var cls = ['oac-t', 'oac-t-' + (face === 'display' ? 'big' : role), 'oac-w' + Math.round(weight / 100), o.fill ? 'oac-f-' + o.fill : (role === 'tick' ? 'oac-f-secondary' : 'oac-f-label')];
    if (o.halo) cls.push('oac-halo');
    if (o.tnum) cls.push('oac-tnum');
    if (open) cls.push('oac-t-open');
    // second pass (maker A's flag): in forced colors a mark in GrayText (seq-3, div-5, mag-3, cat-2, context) is a mid ink in
    // both themes, so a word set on one takes Canvas, as a word on a dark fill does; on context beside a red point, whose
    // marks take the ground (access S10), it keeps CanvasText (kit.css)
    var M = this._m, ux = x0 + w / 2, uy = y - size * 0.35;
    if (M) { ux = M[0] * ux + M[2]; uy = M[1] * uy + M[3]; }
    var under = K.FC_ON_DARK.indexOf(o.fill) < 0 ? this.fill_under(ux, uy) : null;
    var on_gray = !!under && K.FC[under] === 'GrayText';
    if (on_gray) { cls.push('oac-fc-on-gray'); if (under === 'context') cls.push('oac-fc-on-context'); }
    // BC S1 (round 2 fix pass): a word on the ground with no halo carries two markers the draw resolves once every shape is
    // drawn: where a quiet line drawn before it (a gridline, an axis, a total line) runs through it, a knockout of the
    // ground behind it, or the ground's halo where a knockout would touch another shape
    var hm = !o.halo && !under ? ++HALO_SEQ : 0;
    var a = data_of(o, { x: r1(x), y: r1(y), 'class': cls.join(' ') + (hm ? '\u0002' + hm + '\u0002' : ''), 'font-size': size, 'text-anchor': anchor === 'start' ? undefined : anchor });
    var body = lines.length === 1 ? esc(lines[0]) : lines.map(function (ln, i) { return '<tspan x="' + r1(x) + '"' + (i ? ' dy="' + lh + '"' : '') + '>' + esc(ln) + '</tspan>'; }).join('');
    this._push((hm ? '\u0003' + hm + '\u0003' : '') + '<text' + attrs(a) + '>' + body + '</text>');
    // the box the browser gives this text: its line box (ascent 0.969 em, descent 0.241 em, from the metrics) for the edges,
    // and that box less the half-leading for overlaps, as dataviz_check.js --kit measures a rendered drawing
    var vm = metrics().vertical[face === 'display' ? 'Inter Tight|800' : 'Inter|400'] || { ascent: 969, descent: 241 };
    var asc = size * vm.ascent / 1000, desc = size * vm.descent / 1000, half = (asc + desc - size) / 2;
    var box = { x: x0, y: y - asc + half, w: w, h: asc + desc - 2 * half + lh * (lines.length - 1), size: size, words: String(words), role: role,
      overlap_ok: !!o.overlap_ok, id: o.guard_id, top: y - asc, bottom: y + desc + lh * (lines.length - 1), halo: !!o.halo, fill: o.fill,
      on_gray: on_gray, on_context: on_gray && under === 'context', seq: this._seq++, hm: hm,
      margin_of: o.margin_of === undefined || o.margin_of === null ? undefined : String(o.margin_of), margin_note: !!o.margin_note };
    // R3-2: words inside a moved or scaled group are read where they print, at the size they print (a knockout would sit in
    // the group's own units, so the kit clears them with the halo instead)
    if (M) {
      var k = Math.sqrt(Math.abs(M[0] * M[1]));
      box.x = M[0] * box.x + M[2]; box.y = M[1] * box.y + M[3]; box.w *= Math.abs(M[0]); box.h *= Math.abs(M[1]);
      box.top = M[1] * box.top + M[3]; box.bottom = M[1] * box.bottom + M[3]; box.size *= k; box.moved = true;
    }
    this.texts.push(box);
    return box;
  };
  // the fill role of the last filled rect or circle drawn under a point, marks or not, or null; a plate set under words on a
  // fill (oac-fc-plate, Canvas in forced colors) answers 'plate', and a shape with no fill lets the one under it show
  Ctx.prototype.fill_under = function (px, py) {
    for (var i = this.ink.length - 1; i >= 0; i--) {
      var m = this.ink[i];
      if ((m.kind !== 'rect' && m.kind !== 'circle' && !(m.kind === 'path' && m.poly)) || !(m.w > 0) || !(m.h > 0)) continue;
      var inside = m.kind === 'circle' ? Math.pow(px - (m.x + m.w / 2), 2) + Math.pow(py - (m.y + m.h / 2), 2) < Math.pow(m.w / 2, 2)
        : m.kind === 'path' ? K.in_poly(m.poly, px, py) : px > m.x && px < m.x + m.w && py > m.y && py < m.y + m.h;
      if (!inside) continue;
      if (m.plate) return 'plate';
      if (m.fill && m.fill !== 'none') return m.fill;
    }
    return null;
  };
  Ctx.prototype.pattern = function (name, kind) {
    // a hatch for a preliminary or estimated value: lines in the mark's color on no fill (oa.chart.hatch.*)
    var p = this.t('hatch-pitch'), wgt = this.t('hatch-weight'), id = this.uid + '-' + name;
    if (this._defs.some(function (d) { return d.indexOf('id="' + id + '"') >= 0; })) return;
    this._defs.push('<pattern id="' + id + '" width="' + p + '" height="' + p + '" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">' +
      '<line x1="0" y1="0" x2="0" y2="' + p + '" class="oac-s-' + (kind || 'subject') + '" stroke-width="' + wgt + '"/></pattern>');
  };
  Ctx.prototype.key = function (entries) {
    // a key the reader matches marks against: [{fill, pattern, direct}], for the grayscale lightness test (C3a)
    this.keys = this.keys || [];
    this.keys.push(entries);
  };
  Ctx.prototype.height = function (h) { this._h = Math.max(this._h, Math.ceil(h)); };
  // RS-S3 (round 2, contract R2-C4): a form that draws its phone arrangement at a desk width (heat-table's chips at 558 px)
  // says so, c.arrange('phone'); under 480 px the kit says it. The guide hides the desk's phone drawing beside a figure that
  // already draws the phone form.
  Ctx.prototype.arrange = function (name) { this._arr = String(name); };
  // RF-25 (after the second pass): an interval form whose middle interval hides even behind 7 px dots at this width
  // draws no interval lines, prints each row's margin beside its value (c.text(..., {margin_of: key})) and a note in the
  // drawing (c.text(..., {margin_note: true})), and says so here; the check passes that state only with every margin
  // printed and the note drawn
  Ctx.prototype.margins_in_words = function () { this._ivw = true; };
  Ctx.prototype.warn = function (w) { this.warnings.push(w); };
  Ctx.prototype.label = function (name, fallback) {
    var v = this.labels[name];
    if (v === undefined || v === null) {
      if (fallback === undefined) this.warn('labels.' + name + ' is missing from the spec');
      return fallback === undefined ? '' : fallback;
    }
    return v;
  };
  Ctx.prototype.field = function (name, required) {
    var f = this.encode[name];
    if (required !== false && (f === undefined || f === null)) throw new Error('spec ' + this.spec.id + ': encode.' + name + ' is missing');
    return f;
  };

  // ------------------------------------------------------------------------------------------------------------
  // Register a form; draw one
  // ------------------------------------------------------------------------------------------------------------
  K.register_chart = function (def) {
    // R4-3 (round 4): a card form registers html (built in Node, never on the page) in place of draw
    if (!def || !def.form || typeof (def.draw || def.html) !== 'function') throw new Error('register_chart: a form needs "form" and "draw" or "html"');
    if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(def.form)) throw new Error('register_chart: form IDs are kebab-case: ' + def.form);
    def.encode = def.encode || {};
    def.labels = def.labels || [];
    def.phone = def.phone || 'same';
    K.forms[def.form] = def;
    return def;
  };
  K.artboard = function (spec, t, container) {
    var want = t(ARTBOARDS[spec.artboard || 'reading'] || 'artboard-reading');
    return container ? Math.min(want, Math.floor(container)) : want;
  };
  // C-M2, D3-1324 (round 3 fix pass): spec.stage, a width in px, draws the desk drawing at that one width wherever the
  // column gives the drawing PHONE_MAX px or more, in a frame that scrolls sideways where the column is narrower; under
  // PHONE_MAX the phone drawing takes the column's width as before. For a drawing approved at one width that no column
  // gives it (S12's arrows at board 1's 1024 px). Returns the width to draw at.
  // DR-261 (round 4): spec.stage_min, a width in px, is a floor: a desk drawing takes the column's width where the column
  // gives stage_min px or more, and draws at stage_min in the same scrolling frame where it gives less (S12's stacked tile,
  // 618 px)
  K.PHONE_MAX = PHONE_MAX;
  K.draw_width = function (spec, w) { return !spec || w < PHONE_MAX ? w : spec.stage ? Math.round(+spec.stage) : spec.stage_min ? Math.max(w, Math.round(+spec.stage_min)) : w; };
  K.draw = function (spec, rows, opts) {
    // returns {svg, width, height, texts, marks, warnings, guard}
    var def = K.forms[spec.form];
    if (!def) throw new Error('OAChart: form "' + spec.form + '" is not registered');
    var t = opts.t || token_reader(opts.tokens || {});
    var width = Math.round(opts.width || K.artboard(spec, t));
    var c = new Ctx(spec, rows, { width: width, ground: opts.ground, t: t, extra: opts.extra, all_rows: opts.all_rows, uid: opts.uid || ('oac-' + String(spec.id).toLowerCase() + '-' + width) });
    // R4-4 (round 4): a card's crop, drawn at its true size: exactly crop[1] px tall, every word 36 px or more (13 px in a feed)
    if (opts.crop) { c.crop = { w: width, h: opts.crop[1], name: width + 'x' + opts.crop[1] }; c.min_text = K.CARD_MIN_TEXT; }
    if (def.inner && spec.encode && K.forms[spec.encode.of]) {
      var inn = K.forms[spec.encode.of];
      def = Object.assign({}, def, { encode: Object.assign({}, inn.encode, def.encode), labels: def.labels.concat(inn.labels) });
    }
    for (var e in def.encode) {
      if (def.encode[e].slice(-1) !== '?' && (spec.encode || {})[e] === undefined) c.warn('encode.' + e + ' is missing for form ' + spec.form);
    }
    for (var g in (spec.encode || {})) if (!(g in def.encode)) c.warn('encode.' + g + ' is not a name form ' + spec.form + ' reads');
    for (var l in (spec.labels || {})) if (def.labels.indexOf(l) < 0) c.warn('labels.' + l + ' is not a name form ' + spec.form + ' reads');
    def.draw(c);
    // a text whose line box rises above the top edge moves the whole drawing down by that much, so nothing is cut; so does
    // a shape's short stub (an axis line run past its first bar, up to SHAPE_LIFT px: K-S2); a shape further out is a fault
    // the check reports
    var lift = 0, lift_dy = 0;
    c.texts.forEach(function (b) { lift = Math.max(lift, -(b.top !== undefined ? b.top : b.y)); });
    c.ink.forEach(function (b) { if (-b.y <= SHAPE_LIFT) lift = Math.max(lift, -b.y); });
    if (lift > 0.25) {
      var dy = Math.ceil(lift);
      lift_dy = dy;
      c._els = ['<g transform="translate(0,' + dy + ')">' + c._els.join('') + '</g>'];
      c.texts.forEach(function (b) { b.y += dy; if (b.top !== undefined) { b.top += dy; b.bottom += dy; } });
      c.marks.forEach(function (m) { m.y += dy; if (m.zero !== undefined && m.axis !== 'x') m.zero += dy; });
      c.leaders.forEach(function (l) { l.y1 += dy; l.y2 += dy; });
      c.cells.forEach(function (b) { b.y += dy; });
      // the shapes' outlines and points move with them (AX S2: the crossing check reads them against the moved words)
      var mv = function (S) { return S.map(function (pts) { return pts.map(function (q) { return [q[0], q[1] + dy]; }); }); };
      c.ink.forEach(function (b) {
        b.y += dy;
        if (b.seg) b.seg = [b.seg[0], b.seg[1] + dy, b.seg[2], b.seg[3] + dy];
        if (b.ring) b.ring = [b.ring[0], b.ring[1] + dy, b.ring[2]];
        var same = b.subs && b.subs === b.poly;
        if (b.subs) b.subs = mv(b.subs);
        if (b.poly) b.poly = same ? b.subs : mv(b.poly);
      });
      c.marks.forEach(function (m) { if (m.poly) m.poly = mv(m.poly); });
      c._h += dy;
    }
    // the drawing is as tall as its tallest part: the form's height, every text and every mark
    var h = c._h;
    c.texts.forEach(function (b) { h = Math.max(h, Math.ceil((b.bottom !== undefined ? b.bottom : b.y + b.h) + 2)); });
    c.marks.forEach(function (m) { h = Math.max(h, Math.ceil(m.y + m.h + 1)); });
    h = c.crop ? c.crop.h : Math.max(1, h);
    // BC S1: words on the ground that a quiet line drawn before them crosses are cleared: a knockout of the ground behind
    // their box, 2 px wider each side, which cuts the line cleanly (a minus sign or a decimal point keeps its shape); where
    // that box would touch any other shape or word drawn before them, the ground's halo round their letters. Every other
    // marker goes, so a drawing with nothing to clear is the string it was.
    var halo_on = {}, knock_on = {};
    var quiet = function (b) { return b.stroke && !b.fill && K.QUIET_STROKES.indexOf(b.stroke) >= 0; };
    var hits = function (b, k) { return b.x < k.x + k.w && k.x < b.x + b.w && b.y < k.y + k.h && k.y < b.y + b.h; };
    c.texts.forEach(function (t) {
      if (!t.hm) return;
      // R3-5: a link is never cleared this way; the layout guard fails one through a word (K.guard)
      if (!K.crossed_by(c.ink, t, function (b) { return b.seq < t.seq && !b.link && K.QUIET_STROKES.indexOf(b.stroke) >= 0; }).length) return;
      var k = { x: Math.max(0, t.x - 2), y: t.y, w: Math.min(width, t.x + t.w + 2) - Math.max(0, t.x - 2), h: t.h };
      var touch = !!t.moved || c.ink.some(function (b) { return b.seq < t.seq && !quiet(b) && !(b.fill === 'surface' || (b.fill === 'none' && !b.stroke)) && hits({ x: b.x - 0.5, y: b.y - 0.5, w: b.w + 1, h: b.h + 1 }, k); }) ||
        c.texts.some(function (o2) { return o2 !== t && o2.seq < t.seq && hits(o2, k); });
      if (touch) halo_on[t.hm] = true;
      else knock_on[t.hm] = '<rect x="' + r1(k.x) + '" y="' + r1(k.y - lift_dy) + '" width="' + r1(k.w) + '" height="' + r1(k.h) + '" class="oac-f-surface"/>';
      t.halo = true;
      t.cleared = touch ? 'halo' : 'knockout';
    });
    c._els = c._els.map(function (e) {
      if (e.indexOf('\u0002') < 0 && e.indexOf('\u0003') < 0) return e;
      return e.replace(/\u0002(\d+)\u0002/g, function (_, n) { return halo_on[n] ? ' oac-halo' : ''; })
        .replace(/\u0003(\d+)\u0003/g, function (_, n) { return knock_on[n] || ''; });
    });
    var guard = K.guard(c, width, h);
    var title = spec.title && !opts.bare ? '<title>' + esc(spec.title) + '</title>' : '';   // a table-mode island leaves both out; the figure names the drawing
    var desc = spec.alt && !opts.bare ? '<desc>' + esc(spec.alt) + '</desc>' : '';   // opts.bare (round 5): a card's crop on the page carries neither
    var fc = forced_patterns(c);
    var defs = c._defs.length || fc.defs ? '<defs>' + c._defs.join('') + fc.defs + '</defs>' : '';
    var svg = '<svg xmlns="http://www.w3.org/2000/svg" class="oac-svg' + (fc.defs ? ' oac-u-' + c.uid : '') + '" viewBox="0 0 ' + width + ' ' + h + '" width="' + width + '" height="' + h + '"' +
      ' role="img" data-oa-form="' + esc(spec.form) + '" data-oa-width="' + width + '"' + (opts.label_id ? ' aria-labelledby="' + esc(opts.label_id) + '"' : '') + '>' +
      title + desc + fc.style + defs + c._els.join('') + '</svg>';
    return { svg: svg, width: width, height: h, texts: c.texts, marks: c.marks, leaders: c.leaders, ink: c.ink, keys: c.keys || [], cells: c.cells, warnings: c.warnings, guard: guard, phone: c.phone,
      bands: c.bands || [], interval: def.interval || false, margins_in_words: !!c._ivw,
      arrangement: c._arr || (c.phone ? 'phone' : 'desk'),
      fc: K.FC, fc_on_dark: K.FC_ON_DARK };
  };

  // ------------------------------------------------------------------------------------------------------------
  // Forced colors (D3-94): each color role's paint in the reader's system colors. Solid roles take CanvasText, GrayText,
  // Canvas (with a CanvasText outline) or Highlight in kit.css; the steps between take a hatch in one of them, which each
  // drawing carries in its own defs, so a scale's steps stay apart. Text takes CanvasText on a Canvas halo, and text set on
  // a dark fill takes Canvas on a CanvasText halo. checks.js reads this table to fail any label in the ink of its ground.
  // ------------------------------------------------------------------------------------------------------------
  K.FC = {
    subject: 'CanvasText', party: 'CanvasText', 'chip-fill': 'CanvasText', baseline: 'CanvasText', label: 'CanvasText', leader: 'GrayText',
    point: 'Highlight', context: 'GrayText', secondary: 'GrayText', gridline: 'GrayText', ghost: 'GrayText',
    surface: 'Canvas', band: 'Canvas', track: 'Canvas', land: 'Canvas', 'light-fill': 'Canvas', 'sequential-outline': 'CanvasText',
    'seq-1': 'Canvas', 'seq-2': 'hatch', 'seq-3': 'GrayText', 'seq-4': 'dense', 'seq-5': 'CanvasText',
    'div-1': 'CanvasText', 'div-2': 'hatch', 'div-3': 'Canvas', 'div-4': 'hatch-gray', 'div-5': 'GrayText',
    'mag-1': 'Canvas', 'mag-2': 'hatch', 'mag-3': 'GrayText', 'mag-4': 'CanvasText',
    'cat-1': 'CanvasText', 'cat-2': 'GrayText', 'cat-3': 'dense', 'cat-4': 'hatch', none: 'Canvas'
  };
  // text inks: these set text on a dark fill, so they take Canvas in forced colors
  // round 3: a dark step's label ink (sequential 4 and 5, magnitude 4, diverging 1) sets words on a dark fill too
  K.FC_ON_DARK = ['label-on-subject', 'on-cat-1', 'on-cat-2', 'on-cat-3', 'chip-label', 'on-seq-4', 'on-seq-5', 'on-mag-4', 'on-div-1'];
  ['seq-1', 'seq-2', 'seq-3', 'mag-1', 'mag-2', 'div-2', 'div-3', 'div-4'].forEach(function (r) { K.FC['on-' + r] = 'CanvasText'; });
  ['seq-4', 'seq-5', 'mag-3', 'mag-4', 'div-1', 'div-5'].forEach(function (r) { K.FC['on-' + r] = 'Canvas'; });
  var FC_PATTERN = { hatch: [6, 1, 'CanvasText'], dense: [3, 1.5, 'CanvasText'], 'hatch-gray': [6, 1.5, 'GrayText'] };
  function forced_patterns(c) {
    var body = c._els.join(''), used = {}, rules = [], defs = '';
    Object.keys(K.FC).forEach(function (role) {
      var kind = K.FC[role];
      if (!FC_PATTERN[kind] || body.indexOf('oac-f-' + role + '"') < 0 && body.indexOf('oac-f-' + role + ' ') < 0) return;
      used[kind] = true;
      rules.push('.oac-svg.oac-u-' + c.uid + ' .oac-f-' + role + ':not(.oac-t){fill:url(#' + c.uid + '-fc-' + kind + ')}');
    });
    Object.keys(used).forEach(function (kind) {
      var p = FC_PATTERN[kind];
      defs += '<pattern id="' + c.uid + '-fc-' + kind + '" width="' + p[0] + '" height="' + p[0] + '" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">' +
        '<rect width="' + p[0] + '" height="' + p[0] + '" class="oac-fc-bg"/><line x1="0" y1="0" x2="0" y2="' + p[0] + '" class="oac-fc-' + (p[2] === 'GrayText' ? 'gray' : 'ink') + '" stroke-width="' + p[1] + '"/></pattern>';
    });
    return { defs: defs, style: rules.length ? '<style>@media (forced-colors:active){' + rules.join('') + '}</style>' : '' };
  }

  // ------------------------------------------------------------------------------------------------------------
  // The layout guard: every text inside the artboard, no two texts overlapping, nothing under 13 px
  // ------------------------------------------------------------------------------------------------------------
  K.MIN_TEXT = 13;
  K.CARD_MIN_TEXT = 36;
  K.guard = function (c, width, height) {
    var out = [], pad = 1;
    var tx = c.texts;
    for (var i = 0; i < tx.length; i++) {
      var a = tx[i];
      if (a.size < (c.min_text || K.MIN_TEXT) - 1e-6) out.push('text under ' + (c.min_text ? c.min_text + ' px on a card (13 px in a feed)' : '13 px') + ' (' + a.size + ' px): "' + a.words.slice(0, 40) + '"');
      var top = a.top !== undefined ? a.top : a.y, bot = a.bottom !== undefined ? a.bottom : a.y + a.h;
      if (a.x < -0.5 || a.x + a.w > width + 0.5 || top < -0.5 || bot > height + 0.5)
        out.push('text outside the artboard: "' + a.words.slice(0, 40) + '" at ' + r1(a.x) + ',' + r1(a.y) + ' (' + r1(a.w) + ' wide; artboard ' + width + ' by ' + height + ')');
      for (var j = i + 1; j < tx.length; j++) {
        var b = tx[j];
        if (a.overlap_ok || b.overlap_ok) continue;
        if (a.x + pad < b.x + b.w && b.x + pad < a.x + a.w && a.y + pad < b.y + b.h && b.y + pad < a.y + a.h)
          out.push('texts overlap: "' + a.words.slice(0, 30) + '" and "' + b.words.slice(0, 30) + '"');
      }
    }
    // R3-5 (round 3): a link between nodes never runs under a word: one drawn after the word, or before a word set with no
    // halo or knockout, fails (K.parts.link draws links to the edges of their nodes; K.parts.clear_label sets words on one)
    var links = (c.ink || []).filter(function (b) { return b.link; }), seen = {};
    if (links.length) tx.forEach(function (t) {
      if (t.overlap_ok) return;
      K.crossed_by(c.ink, t, function (b) { return b.link && (b.seq > t.seq || !t.halo); }).forEach(function () {
        if (seen[t.words]) return;
        seen[t.words] = 1;
        out.push('a link crosses "' + t.words.slice(0, 30) + '"; draw links before the words and route them round, or set the words on the link with K.parts.clear_label');
      });
    });
    // a leader may end at its own label but never run through one (D3-93)
    (c.leaders || []).forEach(function (l) {
      tx.forEach(function (b) {
        var x0 = b.x + 1.5, x1 = b.x + b.w - 1.5, y0 = b.y + 1.5, y1 = b.y + b.h - 1.5;
        if (x1 <= x0 || y1 <= y0) return;
        if (K.leader_crosses(l, b)) out.push('a leader line crosses "' + b.words.slice(0, 30) + '"');
      });
    });
    return out;
  };
  K.seg_hits_box = seg_hits_box;
  // the guard's own test of a leader through a label, which K.parts.place_labels asks before it picks a place (RB-G3)
  K.leader_crosses = function (l, b) {
    var x0 = b.x + 1.5, x1 = b.x + b.w - 1.5, y0 = b.y + 1.5, y1 = b.y + b.h - 1.5;
    if (x1 <= x0 || y1 <= y0) return false;
    var near = function (x, y) { return x > b.x - 4 && x < b.x + b.w + 4 && y > b.y - 4 && y < b.y + b.h + 4; };
    if (near(l.x1, l.y1) || near(l.x2, l.y2)) return false;
    return seg_hits_box(l.x1, l.y1, l.x2, l.y2, x0, y0, x1, y1);
  };
  function seg_hits_box(ax, ay, bx, by, x0, y0, x1, y1) {
    // Liang-Barsky: does the segment from (ax, ay) to (bx, by) enter the box?
    var t0 = 0, t1 = 1, dx = bx - ax, dy = by - ay, p = [-dx, dx, -dy, dy], q = [ax - x0, x1 - ax, ay - y0, y1 - ay];
    for (var i = 0; i < 4; i++) {
      if (p[i] === 0) { if (q[i] < 0) return false; continue; }
      var r = q[i] / p[i];
      if (p[i] < 0) { if (r > t1) return false; if (r > t0) t0 = r; } else { if (r < t0) return false; if (r < t1) t1 = r; }
    }
    return t0 <= t1;
  }

  // ------------------------------------------------------------------------------------------------------------
  // Words: the shared words (the figure, the table equivalent and atlas IDs in chips are in kit-build.js)
  // ------------------------------------------------------------------------------------------------------------
  K.words = K.words || {};
  function word(opts, k) {
    var w = (opts && opts.words) || K.words;
    if (k in w) return w[k];
    if (K.WORDS && k in K.WORDS) return K.WORDS[k];
    throw new Error('OAChart: words.json has no "' + k + '"; add it there and to K.WORDS in kit-build.js');
  }
  // the shared words for a form: words.json's, through the same fallback the figure uses (editor's read, K1)
  K.word = function (k) { return word(null, k); };
  var MONTH_N = {};
  MONTHS.forEach(function (m, i) { MONTH_N[m] = i + 1; MONTH_N[m.slice(0, 3)] = i + 1; });
  K.unformat = function (text, col) {
    // the raw value a printed cell stands for, or undefined when the words cannot say it exactly
    var t = String(text == null ? '' : text).trim(), f = String(col.format || 'text'), m;
    if (t === '') return null;
    if (col.words) {
      var hits = Object.keys(col.words).filter(function (k) { return col.words[k] === t; });
      return hits.length === 1 ? hits[0] : undefined;
    }
    var lm = /^lead(?::\d+)?$/.exec(f);
    if (lm) {
      var w = col.lead || {};
      if (w.zero && t === w.zero) return '0';
      var mm = /^(.*) \+([\d,.]+)$/.exec(t);
      if (!mm) return undefined;
      var v = parseFloat(mm[2].replace(/,/g, ''));
      return mm[1] === w.positive ? String(v) : mm[1] === w.negative ? String(-v) : undefined;
    }
    var base = f.replace(/:\d+$/, '');
    if (base === 'fraction-percent') {
      var nfp = t.replace(/[%\s]/g, '').replace(MINUS, '-');
      return /^-?\d+(\.\d+)?$/.test(nfp) ? String(dround(parseFloat(nfp) / 100, 12)) : undefined;
    }
    if (/^(integer|number|percent|signed|points|dollars|signed-dollars)$/.test(base)) {
      var n = t.replace(/[+,%$\s]/g, '').replace(MINUS, '-');
      return /^-?\d+(\.\d+)?$/.test(n) ? n : undefined;
    }
    if (base === 'billions' || base === 'billions-value') {
      var nb = t.replace(/ billion$/, '').replace(/[,\s]/g, '').replace(MINUS, '-');
      return /^-?\d+(\.\d+)?$/.test(nb) ? String(parseFloat(nb) * 1e9) : undefined;
    }
    if (base === 'billions-from-millions' || base === 'billions-value-from-millions') {
      var nf = t.replace(/ billion$/, '').replace(/[,\s]/g, '').replace(MINUS, '-');
      return /^-?\d+(\.\d+)?$/.test(nf) ? String(Math.round(parseFloat(nf) * 1e3 * 1e6) / 1e6) : undefined;
    }
    if (base === 'millions' || base === 'millions-value') {
      var nm = t.replace(/ million$/, '').replace(/[,\s]/g, '').replace(MINUS, '-');
      return /^-?\d+(\.\d+)?$/.test(nm) ? String(Math.round(parseFloat(nm) * 1e6 * 1e6) / 1e6) : undefined;
    }
    if (base === 'thousands' || base === 'signed-thousands') {
      var n2 = t.replace(/[+,\s]/g, '').replace(MINUS, '-');
      return /^-?\d+$/.test(n2) ? String(parseFloat(n2) / 1000) : undefined;
    }
    if (base === 'month' && (m = /^([A-Z][a-z]+) (\d{4})$/.exec(t)) && MONTH_N[m[1]]) return m[2] + '-' + String(MONTH_N[m[1]]).padStart(2, '0');
    if (base === 'date' && (m = /^([A-Z][a-z]+) (\d{1,2}), (\d{4})$/.exec(t)) && MONTH_N[m[1]]) return m[3] + '-' + String(MONTH_N[m[1]]).padStart(2, '0') + '-' + String(m[2]).padStart(2, '0');
    if (base === 'year' && /^\d{4}$/.test(t)) return t;
    if (base === 'text') return t;
    return undefined;
  };
  // D3-519 (round 1 fix pass): a spec's "typography" sets the guide's apostrophes and quotation marks, and any exact
  // replacements it lists, in every word the figure prints from the data (the drawing, text cells of the table); the data
  // itself, and so the CSV export, keeps the words as stored. Each replacement must leave nothing it would replace again,
  // so the page, which reads its rows back from the printed table, draws what Node draws.
  // {"typography": {"curl_quotes": true, "replace": [["Act,2026", "Act, 2026"]]}}
  function curl(t) {
    t = t.replace(/(^|[\s(\[{\u2013\u2014-])'/g, '$1\u2018').replace(/'/g, '\u2019');
    return t.replace(/(^|[\s(\[{\u2013\u2014-])"/g, '$1\u201c').replace(/"/g, '\u201d');
  }
  // BC S12 (round 2 fix pass): typography.nbsp holds a date's month and day together ("November 3, 2026") and a span of
  // years with its "to" ("2017 to 2022"), with no-break spaces, in printed words only; a second pass changes nothing
  var MONTH_ALT = 'January|February|March|April|May|June|July|August|September|October|November|December';
  K.nbsp = function (t) {
    return String(t).replace(new RegExp('\\b(' + MONTH_ALT + ') (\\d{1,2})\\b', 'g'), '$1\u00a0$2')
      .replace(/\b((?:1[89]|20)\d{2}) (to|through) ((?:1[89]|20)\d{2})\b/g, '$1\u00a0$2\u00a0$3');
  };
  K.typeset = function (spec, words) {
    var ty = spec && spec.typography;
    if (!ty || words === null || words === undefined) return words;
    var t = String(words);
    (ty.replace || []).forEach(function (pr) { if (pr && pr[0]) t = t.split(String(pr[0])).join(String(pr[1])); });
    // IM-E1 (round 4): a held phrase never breaks in a drawing (K.wrap breaks at spaces only); HTML holds it in .oac-nw
    (ty.hold || []).forEach(function (p) { t = t.split(p).join(p.replace(/ /g, ' ')); });
    if (ty.nbsp) t = K.nbsp(t);
    return ty.curl_quotes ? curl(t) : t;
  };
  // ------------------------------------------------------------------------------------------------------------
  // The data island, carried compressed (DR-238): a figure's island is its drawing spec and the columns its table lacks,
  // deflated (RFC 1951, raw) and written as base64 in <script type="text/plain" data-oa-chart-data="deflate">. Only the
  // script reads it, so a reader with scripts off loses nothing: the words and the table equivalent stay live text. The
  // inflater is synchronous and needs no browser feature (DecompressionStream is asynchronous, so print could outrun it).
  // An island written as JSON (data-oa-chart-data with no value, type application/json) still reads as before.
  // ------------------------------------------------------------------------------------------------------------
  var LBASE = [], LEXT = [], DBASE = [], DEXT = [], FIXED = null;
  (function () {
    // RFC 1951's length and distance bases, and how many extra bits each code reads
    var i, b;
    for (i = 0, b = 3; i < 28; i++) { LEXT[i] = i < 8 ? 0 : (i >> 2) - 1; LBASE[i] = b; b += 1 << LEXT[i]; }
    LBASE[28] = 258; LEXT[28] = 0;
    for (i = 0, b = 1; i < 30; i++) { DEXT[i] = i < 4 ? 0 : (i >> 1) - 1; DBASE[i] = b; b += 1 << DEXT[i]; }
  })();
  function bad() { throw new Error('inflate: the data is not deflate'); }
  function huff(len, off, n) {
    // canonical Huffman decoding table: how many codes of each length, and the symbols in code order
    var count = [], sym = [], offs = [0, 0], i;
    for (i = 0; i < 16; i++) count[i] = 0;
    for (i = 0; i < n; i++) count[len[off + i]]++;
    for (i = 1; i < 15; i++) offs[i + 1] = offs[i] + count[i];
    for (i = 0; i < n; i++) if (len[off + i]) sym[offs[len[off + i]]++] = i;
    return { count: count, sym: sym };
  }
  K.inflate = function (src) {
    // raw DEFLATE bytes in, the bytes they hold out (an array of numbers); throws on data that is not deflate
    var pos = 0, buf = 0, cnt = 0, out = [], last, type, i;
    function bits(n) {
      var v = buf;
      while (cnt < n) { if (pos >= src.length) bad(); v |= src[pos++] << cnt; cnt += 8; }
      buf = v >>> n;
      cnt -= n;
      return v & ((1 << n) - 1);
    }
    function decode(h) {
      var code = 0, first = 0, index = 0, len, c;
      for (len = 1; len < 16; len++) {
        code |= bits(1);
        c = h.count[len];
        if (code - c < first) return h.sym[index + (code - first)];
        index += c;
        first = (first + c) << 1;
        code <<= 1;
      }
      bad();
    }
    function codes(lc, dc) {
      var sym, len, dist;
      while ((sym = decode(lc)) !== 256) {
        if (sym < 256) { out.push(sym); continue; }
        if ((sym -= 257) > 28) bad();
        len = LBASE[sym] + bits(LEXT[sym]);
        if ((sym = decode(dc)) > 29) bad();
        dist = DBASE[sym] + bits(DEXT[sym]);
        if (dist > out.length) bad();
        while (len-- > 0) out.push(out[out.length - dist]);
      }
    }
    function dynamic() {
      var nlen = bits(5) + 257, nd = bits(5) + 1, nc = bits(4) + 4, cl = [], lens = [], j, sym, rep, prev, h;
      var order = [16, 17, 18, 0, 8, 7, 9, 6, 10, 5, 11, 4, 12, 3, 13, 2, 14, 1, 15];
      if (nlen > 286 || nd > 30) bad();
      for (j = 0; j < 19; j++) cl[order[j]] = j < nc ? bits(3) : 0;
      h = huff(cl, 0, 19);
      for (j = 0; j < nlen + nd;) {
        sym = decode(h);
        if (sym < 16) { lens[j++] = sym; continue; }
        prev = 0;
        if (sym === 16) { if (!j) bad(); prev = lens[j - 1]; rep = 3 + bits(2); }
        else rep = sym === 17 ? 3 + bits(3) : 11 + bits(7);
        if (j + rep > nlen + nd) bad();
        while (rep-- > 0) lens[j++] = prev;
      }
      codes(huff(lens, 0, nlen), huff(lens, nlen, nd));
    }
    do {
      last = bits(1);
      type = bits(2);
      if (type === 0) {
        // a stored block: the rest of this byte is dropped, then its length, the length's complement and the bytes
        buf = cnt = 0;
        if (pos + 4 > src.length) bad();
        var n = src[pos] | src[pos + 1] << 8;
        if (n !== (~(src[pos + 2] | src[pos + 3] << 8) & 0xffff) || (pos += 4) + n > src.length) bad();
        while (n-- > 0) out.push(src[pos++]);
      } else if (type === 1) {
        if (!FIXED) {
          var fl = [], fd = [];
          for (i = 0; i < 288; i++) fl[i] = i < 144 ? 8 : i < 256 ? 9 : i < 280 ? 7 : 8;
          for (i = 0; i < 30; i++) fd[i] = 5;
          FIXED = [huff(fl, 0, 288), huff(fd, 0, 30)];
        }
        codes(FIXED[0], FIXED[1]);
      } else if (type === 2) dynamic();
      else bad();
    } while (!last);
    return out;
  };
  function unbase64(s) {
    var bin = root.atob(s.replace(/\s+/g, '')), b = [];
    for (var i = 0; i < bin.length; i++) b.push(bin.charCodeAt(i));
    return b;
  }
  K.island_text = function (text, encoding) {
    // an island's text as JSON text: as written, or inflated from deflate and base64
    return encoding === 'deflate' ? new root.TextDecoder('utf-8').decode(new Uint8Array(K.inflate(unbase64(text)))) : text;
  };
  K.island = function (el) {
    // a figure's data island, read from its script element
    return JSON.parse(K.island_text(el.textContent, el.getAttribute('data-oa-chart-data')));
  };
  K.rows_from_table = function (table, spec, isl) {
    // the rows a chart draws, read back from its own table equivalent and the island's extra columns (method load-table)
    var tb = spec.table || {}, out = [];
    // R3-3: a grouped table holds no row of its own; the island carries every row the drawing reads
    // the geoids, read from the map layer the island names (R3-3)
    var geo_ids = function (rs) {
      if (!isl.geo_key || !K.geo) return rs;
      var gids = K.geo(isl.geo_key.layer).ids;
      if (!rs.length) rs = gids.map(function () { return {}; });
      rs.forEach(function (o, i) { o[isl.geo_key.field] = gids[i]; });
      return rs;
    };
    if (tb.group) return K.type_rows(geo_ids(isl.csv ? K.parse_csv(isl.csv) : []), isl.columns);
    // IM-E6 item 2 (round 4): a held phrase prints with no-break spaces (typography.hold); read back, it takes its stored
    // spaces again, so a form that wraps the stored words draws on the page as in Node
    var held = ((spec.typography || {}).hold || []), cell_raw = function (el, col) {
      var t = el.textContent;
      held.forEach(function (p) { t = t.split(p.replace(/ /g, '\u00a0')).join(p); });
      return el.hasAttribute('data-v') ? el.getAttribute('data-v') : K.unformat(t, col);
    };
    if (tb.pivot) {
      var pv = tb.pivot, rc = (tb.columns || [])[0] || { format: 'text' }, rows_by = [].concat(pv.row);
      var heads = Array.prototype.slice.call(table.querySelectorAll('thead th')).slice(1).map(function (th) {
        if (th.hasAttribute('data-v')) return th.getAttribute('data-v');
        var lab = th.textContent, inv = null;
        Object.keys(pv.labels || {}).forEach(function (k) { if (pv.labels[k] === lab) inv = k; });
        return inv !== null ? inv : lab;
      });
      Array.prototype.forEach.call(table.querySelectorAll('tbody tr'), function (tr) {
        var th = tr.querySelector('th'), keyv;
        if (rows_by.length > 1) keyv = JSON.parse(th.getAttribute('data-v'));
        else keyv = [cell_raw(th, { field: rows_by[0], format: rc.format })];
        Array.prototype.forEach.call(tr.querySelectorAll('td'), function (td, j) {
          if (td.hasAttribute('data-x') || (td.textContent === '' && !td.hasAttribute('data-v') && !td.hasAttribute('data-n'))) return;
          var o = {};
          rows_by.forEach(function (k, i) { o[k] = keyv[i] === null ? null : String(keyv[i]); });
          o[pv.column] = heads[j];
          o[pv.value] = cell_raw(td, { field: pv.value, format: pv.format });
          out.push(o);
        });
      });
    } else {
      var cols = tb.columns || [];
      Array.prototype.forEach.call(table.querySelectorAll('tbody tr'), function (tr) {
        var o = {}, cells = tr.children;
        cols.forEach(function (col, i) { o[col.field] = cell_raw(cells[i], col); });
        out.push(o);
      });
    }
    if (isl.carry) {
      // the compact carrier: each carried field's values, in the table's cell order
      Object.keys(isl.carry).forEach(function (f) {
        var vals = isl.carry[f].split(',');
        out.forEach(function (o, i) { o[f] = vals[i] === '' || vals[i] === undefined ? null : vals[i]; });
      });
    }
    if (isl.csv) {
      var extra = K.parse_csv(isl.csv);
      out.forEach(function (o, i) { var e = extra[i] || {}; for (var k in e) o[k] = e[k]; });
    }
    return K.type_rows(geo_ids(out), isl.columns);
  };
  var PHONE_VIEW_PX = 358;
  // round 3 fix pass (call 10, weight): the builder's half of the kit (the figure's HTML, its table, the plain page's
  // render, tokens from CSS and the words' fallback) lives in kit-build.js, which Node and a plain page load after this
  // file and the guide's page never carries; these are the helpers it shares
  K._p = { esc: esc, word: word, fixed: fixed, group: group, signed: signed, PHONE_VIEW_PX: PHONE_VIEW_PX };
  K.lookup = function (fig) {
    // wire a figure's lookup from its own markup: no island is needed, so the controls work as soon as the page loads
    var box = fig.querySelector('[data-oa-lookup-controls]');
    if (!box || box._oac_wired) return;
    box._oac_wired = true;
    var q = box.querySelector('.oac-lk-input'), clear = box.querySelector('.oac-lk-clear'), toggle = box.querySelector('.oac-lk-toggle');
    var unfilter = box.querySelector('.oac-lk-unfilter'), count = box.querySelector('.oac-lk-count'), status = box.querySelector('.oac-lk-status');
    var groups = Array.prototype.slice.call(box.querySelectorAll('.oac-lk-chips')), chips = Array.prototype.slice.call(box.querySelectorAll('.oac-lk-chip'));
    var rows = Array.prototype.slice.call(fig.querySelectorAll('table.oac-table tbody tr'));
    var norm = function (t) { return String(t || '').replace(/\s+/g, ' ').trim().toLowerCase(); };
    var on = function (c) { return c.getAttribute('aria-pressed') === 'true'; };
    function run() {
      var term = q ? norm(q.value) : '', n = 0;
      rows.forEach(function (tr) {
        var hit = !term || norm(tr.textContent + ' ' + (tr.getAttribute('data-oa-find') || '')).indexOf(term) >= 0;
        hit = hit && groups.every(function (g) {
          var want = Array.prototype.filter.call(g.querySelectorAll('.oac-lk-chip'), on).map(function (c) { return norm(c.textContent); });
          var cell = tr.children[+g.getAttribute('data-col')];
          return !want.length || (cell && want.indexOf(norm(cell.textContent)) >= 0);
        });
        tr.hidden = !hit;
        if (hit) n++;
      });
      var k = chips.filter(on).length;
      if (count) count.textContent = count.getAttribute('data-words').replace('{n}', k);
      if (unfilter) unfilter.hidden = !k;
      if (clear) clear.hidden = !(q && q.value);
      status.textContent = status.getAttribute('data-words').replace('{n}', n).replace('{total}', rows.length).replace('{noun}', status.getAttribute('data-noun')) +
        (n ? '' : '. ' + status.getAttribute('data-none'));
    }
    if (q) {
      q.addEventListener('input', run);
      q.addEventListener('keydown', function (e) { if (e.key === 'Escape' && q.value) { e.preventDefault(); q.value = ''; run(); q.focus(); } });
    }
    if (clear) clear.addEventListener('click', function () { q.value = ''; run(); q.focus(); });
    if (toggle) toggle.addEventListener('click', function () {
      var open = toggle.getAttribute('aria-expanded') !== 'true';
      toggle.setAttribute('aria-expanded', String(open));
      var sheet = fig.ownerDocument.getElementById(toggle.getAttribute('aria-controls'));
      if (sheet) sheet.hidden = !open;
    });
    chips.forEach(function (c) { c.addEventListener('click', function () { c.setAttribute('aria-pressed', String(!on(c))); run(); }); });
    if (unfilter) unfilter.addEventListener('click', function () { chips.forEach(function (c) { c.setAttribute('aria-pressed', 'false'); }); run(); toggle.focus(); });
    // access S7: Escape inside the filter sheet closes it and returns focus to Filters, as chapter 18's filter bar does
    var sheet = toggle ? fig.ownerDocument.getElementById(toggle.getAttribute('aria-controls')) : null;
    if (sheet) sheet.addEventListener('keydown', function (e) {
      if (e.key !== 'Escape' || sheet.hidden) return;
      e.preventDefault(); e.stopPropagation();
      sheet.hidden = true; toggle.setAttribute('aria-expanded', 'false'); toggle.focus();
    });
    // CD AM1, BC S9: where the script runs, the live lookup takes the still list's place: the drawing (the export and the
    // scripts-off view, Rule 14.13) hides, and the controls with the one table and its one count sit where it stood. Print
    // shows the still list again, then every row.
    var art = fig.querySelector('.oac-art[data-oa-art]'), eqd = fig.querySelector('details.oac-eq');
    // a page that exports the still drawing (the kit's build page) sets OAChart.lookup_in_place = false before the figures wire
    if (K.lookup_in_place !== false && art && art.parentNode) {
      art.parentNode.insertBefore(box, art.nextSibling);
      if (eqd) { box.parentNode.insertBefore(eqd, box.nextSibling); eqd.setAttribute('open', ''); }
      art.hidden = true;
      fig.setAttribute('data-oa-live', '');
    }
    box.hidden = false;
    run();
  };

  // ------------------------------------------------------------------------------------------------------------
  // In a browser: draw into a figure, and again when its width changes
  // ------------------------------------------------------------------------------------------------------------
  K.mount = function (fig, spec, rows, opts) {
    var extra = (opts && opts.extra) || {};
    opts = opts || {};
    var art = fig.querySelector('[data-oa-art]');
    if (!art) return null;
    var cs = root.getComputedStyle(fig), t = token_reader(function (n) { return cs.getPropertyValue(n); });
    var ground = opts.ground || (fig.closest && fig.closest('.oa-surface-charcoal') ? 'charcoal' : 'newsprint');
    // R4-4 (round 4): a card draws each crop once at its true size; the page's CSS shows it at the column's width
    if (spec.card && spec.card.crops) {
      spec.card.crops.forEach(function (cr, ci) {
        var doc = fig.ownerDocument || root.document;
        var a = fig.querySelector('[data-oa-crop="' + cr[0] + 'x' + cr[1] + '"]'), lid = fig.id && doc.getElementById(fig.id + '-alt') ? fig.id + '-alt' : null;
        if (!a || a.querySelector('svg.oac-svg')) return;
        // the accessibility lead's request 1 (round 5, carried): the first crop is named by the alt, every later crop by its
        // size line alone, and no crop carries the card's title or alt as a description, so the alt is heard once here
        var sid = fig.id ? fig.id + '-crop-' + cr[0] + 'x' + cr[1] : null;
        if (ci > 0 && sid && doc.getElementById(sid)) lid = sid;
        var r = K.draw(spec, rows, { width: cr[0], crop: cr, ground: ground, t: t, extra: extra, uid: (fig.id || 'oac') + '-c' + cr[1] + '-' + cr[0], label_id: lid, bare: true });
        a.insertAdjacentHTML('beforeend', r.svg);
        if (lid) (fig.ownerDocument || root.document).getElementById(lid).hidden = true;
        if (r.guard.length || r.warnings.length) fig.setAttribute('data-oa-warnings', String(r.guard.length + r.warnings.length));
      });
      fig.setAttribute('data-oa-drawn', 'card');
      K.frame(fig);
      return { redraw: function () {}, result: function () { return null; } };
    }
    var last = -1, result = null, staged = !!(spec.stage || spec.stage_min);
    function draw() {
      var cw = art.clientWidth || fig.clientWidth, w = K.artboard(spec, t, cw), w0 = w;
      // C-M2: a staged drawing keeps its one width and the frame scrolls sideways; a phone column draws the phone form
      // DR-261: a floor (stage_min) stages the drawing only where the column is narrower than the floor
      if (staged) {
        w = K.draw_width(spec, w);
        if (spec.stage ? w === Math.round(+spec.stage) : w > w0) art.setAttribute('data-oa-stage', String(w)); else art.removeAttribute('data-oa-stage');
      }
      if (w === last) { if (staged) stage_stop(); return; }
      last = w;
      // the drawing takes its name from the figure's printed title; a plate that prints no title (chapter 13's) names it
      // by its description, so the name never points at an element that is not there
      var doc = fig.ownerDocument || root.document;
      var has_t = fig.id && doc.getElementById(fig.id + '-t'), has_alt = fig.id && doc.getElementById(fig.id + '-alt');
      // the description names the drawing and the printed title stays in the reading order, so each is heard once
      // (access S1); a figure with neither names it from the spec
      var lid = has_alt ? fig.id + '-alt' : (has_t ? fig.id + '-t' : null);
      result = K.draw(spec, rows, { width: w, ground: ground, t: t, extra: extra, uid: (fig.id || 'oac') + '-' + w, label_id: lid });
      var old = art.querySelector('svg.oac-svg');
      if (old) old.remove();
      art.insertAdjacentHTML('beforeend', result.svg);
      var svg = art.querySelector('svg.oac-svg');
      if (svg && !lid) svg.setAttribute('aria-label', String(spec.alt || spec.title || ''));
      if (has_alt) has_alt.hidden = true;
      fig.setAttribute('data-oa-drawn', String(w));
      // RS-S3: where this drawing is already the phone form, the desk's phone drawing beside it says nothing new
      if (result.arrangement === 'phone') fig.setAttribute('data-oa-phone-form', ''); else fig.removeAttribute('data-oa-phone-form');
      // AX S1 (round 2 fix pass): a clean redraw clears the count a narrower or wider drawing left
      if (result.guard.length || result.warnings.length) fig.setAttribute('data-oa-warnings', String(result.guard.length + result.warnings.length));
      else fig.removeAttribute('data-oa-warnings');
      if (staged) stage_stop();
    }
    // C-M2: a staged drawing wider than its column takes a tab stop and a name, so a keyboard can scroll it (as the table's
    // frame does); it gives them up when it fits
    // RS-1 (second pass): while it scrolls, a hint above the drawing says so before a reader scrolls (the frame's name says
    // the same to a screen reader, so the hint is hidden from it), and the frame shows its edges and a scroll bar (kit.css)
    function stage_stop() {
      var hint = art.previousElementSibling && art.previousElementSibling.classList.contains('oac-stage-hint') ? art.previousElementSibling : null;
      // round 4 (the cartographer's 1,103 px window): a drawing at most 1 px wider than its column shrinks to it, never a 1 px
      // scroll with no tab stop or hint; the overflow is read from the drawn width, so the shrink does not undo itself
      var over = art.hasAttribute('data-oa-stage') ? +art.getAttribute('data-oa-stage') - art.clientWidth : 0;
      if (over > 0 && over <= 1) art.setAttribute('data-oa-stage-fit', ''); else art.removeAttribute('data-oa-stage-fit');
      if (over > 1) {
        art.setAttribute('tabindex', '0'); art.setAttribute('role', 'group'); art.setAttribute('data-oa-scrolls', '');
        art.setAttribute('aria-label', word(opts, 'stage_scroll').replace('{w}', art.getAttribute('data-oa-stage')));
        if (!hint) { art.insertAdjacentHTML('beforebegin', '<p class="oac-stage-hint" aria-hidden="true"></p>'); hint = art.previousElementSibling; }
        hint.textContent = word(opts, 'stage_hint');
        hint.hidden = false;
      } else {
        art.removeAttribute('tabindex'); art.removeAttribute('role'); art.removeAttribute('aria-label'); art.removeAttribute('data-oa-scrolls');
        if (hint) hint.hidden = true;
      }
    }
    draw();
    // the phone drawing at its fixed width, once (D3-487); the figure's description and table carry its data, so it is
    // hidden from assistive technology
    var pv = fig.querySelector('[data-oa-art-phone]');
    if (pv && !pv.querySelector('svg.oac-svg')) {
      var pn = +pv.getAttribute('data-oa-rows') || 0;
      var pr = K.draw(spec, pn ? rows.slice(0, pn) : rows, { width: +pv.getAttribute('data-oa-art-phone') || PHONE_VIEW_PX, ground: ground, t: t, extra: extra, all_rows: pn ? rows : null, uid: (fig.id || 'oac') + '-phone' });
      pv.insertAdjacentHTML('beforeend', pr.svg.replace('<svg ', '<svg aria-hidden="true" ').replace(/<title>[\s\S]*?<\/title>|<desc>[\s\S]*?<\/desc>/g, ''));
    }
    if (root.ResizeObserver) new root.ResizeObserver(function () { draw(); }).observe(art);
    K.frame(fig);
    return { redraw: function () { last = -1; draw(); }, result: function () { return result; } };
  };
  // The table's scroll frame (contract C5; axe scrollable-region-focusable): a frame whose table runs wider than it takes a
  // tab stop, and gives it up when the table fits. Wired for every figure at load, drawn or not, and checked whenever the
  // table opens or the frame changes size, so an open table (a lookup's, or one a reader or a check opens before the
  // drawing comes) never scrolls without one. The frame carries its name (aria-label) from the build.
  K.frame = function (fig) {
    var tw = fig.querySelector('.oac-tw[role="group"]'), eq = fig.querySelector('details.oac-eq');
    if (!tw || tw._oac_frame) return;
    tw._oac_frame = true;
    var stop = function () { if (tw.scrollWidth > tw.clientWidth + 1) tw.setAttribute('tabindex', '0'); else tw.removeAttribute('tabindex'); };
    if (eq) eq.addEventListener('toggle', stop);
    if (root.ResizeObserver) new root.ResizeObserver(stop).observe(tw);
    else if (root.addEventListener) root.addEventListener('resize', stop);
    stop();
  };
  K.mount_all = function (scope, o) {
    // every figure with a JSON island: a script element of type application/json marked data-oa-chart-data. At load each
    // figure closes its table and hides its scripts-off words at once; the drawing comes as the figure nears the screen,
    // and every figure draws before the page prints (D3-97). o.now draws them all at once.
    var figs = (scope || root.document).querySelectorAll('figure.oac-fig'), lazy = [];
    var go = function (f) {
      if (f.getAttribute('data-oa-drawn') || f.getAttribute('data-oa-error') || f._oac_busy) return;
      var isl = f.querySelector('script[data-oa-chart-data]');
      if (!isl) return;
      f._oac_busy = true;
      try {
        var d = K.island(isl);
        var rows = d.mode === 'table' ? K.rows_from_table(f.querySelector('table.oac-table'), d.spec, d)
          : d.csv !== undefined ? K.type_rows(K.parse_csv(d.csv), d.columns) : K.type_rows(d.rows || [], d.columns);
        var extra = {};
        Object.keys(d.extra || {}).forEach(function (k) { extra[k] = K.type_rows(K.parse_csv(d.extra[k].csv), d.extra[k].columns); });
        K.mount(f, d.spec, rows, { words: d.words, extra: extra });
      } catch (e) {
        // a figure that cannot draw goes back to what a reader with scripts off sees: the description, the line that the
        // drawing needs scripts, and its table open, so nothing is lost but the drawing
        f.setAttribute('data-oa-error', String(e && e.message || e));
        f.removeAttribute('data-oa-js');
        var alt = f.querySelector('.oac-alt'), eq = f.querySelector('details.oac-eq');
        if (alt) alt.hidden = false;
        if (eq) eq.setAttribute('open', '');
      }
    };
    for (var i = 0; i < figs.length; i++) {
      var f = figs[i];
      // access N3: a static figure (oa-chart.mjs figure) has no island and no drawing to make, but its table's frame still
      // takes its tab stop when it scrolls
      if (f.hasAttribute('data-oa-static')) { K.frame(f); continue; }
      if (!f.querySelector('script[data-oa-chart-data]')) continue;
      f.setAttribute('data-oa-js', '');
      var eq = f.querySelector('details.oac-eq[open]');
      K.frame(f);
      if (f.hasAttribute('data-oa-lookup')) K.lookup(f);
      else if (eq && !f.getAttribute('data-oa-drawn')) eq.removeAttribute('open');
      lazy.push(f);
    }
    K._pending = (K._pending || []).concat(lazy);
    K._go = go;
    if (o && o.now || !root.IntersectionObserver) { lazy.forEach(go); return; }
    var io = new root.IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { io.unobserve(e.target); go(e.target); } });
    }, { rootMargin: '1200px 0px' });
    lazy.forEach(function (f) { io.observe(f); });
  };
  // Access S4 (second pass): a drawing taller than a printed page (9 in, 864 px) is one unbreakable box, which Chromium moves
  // whole to the next page, leaving its title alone. Before print, such a drawing prints as slices of up to SLICE_PX each,
  // cut in a gap between its words, every slice a copy of the drawing that shows one band of it; the first slice stays
  // under the title (kit.css), the drawing on screen is untouched, and after print the slices go.
  var SLICE_PX = 360, TALL_PX = 864;
  K.print_slices = function (doc) {
    Array.prototype.forEach.call(doc.querySelectorAll('figure.oac-fig .oac-art'), function (a) {
      var svg = a.querySelector(':scope > svg.oac-svg');
      if (!svg || a.querySelector(':scope > .oac-slices') || a.getBoundingClientRect().height <= TALL_PX) return;
      var vb = (svg.getAttribute('viewBox') || '').split(/[\s,]+/).map(Number), W = vb[2], H = vb[3];
      if (!(W > 0 && H > TALL_PX)) return;
      // the words' bands in the drawing's own units, so no cut runs through a line of words
      var sm = svg.getScreenCTM(), inv = sm && sm.inverse(), bands = [];
      Array.prototype.forEach.call(svg.querySelectorAll('text'), function (t) {
        var r = t.getBoundingClientRect();
        if (!r.height || !inv) return;
        var p0 = new DOMPoint(r.left, r.top).matrixTransform(inv), p1 = new DOMPoint(r.right, r.bottom).matrixTransform(inv);
        bands.push([Math.min(p0.y, p1.y) - 2, Math.max(p0.y, p1.y) + 2]);
      });
      var clear = function (y) { return !bands.some(function (b) { return y > b[0] && y < b[1]; }); };
      var cuts = [0], y = 0;
      while (H - y > SLICE_PX) {
        var cut = y + SLICE_PX;
        for (var c = y + SLICE_PX; c > y + SLICE_PX / 2; c--) if (clear(c)) { cut = c; break; }
        cuts.push(Math.round(cut));
        y = Math.round(cut);
      }
      cuts.push(H);
      var html = svg.outerHTML, ids = [], m, re = /\sid="([^"]+)"/g;
      while ((m = re.exec(html))) ids.push(m[1]);
      var box = doc.createElement('div');
      box.className = 'oac-slices';
      box.setAttribute('aria-hidden', 'true');
      for (var k = 0; k + 1 < cuts.length; k++) {
        var s = html;
        ids.forEach(function (id) { s = s.split('id="' + id + '"').join('id="' + id + '-p' + k + '"').split('#' + id + ')').join('#' + id + '-p' + k + ')').split('#' + id + '"').join('#' + id + '-p' + k + '"'); });
        box.insertAdjacentHTML('beforeend', s);
        var sl = box.lastElementChild, h = cuts[k + 1] - cuts[k];
        sl.setAttribute('viewBox', vb[0] + ' ' + (vb[1] + cuts[k]) + ' ' + W + ' ' + h);
        sl.setAttribute('height', String(h));
        sl.removeAttribute('aria-labelledby');
        sl.removeAttribute('role');
        sl.setAttribute('class', (sl.getAttribute('class') || '') + ' oac-slice');
        Array.prototype.forEach.call(sl.querySelectorAll('title, desc'), function (x) { x.remove(); });
      }
      a.appendChild(box);
      a.setAttribute('data-oa-sliced', String(cuts.length - 1));
    });
  };
  K.print_unslice = function (doc) {
    Array.prototype.forEach.call(doc.querySelectorAll('.oac-art[data-oa-sliced]'), function (a) {
      var box = a.querySelector(':scope > .oac-slices');
      if (box) box.remove();
      a.removeAttribute('data-oa-sliced');
    });
  };
  K.draw_all = function () {
    // every figure not yet drawn, at once: before print, and for checks that read every drawing
    (K._pending || []).forEach(function (f) { if (K._go) K._go(f); });
  };
  if (root.document && root.document.addEventListener) {
    var go = function () { K.mount_all(); };
    // before print every chart draws and every table opens, so paper carries both; after print the tables close again
    var opened = [];
    if (root.addEventListener) {
      root.addEventListener('beforeprint', function () {
        K.draw_all();
        K.print_slices(root.document);
        // round 4 (the component engineer's note): a second beforeprint before afterprint adds to the list, never replaces it
        opened = opened.concat(Array.prototype.slice.call(root.document.querySelectorAll('figure.oac-fig details.oac-eq:not([open])')));
        opened.forEach(function (d) { d.setAttribute('open', ''); });
      });
      root.addEventListener('afterprint', function () { opened.forEach(function (d) { d.removeAttribute('open'); }); opened = []; K.print_unslice(root.document); });
    }
    if (root.document.readyState === 'loading') root.document.addEventListener('DOMContentLoaded', go); else setTimeout(go, 0);
  }
})(typeof globalThis !== 'undefined' ? globalThis : this);
