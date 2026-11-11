// Tabs with automatic activation: the arrow keys, Home and End move between tabs and show each panel at once. Only the
// selected tab is in the Tab order, and Tab moves on to its panel. An unavailable tab takes focus but never shows a panel.
(function () {
  document.querySelectorAll('[data-oa-tabs]').forEach(function (box) {
    var tabs = Array.prototype.slice.call(box.querySelectorAll('[role="tab"]'));
    function panelOf(tab) { return document.getElementById(tab.getAttribute('aria-controls')); }
    function select(tab) {
      tabs.forEach(function (t) {
        var on = t === tab;
        t.setAttribute('aria-selected', String(on));
        var p = panelOf(t);
        if (p) p.hidden = !on;
      });
    }
    // focus moves to any tab; the Tab order and the panel follow only a tab that can be chosen
    function move(tab) {
      tab.focus();
      if (tab.getAttribute('aria-disabled') === 'true') return;
      tabs.forEach(function (t) { t.setAttribute('tabindex', t === tab ? '0' : '-1'); });
      select(tab);
    }
    tabs.forEach(function (tab, i) {
      tab.addEventListener('click', function () { move(tab); });
      tab.addEventListener('keydown', function (e) {
        var next = null;
        if (e.key === 'ArrowRight') next = tabs[(i + 1) % tabs.length];
        else if (e.key === 'ArrowLeft') next = tabs[(i - 1 + tabs.length) % tabs.length];
        else if (e.key === 'Home') next = tabs[0];
        else if (e.key === 'End') next = tabs[tabs.length - 1];
        if (!next) return;
        e.preventDefault();
        move(next);
      });
    });
  });
})();
