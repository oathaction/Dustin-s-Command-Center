// A scroll region: while its content is wider than the frame, the frame takes a Tab stop (so the arrow keys scroll it),
// the role of a named group and its hint; when the content fits, all three go. It checks again whenever its size changes.
(function () {
  document.querySelectorAll('[data-oa-scroll]').forEach(function (box) {
    var frame = box.querySelector('.oa-scroll-frame');
    var hint = box.querySelector('.oa-scroll-hint');
    var name = box.querySelector('.oa-scroll-k');
    if (!frame) return;
    function check() {
      var over = frame.scrollWidth > frame.clientWidth + 1;
      if (over) {
        frame.setAttribute('tabindex', '0');
        frame.setAttribute('role', 'group');
        if (name && name.id) frame.setAttribute('aria-labelledby', name.id);
      } else {
        frame.removeAttribute('tabindex');
        frame.removeAttribute('role');
        frame.removeAttribute('aria-labelledby');
      }
      if (hint) hint.hidden = !over;
    }
    check();
    if (window.ResizeObserver) {
      var watch = new ResizeObserver(check);
      watch.observe(frame);
      if (frame.firstElementChild) watch.observe(frame.firstElementChild);
    } else {
      window.addEventListener('resize', check);
    }
  });
})();
