// Copy a value: each Copy button copies the value in its row and says so in the status line, with the success mark.
// If the browser refuses, the line shows the error mark and "Error:", and the value waits, selected, in a field below
// it with focus on it, ready to copy by hand.
(function () {
  document.querySelectorAll('[data-oa-copy]').forEach(function (box) {
    var status = box.querySelector('.oa-copy-status');
    var words = status.querySelector('.oa-copy-words');
    function say(text, error) {
      words.textContent = '';
      if (error) {
        var b = document.createElement('b');
        b.textContent = 'Error:';
        words.appendChild(b);
        words.appendChild(document.createTextNode(' ' + text));
        status.setAttribute('data-oa-state', 'error');
        status.setAttribute('data-red', 'working');
        status.setAttribute('data-red-job', 'error');
      } else {
        words.textContent = text;
        status.removeAttribute('data-oa-state');
        status.removeAttribute('data-red');
        status.removeAttribute('data-red-job');
      }
      status.querySelector('.oa-copy-mark--ok').toggleAttribute('hidden', !!error);
      status.querySelector('.oa-copy-mark--error').toggleAttribute('hidden', !error);
    }
    box.querySelectorAll('.oa-copy-row').forEach(function (row) {
      var button = row.querySelector('.oa-copy-button');
      var value = row.querySelector('.oa-copy-value').textContent.trim();
      // "Copied #121212, Charcoal." names the value and what it is, from the button's own hidden words
      var named = button.querySelector('.oa-copy-vh').textContent.trim();
      button.addEventListener('click', function () {
        var old = box.querySelector('.oa-copy-fallback');
        if (old) old.remove();
        function done() { say('Copied ' + named + '.', false); }
        function fail() {
          say('The browser blocked copying. The value is selected below: press Control and C, or Command and C.', true);
          var field = document.createElement('input');
          field.className = 'oa-copy-fallback';
          field.readOnly = true;
          field.value = value;
          field.setAttribute('aria-label', 'Value to copy');
          status.insertAdjacentElement('afterend', field);
          field.focus();
          field.select();
        }
        if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(value).then(done, fail);
        else fail();
      });
    });
  });
})();
