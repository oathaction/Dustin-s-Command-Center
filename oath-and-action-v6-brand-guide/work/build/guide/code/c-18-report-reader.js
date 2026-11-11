// Report reader. Previous page and Next page turn one page at a time and write "Page 2 of 4: What a mile of road
// costs" to the status line. At the first or last page the button keeps focus, takes aria-disabled and points to the
// line that says why. Fit width and Full size set the page's size; while the page is wider than its view, the view
// takes a Tab stop, a name and its hint, so the arrow keys can scroll it.
(function () {
  document.querySelectorAll('[data-oa-reader]').forEach(function (box) {
    var view = box.querySelector('.oa-reader-view');
    var pages = Array.prototype.slice.call(view.querySelectorAll('.oa-reader-page'));
    var prev = box.querySelector('.oa-reader-prev');
    var next = box.querySelector('.oa-reader-next');
    var status = box.querySelector('.oa-reader-status');
    var why = box.querySelector('.oa-reader-why');
    var hint = box.querySelector('.oa-reader-hint');
    var n = 0;
    function off(button, unavailable) {
      if (unavailable) {
        button.setAttribute('aria-disabled', 'true');
        button.setAttribute('aria-describedby', why.id);
      } else {
        button.removeAttribute('aria-disabled');
        button.removeAttribute('aria-describedby');
      }
    }
    function draw() {
      pages.forEach(function (p, i) { p.hidden = i !== n; });
      status.textContent = 'Page ' + (n + 1) + ' of ' + pages.length + ': ' + pages[n].getAttribute('data-oa-title');
      off(prev, n === 0);
      off(next, n === pages.length - 1);
      why.textContent = n === 0 ? 'This is the first page.' : (n === pages.length - 1 ? 'This is the last page.' : '');
    }
    function fit() {
      var over = view.scrollWidth > view.clientWidth + 1;
      if (over) {
        view.setAttribute('tabindex', '0');
        view.setAttribute('role', 'group');
        view.setAttribute('aria-label', 'The report page');
      } else {
        ['tabindex', 'role', 'aria-label'].forEach(function (k) { view.removeAttribute(k); });
      }
      hint.hidden = !over;
    }
    prev.addEventListener('click', function () { if (n > 0) { n--; draw(); } });
    next.addEventListener('click', function () { if (n < pages.length - 1) { n++; draw(); } });
    box.querySelectorAll('.oa-reader-size-input').forEach(function (input) {
      input.addEventListener('change', function () {
        view.setAttribute('data-oa-size', input.value);
        fit();
      });
    });
    draw();
    fit();
    if (window.ResizeObserver) new ResizeObserver(fit).observe(view);
  });
})();
