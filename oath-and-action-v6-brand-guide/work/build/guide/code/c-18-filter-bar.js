// Filter bar. Filters opens and closes the sheet of chips (aria-expanded), and its name counts the chips that are on.
// Within a group, chips widen the list (any one may match); across groups, each group that has a chip on must match.
// The status line gives the count, with its advice when nothing matches. Clear filters turns every chip off, hides
// itself and sends focus to Filters, since the button the reader pressed is gone.
(function () {
  document.querySelectorAll('[data-oa-filters]').forEach(function (box) {
    var toggle = box.querySelector('.oa-filters-toggle');
    var sheet = document.getElementById(toggle.getAttribute('aria-controls'));
    var count = box.querySelector('.oa-filters-count');
    var clear = box.querySelector('.oa-filters-clear');
    var status = box.querySelector('.oa-filters-status');
    var chips = Array.prototype.slice.call(box.querySelectorAll('.oa-filters-chip'));
    var groups = Array.prototype.slice.call(box.querySelectorAll('[data-oa-group]'));
    var items = Array.prototype.slice.call(box.querySelectorAll('.oa-filters-result'));
    function on(chip) { return chip.getAttribute('aria-pressed') === 'true'; }
    function run() {
      var n = 0;
      items.forEach(function (li) {
        var hit = groups.every(function (g) {
          var wanted = Array.prototype.filter.call(g.querySelectorAll('.oa-filters-chip'), on).map(function (c) { return c.getAttribute('data-oa-filter'); });
          return !wanted.length || wanted.indexOf(li.getAttribute('data-oa-' + g.getAttribute('data-oa-group'))) >= 0;
        });
        li.hidden = !hit;
        if (hit) n++;
      });
      var k = chips.filter(on).length;
      count.textContent = 'Filters, ' + k + ' on';
      clear.hidden = !k;
      status.textContent = n + ' of ' + items.length + ' ' + status.getAttribute('data-oa-noun') + (n ? '' : '. ' + status.getAttribute('data-oa-none'));
    }
    toggle.addEventListener('click', function () {
      var open = toggle.getAttribute('aria-expanded') !== 'true';
      toggle.setAttribute('aria-expanded', String(open));
      if (sheet) sheet.hidden = !open;
    });
    chips.forEach(function (chip) {
      chip.addEventListener('click', function () {
        chip.setAttribute('aria-pressed', String(!on(chip)));
        run();
      });
    });
    clear.addEventListener('click', function () {
      chips.forEach(function (chip) { chip.setAttribute('aria-pressed', 'false'); });
      run();
      toggle.focus();
    });
    run();
  });
})();
