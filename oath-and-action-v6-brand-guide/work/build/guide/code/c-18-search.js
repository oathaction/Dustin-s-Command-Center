// Search: as the reader types, the list keeps the items whose words hold the search, and the status line gives the
// count, with its advice in the same line when nothing matches. Clear the search, or Escape in the field, empties it
// and returns focus to the field.
(function () {
  document.querySelectorAll('[data-oa-search]').forEach(function (box) {
    var field = box.querySelector('.oa-search-input');
    var clear = box.querySelector('.oa-search-clear');
    var status = box.querySelector('.oa-search-status');
    var items = Array.prototype.slice.call(box.querySelectorAll('.oa-search-result'));
    var noun = status.getAttribute('data-oa-noun');
    function run() {
      var q = field.value.trim().toLowerCase();
      var n = 0;
      items.forEach(function (li) {
        var hit = !q || li.textContent.toLowerCase().indexOf(q) >= 0;
        li.hidden = !hit;
        if (hit) n++;
      });
      clear.hidden = !field.value;
      status.textContent = n + ' of ' + items.length + ' ' + noun + (n ? '' : '. ' + status.getAttribute('data-oa-none'));
    }
    function empty() {
      field.value = '';
      run();
      field.focus();
    }
    field.addEventListener('input', run);
    field.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && field.value) { e.preventDefault(); empty(); }
    });
    clear.addEventListener('click', empty);
    run();
  });
})();
