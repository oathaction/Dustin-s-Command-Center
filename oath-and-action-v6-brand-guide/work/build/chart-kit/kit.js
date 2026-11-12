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
      // dollars (R-B2, round 1): $2,000 and −$2,000; signed-dollars +$2,000; dollars:2 keeps cents
      case 'dollars': return (v < 0 ? MINUS : '') + '$' + fixed(v, nd);
      case 'signed-dollars': return signed(v, '$' + fixed(v, nd));
      // billions (R-B7, round 1): a value in dollars as 173.2 billion; billions-value prints 173.2 for a column headed in billions
      case 'billions': return (v < 0 ? MINUS : '') + fixed(v / 1e9, nd) + ' billion';
      case 'billions-value': return (v < 0 ? MINUS : '') + fixed(v / 1e9, nd);
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
      var j = m.idx[s[i] === '\u00a0' ? ' ' : s[i]];   // a no-break space is as wide as a space
      w += j === undefined ? fallback : adv[j];
    }
    return w * size / 1000;
  };
  K.wrap = function (text, size, max, weight, face) {
    // lines break at spaces only, so a no-break space holds two words together
    var words = String(text).split(/[ \t\r\n]+/), lines = [], cur = '';
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
  function in_range(v, rg) {
    if (v === null || v === undefined || v === '') return false;
    var num = function (x) { return typeof x === 'number' || (typeof x === 'string' && /^-?\d+(\.\d+)?$/.test(x)); };
    var cmp = function (a, b) { return num(a) && num(b) ? Number(a) - Number(b) : String(a) < String(b) ? -1 : String(a) > String(b) ? 1 : 0; };
    return !('from' in rg && cmp(v, rg.from) < 0) && !('to' in rg && cmp(v, rg.to) > 0);
  }
  K.select = function (spec, rows) {
    var w = spec.where || {};
    var out = rows.filter(function (r) {
      for (var k in w) {
        // where: {column: value or [values]} keeps those rows; {column: {not: value or [values]}} leaves them out;
        // {column: {from: a, to: b}} keeps a to b, both ends kept, compared as numbers when both are, else as text (R-B3)
        if (w[k] && typeof w[k] === 'object' && !Array.isArray(w[k]) && ('from' in w[k] || 'to' in w[k])) {
          if (!in_range(r[k], w[k])) return false;
          continue;
        }
        var neg = w[k] && typeof w[k] === 'object' && !Array.isArray(w[k]) && 'not' in w[k];
        var want = neg ? [].concat(w[k].not) : Array.isArray(w[k]) ? w[k] : [w[k]];
        if ((want.map(String).indexOf(String(r[k])) >= 0) === neg) return false;
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
    this.leaders = [];
    this.warnings = [];
    this.ink = [];   // K-S2 (round 1 fix pass): the box of every shape drawn, marks or not, so the check finds one outside the drawing
    this._tf = 0;
    this._h = 0;
  }
  K.Ctx = Ctx;
  var SHAPE_LIFT = 12;
  // a shape's box for the drawing-edge check; shapes inside a moved group (a map's projection) are left out
  Ctx.prototype._ink = function (kind, x, y, w, h, o) {
    if (this._tf) return;
    this.ink.push({ kind: kind, x: x, y: y, w: w, h: h, role: (o && (o.fill || o.stroke)) || '' });
  };
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
    var self = this, prev = this._grp, buf = [], tf = !!(o && o.transform);
    this._grp = buf;
    if (tf) this._tf++;
    return {
      end: function () {
        self._grp = prev;
        if (tf) self._tf--;
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
    this._ink('rect', x, y, w, h, o);
    if (o.mark !== false) this.mark({ kind: o.kind || 'rect', x: x, y: y, w: w, h: h, fill: o.fill, stroke: o.stroke, data: o.data || {}, zero: o.zero, axis: o.axis });
  };
  Ctx.prototype.line = function (x1, y1, x2, y2, o) {
    o = o || {};
    var a = data_of(o, { x1: r1(x1), y1: r1(y1), x2: r1(x2), y2: r1(y2), 'class': cls_of(o), 'stroke-width': o.width, 'stroke-dasharray': o.dash });
    this._push('<line' + attrs(a) + '/>');
    this._ink('line', Math.min(x1, x2), Math.min(y1, y2), Math.abs(x2 - x1), Math.abs(y2 - y1), o);
    // a leader is kept for the guard, which fails one that runs through a label (D3-93)
    if (o.stroke === 'leader' && !this._grp_t) this.leaders.push({ x1: x1, y1: y1, x2: x2, y2: y2 });
    if (o.mark !== false) this.mark({ kind: o.kind || 'line', x: Math.min(x1, x2), y: Math.min(y1, y2), w: Math.abs(x2 - x1), h: Math.abs(y2 - y1), stroke: o.stroke, data: o.data || {} });
  };
  Ctx.prototype.path = function (d, o, box) {
    o = o || {};
    var a = data_of(o, { d: d, 'class': cls_of(o), 'stroke-width': o.width, 'stroke-dasharray': o.dash });
    if (o.pattern) a.fill = 'url(#' + this.uid + '-' + o.pattern + ')';
    this._push('<path' + attrs(a) + '/>');
    var pb = path_box(String(d)) || box;
    if (pb) this._ink('path', pb[0], pb[1], pb[2], pb[3], o);
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
    this._ink('circle', cx - r, cy - r, 2 * r, 2 * r, o);
    if (o.mark !== false) this.mark({ kind: o.kind || 'circle', x: cx - r, y: cy - r, w: 2 * r, h: 2 * r, r: r, fill: o.fill, stroke: o.stroke, data: o.data || {}, area_of: o.area_of });
  };
  Ctx.prototype.polygon = function (pts, o) {
    o = o || {};
    var xs = pts.map(function (p) { return p[0]; }), ys = pts.map(function (p) { return p[1]; });
    var a = data_of(o, { points: pts.map(function (p) { return r1(p[0]) + ',' + r1(p[1]); }).join(' '), 'class': cls_of(o) });
    this._push('<polygon' + attrs(a) + '/>');
    this._ink('polygon', Math.min.apply(null, xs), Math.min.apply(null, ys), Math.max.apply(null, xs) - Math.min.apply(null, xs), Math.max.apply(null, ys) - Math.min.apply(null, ys), o);
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
    // a text whose line box rises above the top edge moves the whole drawing down by that much, so nothing is cut; so does
    // a shape's short stub (an axis line run past its first bar, up to SHAPE_LIFT px: K-S2); a shape further out is a fault
    // the check reports
    var lift = 0;
    c.texts.forEach(function (b) { lift = Math.max(lift, -(b.top !== undefined ? b.top : b.y)); });
    c.ink.forEach(function (b) { if (-b.y <= SHAPE_LIFT) lift = Math.max(lift, -b.y); });
    if (lift > 0.25) {
      var dy = Math.ceil(lift);
      c._els = ['<g transform="translate(0,' + dy + ')">' + c._els.join('') + '</g>'];
      c.texts.forEach(function (b) { b.y += dy; if (b.top !== undefined) { b.top += dy; b.bottom += dy; } });
      c.marks.forEach(function (m) { m.y += dy; if (m.zero !== undefined && m.axis !== 'x') m.zero += dy; });
      c.leaders.forEach(function (l) { l.y1 += dy; l.y2 += dy; });
      c.ink.forEach(function (b) { b.y += dy; });
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
    var fc = forced_patterns(c);
    var defs = c._defs.length || fc.defs ? '<defs>' + c._defs.join('') + fc.defs + '</defs>' : '';
    var svg = '<svg xmlns="http://www.w3.org/2000/svg" class="oac-svg' + (fc.defs ? ' oac-u-' + c.uid : '') + '" viewBox="0 0 ' + width + ' ' + h + '" width="' + width + '" height="' + h + '"' +
      ' role="img" data-oa-form="' + esc(spec.form) + '" data-oa-width="' + width + '"' + (opts.label_id ? ' aria-labelledby="' + esc(opts.label_id) + '"' : '') + '>' +
      title + desc + fc.style + defs + c._els.join('') + '</svg>';
    return { svg: svg, width: width, height: h, texts: c.texts, marks: c.marks, leaders: c.leaders, ink: c.ink, keys: c.keys || [], warnings: c.warnings, guard: guard, phone: c.phone,
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
  K.FC_ON_DARK = ['label-on-subject', 'on-cat-1', 'on-cat-2', 'on-cat-3', 'chip-label'];
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
    // a leader may end at its own label but never run through one (D3-93)
    (c.leaders || []).forEach(function (l) {
      tx.forEach(function (b) {
        var x0 = b.x + 1.5, x1 = b.x + b.w - 1.5, y0 = b.y + 1.5, y1 = b.y + b.h - 1.5;
        if (x1 <= x0 || y1 <= y0) return;
        var near = function (x, y) { return x > b.x - 4 && x < b.x + b.w + 4 && y > b.y - 4 && y < b.y + b.h + 4; };
        if (near(l.x1, l.y1) || near(l.x2, l.y2)) return;
        if (seg_hits_box(l.x1, l.y1, l.x2, l.y2, x0, y0, x1, y1)) out.push('a leader line crosses "' + b.words.slice(0, 30) + '"');
      });
    });
    return out;
  };
  K.seg_hits_box = seg_hits_box;
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
  // Words: atlas IDs in chips, the figure, the table equivalent
  // ------------------------------------------------------------------------------------------------------------
  K.words = K.words || {};
  // words.json's words, carried inside the kit so a plain page opened from disk prints them too (access S8); the kit's
  // self-test fails when this copy and words.json differ
  K.WORDS = {"source_label": "Source:", "table_summary": "The table and notes", "notes_in_chart": "Notes in the chart", "table_region": "{caption}, table", "unlabeled_marks": "Not labeled at this width: {codes}. The table names every one.", "unlabeled_tiles": "At this width the tiles are too small for state codes. The table names every state.", "scripts_off": "This chart needs JavaScript, which this browser has turned off. Its figures are in the table below.", "export_fonts": "Set in Inter and Inter Tight. On a computer without both fonts, the labels fall back to another font and change width.", "lookup_clear_search": "Clear the search", "lookup_filters": "Filters, {n} on", "lookup_clear_filters": "Clear filters", "lookup_count": "{n} of {total} {noun}"};
  function word(opts, k) {
    var w = (opts && opts.words) || K.words;
    if (k in w) return w[k];
    if (k in K.WORDS) return K.WORDS[k];
    throw new Error('OAChart: words.json has no "' + k + '"; add it there and to K.WORDS in kit.js');
  }
  // the shared words for a form: words.json's, through the same fallback the figure uses (editor's read, K1)
  K.word = function (k) { return word(null, k); };
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
    if (/^(integer|number|percent|signed|points|dollars|signed-dollars)$/.test(base)) {
      var n = t.replace(/[+,%$\s]/g, '').replace(MINUS, '-');
      return /^-?\d+(\.\d+)?$/.test(n) ? n : undefined;
    }
    if (base === 'billions' || base === 'billions-value') {
      var nb = t.replace(/ billion$/, '').replace(/[,\s]/g, '').replace(MINUS, '-');
      return /^-?\d+(\.\d+)?$/.test(nb) ? String(parseFloat(nb) * 1e9) : undefined;
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
    // a column's "empty" word prints where a cell has no value, so a reader can tell none from missing (access S4)
    if ((v === null || v === undefined || v === '') && col.empty) return col.empty;
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
    function num_col(col) { return /^(integer|number|percent|signed|points|thousands|signed-thousands|dollars|signed-dollars|billions)/.test(String(col.format || '')); }
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
  // The compact carrier (fix pass 2): a number column whose printed figures do not give back the stored value (an
  // unrounded value printed rounded once, D3-95) carries its values in the island as one comma-separated list in the
  // table's cell order, so no cell repeats its value in an attribute. K.lean_carry gives the lists; lean_table leaves those
  // cells bare; K.rows_from_table reads them back.
  function carried_fields(spec, rows, types) {
    var tb = spec.table || {}, t = K.table_rows(spec, rows), out = {};
    var numeric = function (f) { var ty = types[f] && types[f].type; return ty === 'number' || ty === 'integer'; };
    var lossy = function (raw, col) {
      if (raw === null || raw === undefined || raw === '') return false;
      var back = K.unformat(visible_text(esc(K.cell_text(col, (function () { var o = {}; o[col.field] = raw; return o; })()))), col);
      return !same_value(back, raw, types[col.field] && types[col.field].type);
    };
    if (t.pivot) {
      var pv = tb.pivot, vcol = { field: pv.value, format: pv.format };
      if (numeric(pv.value) && t.keys.some(function (k) { return t.cols.some(function (cn) { var r = t.cell[k + '\u0000' + cn]; return r && lossy(r[pv.value], vcol); }); })) out[pv.value] = true;
    } else {
      (tb.columns || []).forEach(function (col) {
        if (col.row_header || !numeric(col.field) || col.words || /^lead/.test(String(col.format || ''))) return;
        if (t.rows.some(function (r) { return lossy(r[col.field], col); })) out[col.field] = true;
      });
    }
    return out;
  }
  K.lean_carry = function (spec, rows, types) {
    var fields = carried_fields(spec, rows, types || {}), t = K.table_rows(spec, rows), out = {};
    var ser = function (v) { return v === null || v === undefined || v === '' ? '' : String(v); };
    Object.keys(fields).forEach(function (f) {
      var vals = [];
      if (t.pivot) t.keys.forEach(function (k) { t.cols.forEach(function (cn) { var r = t.cell[k + '\u0000' + cn]; if (r) vals.push(ser(r[f])); }); });
      else t.rows.forEach(function (r) { vals.push(ser(r[f])); });
      out[f] = vals.join(',');
    });
    return out;
  };
  function lean_table(spec, rows, opts) {
    var tb = spec.table || {}, ids = (spec.v7 && spec.v7.ids) || [], types = opts.types || {};
    var carried = opts.carry === false ? {} : carried_fields(spec, rows, types);
    var cap = tb.caption ? '<caption>' + K.chips(tb.caption, ids) + '</caption>' : '';
    var t = K.table_rows(spec, rows), head = '', body = '';
    var num_col = function (col) { return /^(integer|number|percent|signed|points|thousands|signed-thousands|lead|compact-thousands|signed-compact-thousands|dollars|signed-dollars|billions)/.test(String(col.format || '')); };
    var dv = function (raw, html, col) {
      if (carried[col.field]) return '';
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
          // A8 (round 1): a pivot cell with no row is a bare <td></td>; a row whose value prints as nothing carries data-n,
          // the rarer case, so the reader tells the two apart (pages written with data-x on empty cells still read)
          if (!r) return '<td></td>';
          var h = esc(K.fmt(r[pv.value], pv.format)), d = dv(r[pv.value], h, vcol);
          return '<td' + d + (h === '' && !d ? ' data-n' : '') + '>' + h + '</td>';
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
      // a lookup (A9) also searches columns the table does not print: their words ride on the row as data-oa-find
      var lk = spec.lookup && spec.lookup.search, shown = cols.map(function (c) { return c.field; });
      var extra_find = lk ? (lk.fields || []).filter(function (f) { return shown.indexOf(f) < 0; }) : [];
      body = t.rows.map(function (r) {
        var find = extra_find.map(function (f) { return r[f] == null ? '' : String(r[f]); }).join(' ').replace(/\s+/g, ' ').trim();
        return '<tr' + (find ? ' data-oa-find="' + esc(find) + '"' : '') + '>' + cols.map(function (col) {
          var h = K.chips(K.cell_text(col, r), ids), tag = col.row_header ? 'th' : 'td';
          return '<' + tag + (col.row_header ? ' scope="row"' : '') + (num_col(col) ? '' : ' class="t"') + dv(r[col.field], h, col) + '>' + h + '</' + tag + '>';
        }).join('') + '</tr>';
      }).join('');
    }
    return '<table class="oac-table" data-oa-lean>' + cap + '<thead>' + head + '</thead><tbody>' + body + '</tbody></table>';
  }
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
    // the measure line sits under the title, then the reading guide (Rule 13.7, Rule 12.6; brand KS1)
    if (has('measure') && spec.measure_line) p.push('<p class="oac-measure" data-role="measure">' + K.chips(spec.measure_line, ids) + '</p>');
    if (has('guide') && spec.reading_guide) p.push('<p class="oac-guide" data-role="reading-guide">' + K.chips(spec.reading_guide, ids) + '</p>');
    if (has('chart')) {
      var illus = spec.illustrative ? '<p class="oac-illus" data-role="illustrative">' + esc(spec.illustrative) + '</p>' : '';
      p.push('<div class="oac-art" data-oa-art' + (opts.art_attrs || '') + '>' + illus + (opts.svg || '') + '</div>');
      // with scripts off a reader sees the description as words and a line saying the drawing needs scripts; once the
      // script runs, the description names the drawing and leaves the reading order, so it is heard once (D3-97)
      if (spec.alt) p.push('<p class="oac-alt" id="' + id + '-alt" data-role="alt">' + K.chips(spec.alt, ids) + '</p>');
      if (!opts.svg) p.push('<p class="oac-noscript" data-role="scripts-off">' + esc(word(opts, 'scripts_off')) + '</p>');
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
    var cap = (spec.table && spec.table.caption) || spec.title || '';
    var lookup = spec.lookup && !(spec.table && spec.table.pivot) ? K.lookup_html(spec, id, opts) : '';
    if (lookup) p.push(lookup);
    p.push('<details class="oac-eq" data-role="equivalent"' + (opts.svg && !lookup ? '' : ' open') + '><summary>' + esc(word(opts, 'table_summary')) + (cap ? '<span class="oac-vh">: ' + esc(cap) + '</span>' : '') + '</summary>' +
      '<div class="oac-eq-b">' + cn + (opts.guide ? '<div class="oac-tw" role="group" aria-label="' + esc(region) + '">' : '<div class="oac-tw" role="region" tabindex="0" aria-label="' + esc(region) + '">') + K.table_html(spec, rows, { lean: opts.lean_table, types: opts.types }) + '</div></div></details>');
    var fail = spec.failure ? ' data-oa-failure="' + esc(spec.failure.rule || '') + '"' : '';
    var ab = spec.artboard && spec.artboard !== 'reading' ? ' data-oa-artboard="' + esc(spec.artboard) + '"' : '';
    return '<figure class="oac-fig" id="' + id + '" data-oa-chart-id="' + esc(spec.id) + '" data-form="' + esc(spec.form) + '" data-evidence="' + esc(spec.evidence) + '"' + ab + fail + (lookup ? ' data-oa-lookup' : '') + '>' + p.join('') + '</figure>';
  };
  // A lookup (A9, round 1; chapter 18's search, Rule 18.15, and filter bar, Rule 18.16): a search field, a Filters button
  // that opens a sheet of chips, and one status line that counts the rows shown, above the table equivalent, which stays
  // open. The controls carry hidden until the script wires them, so with scripts off, and in print, the whole table shows.
  // spec.lookup: {search: {label, fields}, filters: [{field, label, words}], noun, none}. Within a filter any chip on may
  // match; across filters every filter with a chip on must match; the search matches the row's words and data-oa-find.
  K.lookup_html = function (spec, id, opts) {
    var lk = spec.lookup, cols = (spec.table && spec.table.columns) || [], fields = cols.map(function (c) { return c.field; });
    var lid = id + '-lk', out = ['<div class="oac-lk" data-oa-lookup-controls hidden>'];
    if (lk.search) {
      out.push('<label class="oac-lk-label" for="' + lid + '-q">' + esc(lk.search.label || '') + '</label><div class="oac-lk-box">' +
        '<input class="oac-lk-input" id="' + lid + '-q" type="search" autocomplete="off" spellcheck="false" aria-describedby="' + lid + '-n">' +
        '<button type="button" class="oac-lk-btn oac-lk-clear" hidden>' + esc(word(opts, 'lookup_clear_search')) + '</button></div>');
    }
    var fl = (lk.filters || []).filter(function (f) { return fields.indexOf(f.field) >= 0 && f.words; });
    if (fl.length) {
      out.push('<div class="oac-lk-bar"><button type="button" class="oac-lk-btn oac-lk-toggle" aria-expanded="false" aria-controls="' + lid + '-f">' +
        '<span class="oac-lk-count" data-words="' + esc(word(opts, 'lookup_filters')) + '">' + esc(word(opts, 'lookup_filters').replace('{n}', '0')) + '</span></button>' +
        '<button type="button" class="oac-lk-btn oac-lk-unfilter" hidden>' + esc(word(opts, 'lookup_clear_filters')) + '</button></div><div class="oac-lk-sheet" id="' + lid + '-f" hidden>');
      fl.forEach(function (f, i) {
        out.push('<p class="oac-lk-k" id="' + lid + '-g' + i + '">' + esc(f.label || f.field) + '</p><div class="oac-lk-chips" role="group" aria-labelledby="' + lid + '-g' + i + '" data-col="' + fields.indexOf(f.field) + '">' +
          Object.keys(f.words).map(function (v) { return '<button type="button" class="oac-lk-btn oac-lk-chip" aria-pressed="false">' + esc(f.words[v]) + '</button>'; }).join('') + '</div>');
      });
      out.push('</div>');
    }
    out.push('<p class="oac-lk-status" id="' + lid + '-n" role="status" data-noun="' + esc(lk.noun || '') + '" data-none="' + esc(lk.none || '') + '" data-words="' + esc(word(opts, 'lookup_count')) + '"></p></div>');
    return out.join('');
  };
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
    var last = -1, result = null;
    function draw() {
      var w = K.artboard(spec, t, art.clientWidth || fig.clientWidth);
      if (w === last) return;
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
      if (result.guard.length || result.warnings.length) fig.setAttribute('data-oa-warnings', String(result.guard.length + result.warnings.length));
    }
    draw();
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
  // A plain page (DR-235; access S8): the figure from a spec, the data file's text and its sidecar's columns. The rows are
  // typed, chosen by the spec's where and put in its order, then drawn: OAChart.render(box, spec, csvText, meta.columns)
  K.render = function (box, spec, text, columns, opts) {
    // columns may be the whole sidecar: its columns type the rows and its printed line stands in for a missing source_line
    if (columns && columns.columns) {
      if (!spec.source_line && columns.printed_source_line) spec = Object.assign({}, spec, { source_line: columns.printed_source_line });
      columns = columns.columns;
    }
    var raw = /^\s*\{/.test(text) ? JSON.parse(text).rows : K.parse_csv(text);
    var rows = K.select(spec, K.type_rows(raw, columns || {}));
    box.innerHTML = K.figure(spec, rows, Object.assign({ id: 'oac-' + String(spec.id).toLowerCase(), types: columns }, opts || {}));
    var fig = box.querySelector('figure.oac-fig');
    fig.setAttribute('data-oa-js', '');
    var eq = fig.querySelector('details.oac-eq[open]');
    if (eq) eq.removeAttribute('open');
    return K.mount(fig, spec, rows, opts || {});
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
        opened = Array.prototype.slice.call(root.document.querySelectorAll('figure.oac-fig details.oac-eq:not([open])'));
        opened.forEach(function (d) { d.setAttribute('open', ''); });
      });
      root.addEventListener('afterprint', function () { opened.forEach(function (d) { d.removeAttribute('open'); }); opened = []; });
    }
    if (root.document.readyState === 'loading') root.document.addEventListener('DOMContentLoaded', go); else setTimeout(go, 0);
  }
})(typeof globalThis !== 'undefined' ? globalThis : this);
