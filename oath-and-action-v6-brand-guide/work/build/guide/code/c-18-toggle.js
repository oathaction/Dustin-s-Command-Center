// Toggle buttons and filter chips: each press flips aria-pressed, and the status line after the control says what
// changed in words. A chip group names every chip that is on.
(function () {
  function statusAfter(el) {
    for (var n = el.nextElementSibling; n; n = n.nextElementSibling) if (n.classList.contains('oa-toggle-status')) return n;
    return null;
  }
  // "Housing", "Housing and Elections", "Housing, Health care and Elections"
  function list(words) {
    return words.length < 2 ? words.join('') : words.slice(0, -1).join(', ') + ' and ' + words[words.length - 1];
  }
  document.querySelectorAll('[data-oa-toggle]').forEach(function (set) {
    set.querySelectorAll('.oa-toggle').forEach(function (button) {
      button.addEventListener('click', function () {
        if (button.getAttribute('aria-disabled') === 'true') return;
        var on = button.getAttribute('aria-pressed') !== 'true';
        button.setAttribute('aria-pressed', String(on));
        var group = button.closest('.oa-toggle-chips');
        var status = statusAfter(group || button);
        if (!status) return;
        if (group) {
          var names = [];
          group.querySelectorAll('.oa-toggle[aria-pressed="true"] .oa-toggle-label').forEach(function (l) { names.push(l.textContent.trim()); });
          status.textContent = names.length ? group.getAttribute('data-oa-say-some') + ' ' + list(names) + '.' : group.getAttribute('data-oa-say-none');
        } else {
          status.textContent = button.getAttribute(on ? 'data-oa-say-on' : 'data-oa-say-off');
        }
      });
    });
  });
})();
