// A code block: each panel's Copy button copies that panel's code and says so in the block's status line, with the
// success mark. If the browser refuses, the line turns into an error with "Error:", and the code waits, selected, in a
// text box below it with focus on it, ready to copy by hand. A panel whose code is wider than it becomes a named Tab stop.
(function () {
  document.querySelectorAll('[data-oa-code]').forEach(function (block) {
    var status = block.querySelector('.oa-code-status');
    var words = status.querySelector('.oa-code-words');
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
      status.querySelector('.oa-code-mark--ok').toggleAttribute('hidden', !!error);
      status.querySelector('.oa-code-mark--error').toggleAttribute('hidden', !error);
    }
    block.querySelectorAll('.oa-code-panel').forEach(function (panel) {
      var button = panel.querySelector('.oa-code-copy');
      var pre = panel.querySelector('.oa-code-pre');
      var lang = panel.querySelector('.oa-code-lang');
      // a panel that scrolls takes a Tab stop and a name, so the arrow keys can scroll it
      function fit() {
        if (pre.scrollWidth > pre.clientWidth + 1) {
          pre.setAttribute('tabindex', '0');
          pre.setAttribute('role', 'group');
          pre.setAttribute('aria-label', lang.textContent + '. Scroll sideways to see all of it.');
        } else {
          ['tabindex', 'role', 'aria-label'].forEach(function (k) { pre.removeAttribute(k); });
        }
      }
      fit();
      if (window.ResizeObserver) new ResizeObserver(fit).observe(pre);
      button.addEventListener('click', function () {
        var text = pre.textContent;
        var lines = text.replace(/\n$/, '').split('\n').length;
        var old = block.querySelector('.oa-code-fallback');
        if (old) old.remove();
        function done() {
          say('Copied ' + button.getAttribute('data-oa-copy-what') + ', ' + lines + (lines === 1 ? ' line' : ' lines') + ', to the clipboard.', false);
        }
        function fail() {
          say('The browser blocked copying. The text is selected below: press Control and C, or Command and C.', true);
          var box = document.createElement('textarea');
          box.className = 'oa-code-fallback';
          box.readOnly = true;
          box.rows = Math.min(lines, 8);
          box.value = text;
          box.setAttribute('aria-label', 'Text to copy');
          status.insertAdjacentElement('afterend', box);
          box.focus();
          box.select();
        }
        if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(done, fail);
        else fail();
      });
    });
  });
})();
