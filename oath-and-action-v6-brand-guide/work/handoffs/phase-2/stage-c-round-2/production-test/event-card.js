// Event sign-up card (production test, DR-219). Built from Rule 18.17's form script, Rule 18.1's unavailable button
// and Rule 18.4's theme switch, as the chapters page prints them. Illustrative event; the send is a stand-in.

// Rule 18.4's switch script, copied as printed.
(function () {
  var KEY = 'oa-theme';
  function stored() {
    try { var t = localStorage.getItem(KEY); return t === 'light' || t === 'dark' ? t : null; } catch (e) { return null; }
  }
  function store(value) {
    try { if (value === 'light' || value === 'dark') localStorage.setItem(KEY, value); else localStorage.removeItem(KEY); } catch (e) {}
  }
  function targetOf(box) {
    var id = box.getAttribute('data-oa-theme-for');
    return id ? document.getElementById(id) : document.documentElement;
  }
  function show(box, value) {
    var input = box.querySelector('.oa-theme-input[value="' + (value === 'light' || value === 'dark' ? value : 'device') + '"]');
    if (input) input.checked = true;
  }
  var boxes = Array.prototype.slice.call(document.querySelectorAll('.oa-theme'));
  boxes.forEach(function (box) {
    var target = targetOf(box);
    if (!target) return;
    var root = target === document.documentElement;
    var now = target.getAttribute('data-oa-theme');
    if (root && now !== 'light' && now !== 'dark') {
      now = stored();
      if (now) target.setAttribute('data-oa-theme', now);
    }
    show(box, now);
    box.addEventListener('change', function (event) {
      var value = event.target.value;
      target.setAttribute('data-oa-theme', value);
      if (root) store(value);
      boxes.forEach(function (other) { if (other !== box && targetOf(other) === target) show(other, value); });
    });
  });
})();

// The sign-up form: Rule 18.17's pattern, with a name check, the "Sending" word of Rule 18.1 and the seat count.
(function () {
  var CHECKS = {
    name: function (v) { return /[\p{L}\p{N}]/u.test(v); },
    email: function (v) { return /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v); }
  };
  // Replace this with your own request. It calls done() once the server has the form.
  function send(form, done) { setTimeout(done, 800); }

  document.querySelectorAll('[data-ev-form]').forEach(function (form) {
    var ask = form.querySelector('.ev-send');
    var status = form.querySelector('.ev-status');
    var fields = Array.prototype.slice.call(form.querySelectorAll('[data-ev-check]'));
    var word = ask.textContent;
    function errorOf(input) { return document.getElementById(input.id + '-error'); }
    function mark(input, bad) {
      var error = errorOf(input);
      var ids = (input.getAttribute('aria-describedby') || '').split(' ').filter(function (x) { return x && x !== error.id; });
      if (bad) {
        input.setAttribute('aria-invalid', 'true');
        ids.push(error.id);
        error.hidden = false;
        error.setAttribute('data-red', 'working');
        error.setAttribute('data-red-job', 'error');
      } else {
        input.removeAttribute('aria-invalid');
        error.hidden = true;
        error.removeAttribute('data-red');
        error.removeAttribute('data-red-job');
      }
      if (ids.length) input.setAttribute('aria-describedby', ids.join(' '));
      else input.removeAttribute('aria-describedby');
    }
    function check(input) {
      var bad = !CHECKS[input.getAttribute('data-ev-check')](input.value.trim());
      mark(input, bad);
      return bad;
    }
    // the error holds the red; once no field is in error, the red goes back to the ask
    function red() {
      if (!fields.length) return;
      var any = fields.some(function (f) { return f.getAttribute('aria-invalid') === 'true'; });
      if (any) {
        ask.setAttribute('data-oa-yield', '');
        ask.removeAttribute('data-red');
        ask.removeAttribute('data-red-job');
      } else {
        ask.removeAttribute('data-oa-yield');
        ask.setAttribute('data-red', 'working');
        ask.setAttribute('data-red-job', 'take part now');
      }
    }
    function say(template) {
      if (!status) return;
      status.textContent = '';
      if (template) status.appendChild(form.querySelector(template).content.cloneNode(true));
    }
    fields.forEach(function (input) {
      input.addEventListener('input', function () {
        if (input.getAttribute('aria-invalid') === 'true') { check(input); red(); }
      });
    });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      // Rule 18.1: an unavailable button keeps focus, and a press does nothing
      if (ask.getAttribute('aria-disabled') === 'true') return;
      var first = null;
      fields.forEach(function (input) { if (check(input) && !first) first = input; });
      red();
      if (first) {
        say(null);
        first.focus();
        return;
      }
      ask.setAttribute('aria-disabled', 'true');
      ask.textContent = 'Sending';
      if (status && status.id) ask.setAttribute('aria-describedby', status.id);
      say('.ev-say-sending');
      send(form, function () {
        ask.removeAttribute('aria-disabled');
        ask.removeAttribute('aria-describedby');
        ask.textContent = word;
        var seats = form.closest('.ev-card').querySelector('[data-ev-seats]');
        if (seats) seats.textContent = String(Math.max(0, parseInt(seats.textContent, 10) - 1));
        say('.ev-say-done');
        form.reset();
      });
    });
  });
})();
