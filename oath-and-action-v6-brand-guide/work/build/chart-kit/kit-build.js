/* Oath & Action chart kit, the builder's half (round 3 fix pass, call 10). Load after kit.js, in Node and on a plain page
 * opened from disk (README, "A plain page"); the guide's page never carries it, since its figures, tables and words are
 * written at build and the page only draws, reads its rows back and checks itself (kit.js). It holds: the figure's HTML
 * (K.figure, K.lookup_html), the table equivalent (K.table_html, K.table_rows, K.table_groups, K.group_cell,
 * K.cell_text, K.lean_carry), atlas IDs in chips (K.chips, K.fill_words), K.lead, the plain page's K.render and the rows
 * it keeps (K.select: a page's island holds its rows already chosen), tokens read from tokens.css (K.tokens_from_css)
 * and words.json's copy (K.WORDS). Moved here whole from kit.js; nothing changed. */
(function (root) {
  'use strict';
  var K = root.OAChart, P = K._p;
  var esc = P.esc, word = P.word, fixed = P.fixed, group = P.group, signed = P.signed, PHONE_VIEW_PX = P.PHONE_VIEW_PX;

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
      // A12 (second pass): "values" gives an order of its own, [{"field": "reform_group", "values": ["G1", "G2"]}]; a value
      // it does not list sorts after those it does, in the data's order
      var order = Array.isArray(s.values) ? s.values.map(String) : null;
      var rank = function (v) { var i = order.indexOf(String(v)); return i < 0 ? order.length : i; };
      out = out.map(function (r, i) { return [r, i]; }).sort(function (a, b) {
        var x = a[0][s.field], y = b[0][s.field];
        if (order) return (rank(x) - rank(y)) * dir || a[1] - b[1];
        if (x === y) return a[1] - b[1];
        if (x === null) return 1;
        if (y === null) return -1;
        return (x < y ? -1 : 1) * dir;
      }).map(function (p) { return p[0]; });
    });
    return after();
  };
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

  // words.json's words, carried inside the kit so a plain page opened from disk prints them too (access S8); the kit's
  // self-test fails when this copy and words.json differ
  K.WORDS = {"source_label": "Source:", "table_summary": "The table and notes", "notes_in_chart": "Notes in the chart", "table_region": "{caption}, table", "unlabeled_marks": "Not labeled at this width: {codes}. The table names every one.", "unlabeled_tiles": "At this width the tiles are too small for state codes. The table names every state.", "scripts_off": "This chart needs JavaScript, which this browser has turned off. Its figures are in the table below.", "export_fonts": "Set in Inter and Inter Tight. On a computer without both fonts, the labels fall back to another font and change width.", "lookup_clear_search": "Clear the search", "lookup_filters": "Filters, {n} on", "lookup_clear_filters": "Clear filters", "lookup_count": "{n} of {total} {noun}", "phone_view": "On a phone, {w} px", "phone_view_part": "On a phone, {w} px: {part}", "phone_view_rows": "the first {n} of {total} rows; a phone draws them all", "stage_scroll": "The drawing at its full width, {w} px; scroll sideways to see all of it", "data_file": "this chart’s data file in the guide’s asset package"};

  // ST-M2 item 1 (round 3 fix pass): "{data_file}" in a caption or note prints words.json's data_file, the one place
  // that names where a chart's full rows live, so Dustin's answer changes one string and no spec
  K.fill_words = function (text) { return String(text).split('{data_file}').join(word(null, 'data_file')); };
  K.chips = function (text, ids) {
    // set each atlas ID the spec names (spec.v7.ids) in its typed chip; an ASCII hyphen, never U+2011, in a no-wrap span
    var s = esc(K.fill_words(text));
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
    // R3-3 (round 3, DR-249): a grouped table prints one row a group; every data row falls in one, and the island and the
    // CSV export carry every row
    if (tb.group) return { pivot: false, rows: rows, group: true, groups: K.table_groups(spec, rows) };
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

  function text_col(col) { return !col.format || col.format === 'text'; }
  // RB-G5 (round 2 fix pass): a pivot's row header prints its column's words where the column gives them ("100" as "100
  // and over"), as any cell does; the lean table carries the stored value in data-v for the read-back
  // C-E7 (round 3 fix pass): a pivot's cell of format text takes the spec's typography, as an ungrouped table's text
  // columns do (S84's "..." prints "No state law"); the lean table's read-back compares it with the typeset value
  function pivot_cell(spec, r, pv) {
    var t = K.fmt(r[pv.value], pv.format);
    return spec.typography && text_col({ format: pv.format }) ? K.typeset(spec, t) : t;
  }
  function pivot_head(rc, v) {
    if (rc.words && v !== null && v !== undefined && rc.words[String(v)] !== undefined) return String(rc.words[String(v)]);
    return K.fmt(v, rc.format);
  }
  K.cell_text = function (col, r, spec) {
    if (spec && spec.typography && text_col(col)) return K.typeset(spec, K.cell_text(col, r));
    var v = r[col.field];
    // a column's "empty" word prints where a cell has no value, so a reader can tell none from missing (access S4)
    if ((v === null || v === undefined || v === '') && col.empty) return col.empty;
    var lm = /^lead(?::(\d+))?$/.exec(String(col.format || ''));
    if (lm) return K.lead(v, col.lead, lm[1] ? +lm[1] : 0);
    if (col.words && v !== null && v !== undefined && col.words[String(v)] !== undefined) return col.words[String(v)];
    return K.fmt(v, col.format);
  };
  // MA-9: a column's words, {group key: words}, print in place of its aggregate for those groups (any agg).
  // R3-3 (round 3, DR-249): a table grouped by a column, for a chart of thousands of rows (a county map): table.group =
  // {by: a column, or a list of columns whose values join with ", " (A-E1), sort: 'key' or 'name' (else first seen, after the spec's sort), columns: [{label, agg, field, format, words, state_name, row_header,
  // from, to, name}]}. agg: 'key' (the group's value, its words, or with state_name the state's name from the tile grid),
  // 'count' (rows in the group), 'count_in' (rows whose field is at least from and under to; either may be left out),
  // 'count_eq' (rows whose field equals value, or any value of a list: C-E1), 'count_set' (rows whose field is not
  // empty), 'list' (the field's values joined with "; "; distinct, odd and with: A-E5, A-E6), 'min',
  // 'max', 'median', 'sum', 'first', and 'min_name' or 'max_name' (the name column of the row with the least or most of
  // field). The page prints one row a group; the island carries every row the drawing reads, and the CSV export every row
  // (table.columns names them). Its rows are not read back from the table.
  // A-E1 (maker A): by may be a list of columns; the group's key is their values joined with ", " ("Senate, D")
  K.table_groups = function (spec, rows) {
    var g = spec.table.group, keys = [], map = {}, by = [].concat(g.by);
    rows.forEach(function (r) { var k = by.map(function (f) { return String(r[f]); }).join(', '); if (!(k in map)) { map[k] = []; keys.push(k); } map[k].push(r); });
    if (g.sort === 'key') keys.sort();
    var out = keys.map(function (k) { return { key: k, rows: map[k] }; });
    // ST-S9, AX-S4, C-S4 (round 3 fix pass, D3-1320): sort 'name' orders the groups by the words the key column prints
    // (a state's name, or the column's words); sort 'key' does the same where the key column prints a state's name, so
    // "Alabama" comes before "Alaska" as a reader scanning the names expects. Case folded, then by code point, so Node
    // and every browser give one order
    var kc = (g.columns || []).filter(function (c) { return (c.agg || 'key') === 'key'; })[0];
    if (kc && (g.sort === 'name' || (g.sort === 'key' && kc.state_name))) {
      var nm = function (grp) { return String(K.group_cell(kc, grp)).toLowerCase(); };
      out.forEach(function (grp) { grp.name = nm(grp); });
      out.sort(function (a, b) { return a.name < b.name ? -1 : a.name > b.name ? 1 : (a.key < b.key ? -1 : a.key > b.key ? 1 : 0); });
      out.forEach(function (grp) { delete grp.name; });
    }
    return out;
  };
  var GROUP_NUM = /^(count|count_in|count_eq|count_set|min|max|median|sum)$/;
  K.group_cell = function (col, grp) {
    var f = col.field, rs = grp.rows, ok = function (v) { return v !== null && v !== undefined && v !== '' && isFinite(+v); };
    var vals = rs.filter(function (r) { return ok(r[f]); });
    var nums = vals.map(function (r) { return +r[f]; });
    var a = col.agg || 'key';
    // MA-9 (round 3): any column's words, keyed by the group's key, print in place of its aggregate for that group (a
    // court whose list stands for every state)
    if (a !== 'key' && col.words && col.words[grp.key] !== undefined) return col.words[grp.key];
    if (a === 'key') {
      if (col.state_name && root.OAChartGeo && root.OAChartGeo.tiles && root.OAChartGeo.tiles[grp.key]) return root.OAChartGeo.tiles[grp.key][3];
      return col.words && col.words[grp.key] !== undefined ? col.words[grp.key] : grp.key;
    }
    // ST-M1, AX-M1 (round 3 fix pass): 'first' prints the group's first row through K.cell_text whatever its type, text
    // as well as numbers (its words and its empty word included); it sat below the numeric guard and printed nothing
    // for a text field
    if (a === 'first') return K.cell_text(col, rs[0]);
    if (a === 'count') return K.fmt(rs.length, col.format || 'integer');
    // A-E2 (maker A): 'list', the field's non-empty values in the group in row order joined with "; "; 'count_set', the
    // rows whose field is not empty
    if (a === 'list') {
      // A-E6: odd names a field; only the rows whose value of it differs from the group's most common value are listed
      // (every row where no one value is most common); with adds those fields in parentheses after each ("Cuellar (TX,
      // Yea)"). A-E5: distinct lists each entry once, in first-seen order
      var lr = rs;
      if (col.odd) {
        var tally = {}, top = 0, tops = 0;
        rs.forEach(function (r) { var k = String(r[col.odd]); tally[k] = (tally[k] || 0) + 1; });
        Object.keys(tally).forEach(function (k) { if (tally[k] > top) { top = tally[k]; tops = 1; } else if (tally[k] === top) tops++; });
        var common = tops === 1 ? Object.keys(tally).filter(function (k) { return tally[k] === top; })[0] : null;
        lr = common === null ? rs : rs.filter(function (r) { return String(r[col.odd]) !== common; });
      }
      var items = lr.filter(function (r) { return r[f] !== null && r[f] !== undefined && r[f] !== ''; }).map(function (r) {
        var extra = [].concat(col.with || []).map(function (w) { return r[w]; }).filter(function (v) { return v !== null && v !== undefined && v !== ''; });
        return String(r[f]) + (extra.length ? ' (' + extra.join(', ') + ')' : '');
      });
      if (col.distinct) items = items.filter(function (x, i) { return items.indexOf(x) === i; });
      return items.join('; ') || col.empty || '';
    }
    if (a === 'count_set') return K.fmt(rs.filter(function (r) { return r[f] !== null && r[f] !== undefined && r[f] !== ''; }).length, col.format || 'integer');
    // C-E1 (cartographer): rows whose field equals value (or any of a list of values)
    if (a === 'count_eq') { var want = [].concat(col.value).map(String); return K.fmt(rs.filter(function (r) { return want.indexOf(String(r[f])) >= 0; }).length, col.format || 'integer'); }
    if (a === 'count_in') return K.fmt(nums.filter(function (v) { return (col.from === undefined || col.from === null || v >= col.from) && (col.to === undefined || col.to === null || v < col.to); }).length, col.format || 'integer');
    if (!nums.length) return col.empty || '';
    if (a === 'min' || a === 'min_name' || a === 'max' || a === 'max_name') {
      var best = vals[0];
      vals.forEach(function (r) { if (/^min/.test(a) ? +r[f] < +best[f] : +r[f] > +best[f]) best = r; });
      return /_name$/.test(a) ? String(best[col.name || 'name']) : K.fmt(best[f], col.format);
    }
    if (a === 'sum') return K.fmt(nums.reduce(function (t, v) { return t + v; }, 0), col.format);
    if (a === 'median') { var v = nums.slice().sort(function (x, y) { return x - y; }), m = v.length; return K.fmt(m % 2 ? v[(m - 1) / 2] : (v[m / 2 - 1] + v[m / 2]) / 2, col.format); }
    return '';
  };
  function group_table(spec, rows) {
    // set as the lean table is: numbers bare, words in class t
    var tb = spec.table, g = tb.group, ids = (spec.v7 && spec.v7.ids) || [], cols = g.columns || [];
    var cap = tb.caption ? '<caption>' + K.chips(tb.caption, ids) + '</caption>' : '';
    var numc = function (col) { return GROUP_NUM.test(col.agg || '') || /^(integer|number|percent|fraction-percent|dollars|thousands)/.test(String(col.format || '')); };
    var head = '<tr>' + cols.map(function (col) { return '<th scope="col"' + (numc(col) ? '' : ' class="t"') + '>' + K.chips(col.label, ids) + '</th>'; }).join('') + '</tr>';
    var body = K.table_groups(spec, rows).map(function (grp) {
      return '<tr>' + cols.map(function (col) {
        // A-E7 (maker A): a grouped table's words take the spec's typography, as an ungrouped table's text columns do
        var raw = K.group_cell(col, grp);
        if (spec.typography && !numc(col)) raw = K.typeset(spec, raw);
        var txt = esc(raw), hd = col.row_header || (col.agg || 'key') === 'key';
        return '<' + (hd ? 'th scope="row"' : 'td') + (numc(col) ? '' : ' class="t"') + '>' + txt + '</' + (hd ? 'th' : 'td') + '>';
      }).join('') + '</tr>';
    }).join('');
    return '<table class="oac-table" data-oa-group>' + cap + '<thead>' + head + '</thead><tbody>' + body + '</tbody></table>';
  }
  K.table_html = function (spec, rows, opts) {
    if (spec.table && spec.table.group) return group_table(spec, rows);
    if (opts && opts.lean) return lean_table(spec, rows, opts);
    var tb = spec.table || {}, ids = (spec.v7 && spec.v7.ids) || [];
    var cap = tb.caption ? '<caption>' + K.chips(tb.caption, ids) + '</caption>' : '';
    var t = K.table_rows(spec, rows), head = '', body = '';
    function num_col(col) { return /^(integer|number|percent|fraction-percent|signed|points|thousands|signed-thousands|dollars|signed-dollars|billions|millions)/.test(String(col.format || '')); }
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
          return '<td class="oac-num"' + (r ? ' data-oa-row="1"' : '') + '>' + (r ? esc(pivot_cell(spec, r, pv)) : '') + '</td>';
        }).join('');
        var rows_by = [].concat(pv.row), head_txt = first ? pivot_head(rc, first[rows_by[0]]) : k;
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
          var txt = K.chips(K.cell_text(col, r, spec), ids);
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
    if (spec.table && spec.table.group) return {};
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
    var num_col = function (col) { return /^(integer|number|percent|fraction-percent|signed|points|thousands|signed-thousands|lead|compact-thousands|signed-compact-thousands|dollars|signed-dollars|billions|millions)/.test(String(col.format || '')); };
    var dv = function (raw, html, col) {
      if (carried[col.field]) return '';
      var back = K.unformat(visible_text(html), col);
      // a text cell set by the spec's typography reads back as the printed words, which draw the same (D3-519)
      var want = spec.typography && text_col(col) && raw !== null && raw !== undefined ? K.typeset(spec, raw) : raw;
      return same_value(back, want, types[col.field] && types[col.field].type) ? '' : ' data-v="' + esc(raw === null || raw === undefined ? '' : raw) + '"';
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
          var h = esc(pivot_cell(spec, r, pv)), d = dv(r[pv.value], h, vcol);
          return '<td' + d + (h === '' && !d ? ' data-n' : '') + '>' + h + '</td>';
        }).join('');
        var head_txt = first ? pivot_head(rc, first[rows_by[0]]) : k;
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
          var h = K.chips(K.cell_text(col, r, spec), ids), tag = col.row_header ? 'th' : 'td';
          return '<' + tag + (col.row_header ? ' scope="row"' : '') + (num_col(col) ? '' : ' class="t"') + dv(r[col.field], h, col) + '>' + h + '</' + tag + '>';
        }).join('') + '</tr>';
      }).join('');
    }
    return '<table class="oac-table" data-oa-lean>' + cap + '<thead>' + head + '</thead><tbody>' + body + '</tbody></table>';
  }

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
      // D3-487 (BC S3, ED-E10): a form that changes on a phone also shows its phone drawing to a reader at a desk, drawn
      // from the same rows at a fixed 358 px under the desktop drawing; hidden where the figure is itself phone width
      // A17 (D3-534): desk_phone {rows, part} draws it from the first rows only, where the whole phone drawing would run far
      // longer than the desktop one, and says so; a phone still draws every row
      var dp = spec.desk_phone && +spec.desk_phone.rows > 0 ? spec.desk_phone : null;
      var pk = dp ? word(opts, 'phone_view_part').replace('{part}', dp.part || word(opts, 'phone_view_rows').replace('{n}', String(+dp.rows)).replace('{total}', String((rows || []).length)))
        : word(opts, 'phone_view');
      if (spec.phone_view && !opts.svg) p.push('<div class="oac-art oac-art-phone" data-oa-art-phone="' + PHONE_VIEW_PX + '"' + (dp ? ' data-oa-rows="' + (+dp.rows) + '"' : '') + '><p class="oac-phone-k">' +
        esc(pk.replace('{w}', String(PHONE_VIEW_PX))) + '</p></div>');
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
})(typeof globalThis !== 'undefined' ? globalThis : this);
