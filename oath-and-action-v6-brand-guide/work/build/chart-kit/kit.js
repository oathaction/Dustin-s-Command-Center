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
  function fixed(v, nd) { var p = Math.abs(v).toFixed(nd || 0).split('.'); p[0] = p[0].replace(/\B(?=(\d{3})+(?!\d))/g, ','); return p.join('.'); }
  function signed(v, txt) { return (v > 0 ? '+' : v < 0 ? MINUS : '') + txt; }
  K.fmt = function (v, format) {
    if (v === null || v === undefined || v === '') return '';
    var f = String(format || 'text'), nd = 0, m = f.match(/^([a-z-]+):(\d+)$/);
    if (m) { f = m[1]; nd = +m[2]; }
    switch (f) {
      case 'text': return String(v);
      case 'integer': return (v < 0 ? MINUS : '') + group(Math.round(Math.abs(v)));
      case 'number': return (v < 0 ? MINUS : '') + fixed(v, nd);
      case 'percent': return (v < 0 ? MINUS : '') + fixed(v, nd) + '%';
      case 'signed': return signed(v, fixed(v, nd));
      case 'points': return (v < 0 ? MINUS : '') + fixed(v, nd);
      case 'compact-thousands':
      case 'signed-compact-thousands': {
        var a = Math.abs(v) * 1000, sg = f === 'signed-compact-thousands' ? (v > 0 ? '+' : v < 0 ? MINUS : '') : (v < 0 ? MINUS : '');
        if (a >= 1e6) return sg + (a / 1e6).toFixed(a >= 1e7 ? 0 : 1) + ' million';
        return sg + group(Math.round(a / 1000) * 1000);
      }
      case 'thousands': return (v < 0 ? MINUS : '') + group(m ? Math.round(Math.abs(v)) * 1000 : Math.round(Math.abs(v) * 1000));
      case 'signed-thousands': return m ? signed(Math.round(v) === 0 ? 0 : v, group(Math.round(Math.abs(v)) * 1000)) : signed(v, group(Math.round(Math.abs(v) * 1000)));
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
      var j = m.idx[s[i]];
      w += j === undefined ? fallback : adv[j];
    }
    return w * size / 1000;
  };
  K.wrap = function (text, size, max, weight, face) {
    var words = String(text).split(/\s+/), lines = [], cur = '';
    for (var i = 0; i < words.length; i++) {
      var t = cur ? cur + ' ' + words[i] : words[i];
      if (cur && K.measure(t, size, weight, face) > max) { lines.push(cur); cur = words[i]; } else cur = t;
    }
    if (cur) lines.push(cur);
    return lines;
  };

  // ------------------------------------------------------------------------------------------------------------
  // Tokens: numbers from tokens.css. In a browser the figure's computed style; in Node a map the CLI builds.
  // ------------------------------------------------------------------------------------------------------------
  K.tokens_from_css = function (css, surface) {
    // every --oa-* in :root, then the surface class block's short names, with var() chains resolved
    var map = {};
    function block(sel) {
      var re = new RegExp(sel.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '\\s*\\{([^}]*)\\}', 'g'), m, out = [];
      while ((m = re.exec(css))) out.push(m[1]);
      return out.join('\n');
    }
    function take(txt) {
      var re = /(--oa-[a-z0-9-]+)\s*:\s*([^;]+);/g, m;
      while ((m = re.exec(txt))) map[m[1]] = m[2].trim();
    }
    take(block(':root'));
    if (surface) take(block('.oa-surface-' + surface));
    function res(v, depth) {
      if (depth > 12) return v;
      return v.replace(/var\((--[a-z0-9-]+)(?:\s*,\s*([^()]*(?:\([^()]*\))?[^()]*))?\)/g, function (_, n, fb) {
        return map[n] !== undefined ? res(map[n], depth + 1) : (fb !== undefined ? res(fb.trim(), depth + 1) : 'var(' + n + ')');
      });
    }
    var out = {};
    for (var k in map) out[k] = res(map[k], 0);
    return out;
  };
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
    var rows = [], row = [], cell = '', q = false, i = 0, s = String(text).replace(/^﻿/, '');
    for (; i < s.length; i++) {
      var ch = s[i];
      if (q) {
        if (ch === '"') { if (s[i + 1] === '"') { cell += '"'; i++; } else q = false; } else cell += ch;
      } else if (ch === '"') q = true;
      else if (ch === ',') { row.push(cell); cell = ''; }
      else if (ch === '\n' || ch === '\r') {
        if (ch === '\r' && s[i + 1] === '\n') i++;
        row.push(cell); cell = '';
        if (row.length > 1 || row[0] !== '') rows.push(row);
        row = [];
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
  K.select = function (spec, rows) {
    var w = spec.where || {};
    var out = rows.filter(function (r) {
      for (var k in w) {
        var want = Array.isArray(w[k]) ? w[k] : [w[k]];
        if (want.map(String).indexOf(String(r[k])) < 0) return false;
      }
      return true;
    });
    var pv0 = spec.table && spec.table.pivot;
    var after = function () {
      if (!pv0) return out;
      var rk = function (r) { return [].concat(pv0.row).map(function (k) { return String(r[k]); }).join('\u0001'); };
      var keys = [], cols = [], at = {};
      out.forEach(function (r) { var a = rk(r), b = String(r[pv0.column]); if (keys.indexOf(a) < 0) keys.push(a); if (cols.indexOf(b) < 0) cols.push(b); at[a + '\u0000' + b] = r; });
      var res = [];
      keys.forEach(function (a) { cols.forEach(function (b) { if (at[a + '\u0000' + b]) res.push(at[a + '\u0000' + b]); }); });
      return res;
    };
    (spec.sort || []).slice().reverse().forEach(function (s) {
      var dir = s.order === 'desc' ? -1 : 1;
      out = out.map(function (r, i) { return [r, i]; }).sort(function (a, b) {
        var x = a[0][s.field], y = b[0][s.field];
        if (x === y) return a[1] - b[1];
        if (x === null) return 1;
        if (y === null) return -1;
        return (x < y ? -1 : 1) * dir;
      }).map(function (p) { return p[0]; });
    });
    return after();
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
    this.warnings = [];
    this._h = 0;
  }
  K.Ctx = Ctx;
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
    return c.join(' ') || undefined;
  }
  function data_of(o, base) {
    var d = o.data || {};
    for (var k in d) if (d[k] !== undefined && d[k] !== null) base['data-' + k] = d[k];
    return base;
  }
  Ctx.prototype.size = function (role) {
    var r = TEXT_ROLES[role] || 'type-label', s = this.t(r);
    if (role === 'big' && this.phone) s = this.t('type-big-phone');
    if (role === 'label' && this.phone) s = Math.max(this.t('type-phone-min'), Math.min(s, this.t('type-phone-min')));
    return s;
  };
  Ctx.prototype.measure = function (words, role, weight, tnum) {
    return K.measure(words, typeof role === 'number' ? role : this.size(role || 'label'), weight || 400, role === 'big' ? 'display' : 'reading', tnum);
  };
  Ctx.prototype.wrap = function (words, role, max, weight) {
    return K.wrap(words, this.size(role || 'note'), max, weight || 400, role === 'big' ? 'display' : 'reading');
  };
  Ctx.prototype._push = function (s) { (this._grp || this._els).push(s); };
  Ctx.prototype.group = function (o) {
    var self = this, prev = this._grp, buf = [];
    this._grp = buf;
    return {
      end: function () {
        self._grp = prev;
        var a = data_of(o || {}, { 'class': cls_of(o || {}), transform: o && o.transform });
        self._push('<g' + attrs(a) + '>' + buf.join('') + '</g>');
      }
    };
  };
  Ctx.prototype.mark = function (m) { this.marks.push(m); return m; };
  Ctx.prototype.rect = function (x, y, w, h, o) {
    o = o || {};
    if (w < 0) { x += w; w = -w; }
    if (h < 0) { y += h; h = -h; }
    var a = data_of(o, { x: r1(x), y: r1(y), width: r1(w), height: r1(h), 'class': cls_of(o), rx: o.rx, 'stroke-width': o.width, 'stroke-dasharray': o.dash });
    if (o.pattern) a.fill = 'url(#' + this.uid + '-' + o.pattern + ')';
    this._push('<rect' + attrs(a) + '/>');
    if (o.mark !== false) this.mark({ kind: o.kind || 'rect', x: x, y: y, w: w, h: h, fill: o.fill, stroke: o.stroke, data: o.data || {}, zero: o.zero, axis: o.axis });
  };
  Ctx.prototype.line = function (x1, y1, x2, y2, o) {
    o = o || {};
    var a = data_of(o, { x1: r1(x1), y1: r1(y1), x2: r1(x2), y2: r1(y2), 'class': cls_of(o), 'stroke-width': o.width, 'stroke-dasharray': o.dash });
    this._push('<line' + attrs(a) + '/>');
    if (o.mark !== false) this.mark({ kind: o.kind || 'line', x: Math.min(x1, x2), y: Math.min(y1, y2), w: Math.abs(x2 - x1), h: Math.abs(y2 - y1), stroke: o.stroke, data: o.data || {} });
  };
  Ctx.prototype.path = function (d, o, box) {
    o = o || {};
    var a = data_of(o, { d: d, 'class': cls_of(o), 'stroke-width': o.width, 'stroke-dasharray': o.dash });
    if (o.pattern) a.fill = 'url(#' + this.uid + '-' + o.pattern + ')';
    this._push('<path' + attrs(a) + '/>');
    if (box && o.mark !== false) this.mark({ kind: o.kind || 'path', x: box[0], y: box[1], w: box[2], h: box[3], fill: o.fill, stroke: o.stroke, data: o.data || {} });
  };
  Ctx.prototype.datum = function (x, y, o) {
    // a record for the checks at a point the drawing already inks (a line's vertex): no element, no bytes
    this.mark({ kind: 'datum', x: x, y: y, w: 0, h: 0, data: (o && o.data) || {} });
  };
  Ctx.prototype.circle = function (cx, cy, r, o) {
    o = o || {};
    var a = data_of(o, { cx: r1(cx), cy: r1(cy), r: r2(r), 'class': cls_of(o), 'stroke-width': o.width });
    this._push('<circle' + attrs(a) + '/>');
    if (o.mark !== false) this.mark({ kind: o.kind || 'circle', x: cx - r, y: cy - r, w: 2 * r, h: 2 * r, r: r, fill: o.fill, stroke: o.stroke, data: o.data || {}, area_of: o.area_of });
  };
  Ctx.prototype.polygon = function (pts, o) {
    o = o || {};
    var xs = pts.map(function (p) { return p[0]; }), ys = pts.map(function (p) { return p[1]; });
    var a = data_of(o, { points: pts.map(function (p) { return r1(p[0]) + ',' + r1(p[1]); }).join(' '), 'class': cls_of(o) });
    this._push('<polygon' + attrs(a) + '/>');
    if (o.mark !== false) this.mark({ kind: o.kind || 'polygon', x: Math.min.apply(null, xs), y: Math.min.apply(null, ys), w: Math.max.apply(null, xs) - Math.min.apply(null, xs), h: Math.max.apply(null, ys) - Math.min.apply(null, ys), fill: o.fill, data: o.data || {} });
  };
  Ctx.prototype.text = function (x, y, words, o) {
    // y is the baseline. o: role (tick, label, note, big, eyebrow), weight, anchor, fill, halo, tnum, max (wrap width)
    o = o || {};
    var role = o.role || 'label', size = o.size || this.size(role), weight = o.weight || 400, anchor = o.anchor || 'start';
    var face = o.face || (role === 'big' ? 'display' : 'reading');
    var lines = o.max ? K.wrap(words, size, o.max, weight, face) : [String(words)];
    var lh = o.leading || Math.round(size * (role === 'note' ? 1.36 : 1.25));
    var self = this, w = 0;
    lines.forEach(function (ln) { w = Math.max(w, K.measure(ln, size, weight, face, o.tnum)); });
    var x0 = anchor === 'middle' ? x - w / 2 : anchor === 'end' ? x - w : x;
    var cls = ['oac-t', 'oac-t-' + (face === 'display' ? 'big' : role), 'oac-w' + Math.round(weight / 100), o.fill ? 'oac-f-' + o.fill : (role === 'tick' ? 'oac-f-secondary' : 'oac-f-label')];
    if (o.halo) cls.push('oac-halo');
    if (o.tnum) cls.push('oac-tnum');
    var a = data_of(o, { x: r1(x), y: r1(y), 'class': cls.join(' '), 'font-size': size, 'text-anchor': anchor === 'start' ? undefined : anchor });
    var body = lines.length === 1 ? esc(lines[0]) : lines.map(function (ln, i) { return '<tspan x="' + r1(x) + '"' + (i ? ' dy="' + lh + '"' : '') + '>' + esc(ln) + '</tspan>'; }).join('');
    this._push('<text' + attrs(a) + '>' + body + '</text>');
    // the box the browser gives this text: its line box (ascent 0.969 em, descent 0.241 em, from the metrics) for the edges,
    // and that box less the half-leading for overlaps, as dataviz_check.js --kit measures a rendered drawing
    var vm = metrics().vertical[face === 'display' ? 'Inter Tight|800' : 'Inter|400'] || { ascent: 969, descent: 241 };
    var asc = size * vm.ascent / 1000, desc = size * vm.descent / 1000, half = (asc + desc - size) / 2;
    var box = { x: x0, y: y - asc + half, w: w, h: asc + desc - 2 * half + lh * (lines.length - 1), size: size, words: String(words), role: role,
      overlap_ok: !!o.overlap_ok, id: o.guard_id, top: y - asc, bottom: y + desc + lh * (lines.length - 1), halo: !!o.halo, fill: o.fill };
    this.texts.push(box);
    return box;
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
    if (!def || !def.form || typeof def.draw !== 'function') throw new Error('register_chart: a form needs "form" and "draw"');
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
  K.draw = function (spec, rows, opts) {
    // returns {svg, width, height, texts, marks, warnings, guard}
    var def = K.forms[spec.form];
    if (!def) throw new Error('OAChart: form "' + spec.form + '" is not registered');
    var t = opts.t || token_reader(opts.tokens || {});
    var width = Math.round(opts.width || K.artboard(spec, t));
    var c = new Ctx(spec, rows, { width: width, ground: opts.ground, t: t, extra: opts.extra, uid: opts.uid || ('oac-' + String(spec.id).toLowerCase() + '-' + width) });
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
    // a text whose line box rises above the top edge moves the whole drawing down by that much, so nothing is cut
    var lift = 0;
    c.texts.forEach(function (b) { lift = Math.max(lift, -(b.top !== undefined ? b.top : b.y)); });
    if (lift > 0.25) {
      var dy = Math.ceil(lift);
      c._els = ['<g transform="translate(0,' + dy + ')">' + c._els.join('') + '</g>'];
      c.texts.forEach(function (b) { b.y += dy; if (b.top !== undefined) { b.top += dy; b.bottom += dy; } });
      c.marks.forEach(function (m) { m.y += dy; if (m.zero !== undefined && m.axis !== 'x') m.zero += dy; });
      c._h += dy;
    }
    // the drawing is as tall as its tallest part: the form's height, every text and every mark
    var h = c._h;
    c.texts.forEach(function (b) { h = Math.max(h, Math.ceil((b.bottom !== undefined ? b.bottom : b.y + b.h) + 2)); });
    c.marks.forEach(function (m) { h = Math.max(h, Math.ceil(m.y + m.h + 1)); });
    h = Math.max(1, h);
    var guard = K.guard(c, width, h);
    var title = spec.title ? '<title>' + esc(spec.title) + '</title>' : '';   // a table-mode island leaves both out; the figure names the drawing
    var desc = spec.alt ? '<desc>' + esc(spec.alt) + '</desc>' : '';
    var defs = c._defs.length ? '<defs>' + c._defs.join('') + '</defs>' : '';
    var svg = '<svg xmlns="http://www.w3.org/2000/svg" class="oac-svg" viewBox="0 0 ' + width + ' ' + h + '" width="' + width + '" height="' + h + '"' +
      ' role="img" data-oa-form="' + esc(spec.form) + '" data-oa-width="' + width + '"' + (opts.label_id ? ' aria-labelledby="' + esc(opts.label_id) + '"' : '') + '>' +
      title + desc + defs + c._els.join('') + '</svg>';
    return { svg: svg, width: width, height: h, texts: c.texts, marks: c.marks, keys: c.keys || [], warnings: c.warnings, guard: guard, phone: c.phone };
  };

  // ------------------------------------------------------------------------------------------------------------
  // The layout guard: every text inside the artboard, no two texts overlapping, nothing under 13 px
  // ------------------------------------------------------------------------------------------------------------
  K.MIN_TEXT = 13;
  K.guard = function (c, width, height) {
    var out = [], pad = 1;
    var tx = c.texts;
    for (var i = 0; i < tx.length; i++) {
      var a = tx[i];
      if (a.size < K.MIN_TEXT - 1e-6) out.push('text under 13 px (' + a.size + ' px): "' + a.words.slice(0, 40) + '"');
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
    return out;
  };

  // ------------------------------------------------------------------------------------------------------------
  // Words: atlas IDs in chips, the figure, the table equivalent
  // ------------------------------------------------------------------------------------------------------------
  K.words = K.words || {};
  function word(opts, k) {
    var w = (opts && opts.words) || K.words;
    if (!(k in w)) throw new Error('OAChart: words.json has no "' + k + '"');
    return w[k];
  }
  K.chips = function (text, ids) {
    // set each atlas ID the spec names (spec.v7.ids) in its typed chip; an ASCII hyphen, never U+2011, in a no-wrap span
    var s = esc(text);
    if (!ids || !ids.length) return s;
    var sorted = ids.slice().sort(function (a, b) { return b.length - a.length; });
    var re = new RegExp('(^|[^A-Za-z0-9-])(' + sorted.map(function (x) { return esc(x).replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }).join('|') + ')(?![A-Za-z0-9])', 'g');
    var types = K.id_types || {};
    return s.replace(re, function (all, pre, id, off, whole) {
      var tw = types[id], before = whole.slice(Math.max(0, off - 16), off + pre.length).toLowerCase();
      var typed = tw && before.indexOf(tw.toLowerCase()) < 0 ? tw + ' ' : '';
      return pre + '<span class="oa-id" data-oa-id="' + id + '">' + typed + id + '</span>';
    });
  };
  K.table_rows = function (spec, rows) {
    // the table equivalent's body rows: one per data row, or a pivot (spec.table.pivot) with one cell per data row
    var tb = spec.table || {};
    if (tb.pivot) {
      var pv = tb.pivot, keys = [], cols = [], cell = {};
      var rkey = function (r) { return [].concat(pv.row).map(function (k) { return String(r[k]); }).join('\u0001'); };
      rows.forEach(function (r) {
        var rk = rkey(r), ck = String(r[pv.column]);
        if (keys.indexOf(rk) < 0) keys.push(rk);
        if (cols.indexOf(ck) < 0) cols.push(ck);
        cell[rk + '\u0000' + ck] = r;
      });
      return { pivot: true, keys: keys, cols: cols, cell: cell, rkey: rkey };
    }
    return { pivot: false, rows: rows };
  };
  K.lead = function (v, words, nd) {
    // "Republican +1.5": the leader's word by sign, then the absolute value with a plus sign (H10)
    if (v === null || v === undefined || v === '') return '';
    words = words || {};
    if (Math.abs(v) < Math.pow(10, -(nd || 0)) / 2) return words.zero || K.fmt(0, 'number:' + (nd || 0));
    return (v > 0 ? words.positive : words.negative) + ' +' + fixed(v, nd || 0);
  };
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
    if (/^(integer|number|percent|signed|points)$/.test(base)) {
      var n = t.replace(/[+,%\s]/g, '').replace(MINUS, '-');
      return /^-?\d+(\.\d+)?$/.test(n) ? n : undefined;
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
  function same_value(a, b, type) {
    if (a === undefined) return false;
    if (b === null || b === undefined || b === '') return a === null;
    if (a === null) return false;
    if (type === 'number' || type === 'integer' || type === 'year') return Math.abs(parseFloat(a) - Number(b)) < 1e-9;
    return String(a) === String(b);
  }
  function visible_text(h) {
    return String(h).replace(/<[^>]*>/g, '').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&amp;/g, '&');
  }
  K.cell_text = function (col, r) {
    var v = r[col.field];
    var lm = /^lead(?::(\d+))?$/.exec(String(col.format || ''));
    if (lm) return K.lead(v, col.lead, lm[1] ? +lm[1] : 0);
    if (col.words && v !== null && v !== undefined && col.words[String(v)] !== undefined) return col.words[String(v)];
    return K.fmt(v, col.format);
  };
  K.table_html = function (spec, rows, opts) {
    if (opts && opts.lean) return lean_table(spec, rows, opts);
    var tb = spec.table || {}, ids = (spec.v7 && spec.v7.ids) || [];
    var cap = tb.caption ? '<caption>' + K.chips(tb.caption, ids) + '</caption>' : '';
    var t = K.table_rows(spec, rows), head = '', body = '';
    function num_col(col) { return /^(integer|number|percent|signed|points|thousands|signed-thousands)/.test(String(col.format || '')); }
    if (t.pivot) {
      var pv = tb.pivot, rc = (tb.columns || [])[0] || { label: pv.row, format: 'text' };
      head = '<tr><th scope="col">' + esc(rc.label) + '</th>' + t.cols.map(function (cn) {
        var lab = (pv.labels && pv.labels[cn]) || cn;
        return '<th scope="col" class="oac-num">' + K.chips(lab, ids) + '</th>';
      }).join('') + '</tr>';
      body = t.keys.map(function (k) {
        var first = null;
        var cells = t.cols.map(function (cn) {
          var r = t.cell[k + '\u0000' + cn];
          if (r && !first) first = r;
          return '<td class="oac-num"' + (r ? ' data-oa-row="1"' : '') + '>' + (r ? esc(K.fmt(r[pv.value], pv.format)) : '') + '</td>';
        }).join('');
        var rows_by = [].concat(pv.row), head_txt = first ? K.fmt(first[rows_by[0]], rc.format) : k;
        if (first && rows_by.length > 1) rows_by.slice(1).forEach(function (k2) {
          var v2 = first[k2], w2 = (pv.row_words || {})[String(v2)];
          if (w2) head_txt += ', ' + w2;
        });
        return '<tr><th scope="row">' + esc(head_txt) + '</th>' + cells + '</tr>';
      }).join('');
    } else {
      var cols = tb.columns || [];
      head = '<tr>' + cols.map(function (col) { return '<th scope="col"' + (num_col(col) ? ' class="oac-num"' : '') + '>' + K.chips(col.label, ids) + '</th>'; }).join('') + '</tr>';
      body = t.rows.map(function (r) {
        return '<tr data-oa-row="1">' + cols.map(function (col) {
          var txt = K.chips(K.cell_text(col, r), ids);
          return col.row_header ? '<th scope="row">' + txt + '</th>' : '<td' + (num_col(col) ? ' class="oac-num"' : '') + '>' + txt + '</td>';
        }).join('') + '</tr>';
      }).join('');
    }
    return '<table class="oac-table">' + cap + '<thead>' + head + '</thead><tbody>' + body + '</tbody></table>';
  };
  function lean_table(spec, rows, opts) {
    var tb = spec.table || {}, ids = (spec.v7 && spec.v7.ids) || [], types = opts.types || {};
    var cap = tb.caption ? '<caption>' + K.chips(tb.caption, ids) + '</caption>' : '';
    var t = K.table_rows(spec, rows), head = '', body = '';
    var num_col = function (col) { return /^(integer|number|percent|signed|points|thousands|signed-thousands|lead|compact-thousands|signed-compact-thousands)/.test(String(col.format || '')); };
    var dv = function (raw, html, col) {
      var back = K.unformat(visible_text(html), col);
      return same_value(back, raw, types[col.field] && types[col.field].type) ? '' : ' data-v="' + esc(raw === null || raw === undefined ? '' : raw) + '"';
    };
    if (t.pivot) {
      var pv = tb.pivot, rc = (tb.columns || [])[0] || { label: pv.row, format: 'text' }, rows_by = [].concat(pv.row);
      head = '<tr><th scope="col" class="t">' + esc(rc.label) + '</th>' + t.cols.map(function (cn) {
        var lab = (pv.labels && pv.labels[cn]) || cn, h = K.chips(lab, ids);
        return '<th scope="col"' + (visible_text(h) === cn ? '' : ' data-v="' + esc(cn) + '"') + '>' + h + '</th>';
      }).join('') + '</tr>';
      var vcol = { field: pv.value, format: pv.format };
      body = t.keys.map(function (k) {
        var first = null;
        var cells = t.cols.map(function (cn) {
          var r = t.cell[k + '\u0000' + cn];
          if (r && !first) first = r;
          if (!r) return '<td data-x></td>';
          var h = esc(K.fmt(r[pv.value], pv.format));
          return '<td' + dv(r[pv.value], h, vcol) + '>' + h + '</td>';
        }).join('');
        var head_txt = first ? K.fmt(first[rows_by[0]], rc.format) : k;
        if (first && rows_by.length > 1) rows_by.slice(1).forEach(function (k2) { var w2 = (pv.row_words || {})[String(first[k2])]; if (w2) head_txt += ', ' + w2; });
        var keyv = rows_by.length > 1 ? JSON.stringify(rows_by.map(function (k2) { return first ? first[k2] : null; })) : null;
        var hv = keyv !== null ? ' data-v="' + esc(keyv) + '"' : dv(first ? first[rows_by[0]] : k, esc(head_txt), { field: rows_by[0], format: rc.format });
        return '<tr><th scope="row" class="t"' + hv + '>' + esc(head_txt) + '</th>' + cells + '</tr>';
      }).join('');
    } else {
      var cols = tb.columns || [];
      head = '<tr>' + cols.map(function (col) { return '<th scope="col"' + (num_col(col) ? '' : ' class="t"') + '>' + K.chips(col.label, ids) + '</th>'; }).join('') + '</tr>';
      body = t.rows.map(function (r) {
        return '<tr>' + cols.map(function (col) {
          var h = K.chips(K.cell_text(col, r), ids), tag = col.row_header ? 'th' : 'td';
          return '<' + tag + (col.row_header ? ' scope="row"' : '') + (num_col(col) ? '' : ' class="t"') + dv(r[col.field], h, col) + '>' + h + '</' + tag + '>';
        }).join('') + '</tr>';
      }).join('');
    }
    return '<table class="oac-table" data-oa-lean>' + cap + '<thead>' + head + '</thead><tbody>' + body + '</tbody></table>';
  }
  K.rows_from_table = function (table, spec, isl) {
    // the rows a chart draws, read back from its own table equivalent and the island's extra columns (method load-table)
    var tb = spec.table || {}, out = [], cell_raw = function (el, col) {
      return el.hasAttribute('data-v') ? el.getAttribute('data-v') : K.unformat(el.textContent, col);
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
          if (td.hasAttribute('data-x')) return;
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
    if (isl.csv) {
      var extra = K.parse_csv(isl.csv);
      out.forEach(function (o, i) { var e = extra[i] || {}; for (var k in e) o[k] = e[k]; });
    }
    return K.type_rows(out, isl.columns);
  };
  K.figure = function (spec, rows, opts) {
    // the whole figure as HTML; opts.svg puts a drawing inside, opts.art_attrs adds attributes to the drawing's box
    opts = opts || {};
    var ids = (spec.v7 && spec.v7.ids) || [], id = String(opts.id || ('oac-' + String(spec.id).toLowerCase()));
    var show = spec.show || ['evidence', 'title', 'guide', 'measure', 'chart', 'notes', 'source', 'table'];
    var has = function (k) { return show.indexOf(k) >= 0 || (k === 'evidence' && show.indexOf('title') >= 0 && !spec.show) || (k === 'guide' && show.indexOf('measure') >= 0 && !spec.show); };
    var p = [];
    if (has('evidence') && spec.evidence_label) {
      p.push('<div class="oac-ev"><p class="oac-ev-k" data-role="evidence-label">' + esc(spec.evidence_label) + '</p>' +
        (spec.grade_line ? '<p class="oac-ev-g" data-role="grade">' + K.chips(spec.grade_line, ids) + '</p>' : '') + '</div>');
    }
    if (has('title')) p.push('<p class="oac-title" id="' + id + '-t" data-role="title">' + K.chips(spec.title, ids) + '</p>');
    if (has('guide') && spec.reading_guide) p.push('<p class="oac-guide" data-role="reading-guide">' + K.chips(spec.reading_guide, ids) + '</p>');
    if (has('measure') && spec.measure_line) p.push('<p class="oac-measure" data-role="measure">' + K.chips(spec.measure_line, ids) + '</p>');
    if (has('chart')) {
      var illus = spec.illustrative ? '<p class="oac-illus" data-role="illustrative">' + esc(spec.illustrative) + '</p>' : '';
      p.push('<div class="oac-art" data-oa-art' + (opts.art_attrs || '') + '>' + illus + (opts.svg || '') + '</div>');
      if (spec.alt) p.push('<p class="oac-alt" id="' + id + '-alt" data-role="alt">' + K.chips(spec.alt, ids) + '</p>');
    }
    if (has('chart') && spec.phone_notes && spec.phone_notes.length) p.push('<ul class="oac-notes oac-phone-notes" data-role="phone-notes">' + spec.phone_notes.map(function (n) { return '<li>' + K.chips(n, ids) + '</li>'; }).join('') + '</ul>');
    if (has('notes') && spec.notes && spec.notes.length) p.push('<ul class="oac-notes" data-role="notes">' + spec.notes.map(function (n) { return '<li>' + K.chips(n, ids) + '</li>'; }).join('') + '</ul>');
    if (has('source')) {
      var src = String(spec.source_line || ''), lab = word(opts, 'source_label');
      var rest = src.indexOf(lab) === 0 ? src.slice(lab.length).replace(/^\s+/, '') : src;
      p.push('<div class="oac-src"><p class="oac-source" data-role="source"><span class="oac-src-k">' + esc(lab) + '</span> ' + K.chips(rest, ids) + '</p>' +
        (spec.credit ? '<p class="oac-credit">' + esc(spec.credit) + '</p>' : '') + '</div>');
    }
    // the table equivalent is always kept (contract C7), folded, as live text
    var cn = spec.chart_notes && spec.chart_notes.length ? '<p class="oac-eq-h">' + esc(word(opts, 'notes_in_chart')) + '</p><ul class="oac-eq-n">' +
      spec.chart_notes.map(function (n) { return '<li>' + K.chips(n, ids) + '</li>'; }).join('') + '</ul>' : '';
    var region = word(opts, 'table_region').replace('{caption}', (spec.table && spec.table.caption) || spec.id);
    p.push('<details class="oac-eq" data-role="equivalent"><summary>' + esc(word(opts, 'table_summary')) + '<span class="oac-vh"> ' + esc(spec.id) + '</span></summary>' +
      '<div class="oac-eq-b">' + cn + (opts.guide ? '<div class="oac-tw" role="group" aria-label="' + esc(region) + '">' : '<div class="oac-tw" role="region" tabindex="0" aria-label="' + esc(region) + '">') + K.table_html(spec, rows, { lean: opts.lean_table, types: opts.types }) + '</div></div></details>');
    var fail = spec.failure ? ' data-oa-failure="' + esc(spec.failure.rule || '') + '"' : '';
    var ab = spec.artboard && spec.artboard !== 'reading' ? ' data-oa-artboard="' + esc(spec.artboard) + '"' : '';
    return '<figure class="oac-fig" id="' + id + '" data-oa-chart-id="' + esc(spec.id) + '" data-form="' + esc(spec.form) + '" data-evidence="' + esc(spec.evidence) + '"' + ab + fail + '>' + p.join('') + '</figure>';
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
    var last = -1, result = null;
    function draw() {
      var w = K.artboard(spec, t, art.clientWidth || fig.clientWidth);
      if (w === last) return;
      last = w;
      // the drawing takes its name from the figure's printed title; a plate that prints no title (chapter 13's) names it
      // by its description, so the name never points at an element that is not there
      var doc = fig.ownerDocument || root.document;
      var has_t = fig.id && doc.getElementById(fig.id + '-t'), has_alt = fig.id && doc.getElementById(fig.id + '-alt');
      var lid = has_t ? fig.id + '-t' : (has_alt ? fig.id + '-alt' : null);
      result = K.draw(spec, rows, { width: w, ground: ground, t: t, extra: extra, uid: (fig.id || 'oac') + '-' + w, label_id: lid });
      var old = art.querySelector('svg.oac-svg');
      if (old) old.remove();
      art.insertAdjacentHTML('beforeend', result.svg);
      var svg = art.querySelector('svg.oac-svg');
      if (svg && has_t && has_alt) svg.setAttribute('aria-describedby', fig.id + '-alt');
      if (svg && !lid) svg.setAttribute('aria-label', String(spec.alt || spec.title || ''));
      fig.setAttribute('data-oa-drawn', String(w));
      if (result.guard.length || result.warnings.length) fig.setAttribute('data-oa-warnings', String(result.guard.length + result.warnings.length));
    }
    draw();
    if (root.ResizeObserver) new root.ResizeObserver(function () { draw(); }).observe(art);
    var tw = fig.querySelector('.oac-tw[role="group"]'), eq = fig.querySelector('details.oac-eq');
    var stop = function () { if (!tw) return; if (tw.scrollWidth > tw.clientWidth + 1) tw.setAttribute('tabindex', '0'); else tw.removeAttribute('tabindex'); };
    if (tw && eq) { eq.addEventListener('toggle', stop); if (root.addEventListener) root.addEventListener('resize', stop); }
    return { redraw: function () { last = -1; draw(); }, result: function () { return result; } };
  };
  K.mount_all = function (scope) {
    // every figure with a JSON island: a script element of type application/json marked data-oa-chart-data, holding {spec, columns, csv}
    var figs = (scope || root.document).querySelectorAll('figure.oac-fig');
    for (var i = 0; i < figs.length; i++) {
      var f = figs[i], isl = f.querySelector('script[data-oa-chart-data]');
      if (!isl || f.getAttribute('data-oa-drawn')) continue;
      try {
        var d = JSON.parse(isl.textContent);
        var rows = d.mode === 'table' ? K.rows_from_table(f.querySelector('table.oac-table'), d.spec, d)
          : d.csv !== undefined ? K.type_rows(K.parse_csv(d.csv), d.columns) : K.type_rows(d.rows || [], d.columns);
        var extra = {};
        Object.keys(d.extra || {}).forEach(function (k) { extra[k] = K.type_rows(K.parse_csv(d.extra[k].csv), d.extra[k].columns); });
        K.mount(f, d.spec, rows, { words: d.words, extra: extra });
      } catch (e) {
        f.setAttribute('data-oa-error', String(e && e.message || e));
      }
    }
  };
  if (root.document && root.document.addEventListener) {
    var go = function () { K.mount_all(); };
    if (root.document.readyState === 'loading') root.document.addEventListener('DOMContentLoaded', go); else setTimeout(go, 0);
  }
})(typeof globalThis !== 'undefined' ? globalThis : this);
