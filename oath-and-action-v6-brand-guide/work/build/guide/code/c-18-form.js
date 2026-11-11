// A form with the error pattern (Rule 11.15). On send, each field is checked; a field that fails takes aria-invalid,
// points to its message and draws the red bar, focus moves to the first field to fix, and the ask yields its red
// (Rule 11.16). A field in error is checked again as the reader types, so the red returns to the ask once all are
// fixed. A good send says "Sending" in the status line, keeps the ask unavailable while it runs, then says what happened.
(function () {
  var CHECKS = {
    email: function (v) { return /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v); },
    zip: function (v) { return /^[0-9]{5}$/.test(v); }
  };
  // Replace this with your own request. It calls done() once the server has the form.
  function send(form, done) { setTimeout(done, 800); }

  document.querySelectorAll('[data-oa-form]').forEach(function (form) {
    var ask = form.querySelector('.oa-form-send');
    var status = form.querySelector('.oa-form-status');
    var fields = Array.prototype.slice.call(form.querySelectorAll('[data-oa-check]'));
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
      var bad = !CHECKS[input.getAttribute('data-oa-check')](input.value.trim());
      mark(input, bad);
      return bad;
    }
    // the error holds the red; once no field is in error, the red goes back to the ask
    function red() {
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
      if (status.id) ask.setAttribute('aria-describedby', status.id);
      say('.oa-form-say-sending');
      send(form, function () {
        ask.removeAttribute('aria-disabled');
        ask.removeAttribute('aria-describedby');
        say('.oa-form-say-done');
      });
    });
  });
})();
