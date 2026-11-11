// A sortable table: a press on a heading's button sorts the rows by that column, the first press in the order its
// heading names first and the next press the other way. aria-sort moves to that heading, and the status line says the
// order in words. Each cell to sort by carries its value in data-oa-value.
(function () {
  document.querySelectorAll('[data-oa-table]').forEach(function (box) {
    var table = box.querySelector('.oa-table-grid');
    var body = table && table.tBodies[0];
    var status = box.querySelector('.oa-table-status');
    if (!body) return;
    var heads = Array.prototype.slice.call(table.querySelectorAll('.oa-table-th'));
    table.querySelectorAll('.oa-table-sort').forEach(function (button) {
      var th = button.closest('.oa-table-th');
      var col = heads.indexOf(th);
      button.addEventListener('click', function () {
        var order = th.getAttribute('aria-sort') === 'ascending' ? 'descending' : 'ascending';
        var number = button.getAttribute('data-oa-sort') === 'number';
        var rows = Array.prototype.slice.call(body.rows);
        rows.sort(function (a, b) {
          var x = a.cells[col].getAttribute('data-oa-value') || a.cells[col].textContent;
          var y = b.cells[col].getAttribute('data-oa-value') || b.cells[col].textContent;
          var c = number ? Number(x) - Number(y) : x.localeCompare(y);
          return order === 'ascending' ? c : -c;
        });
        rows.forEach(function (r) { body.appendChild(r); });
        heads.forEach(function (h) { if (h !== th) h.removeAttribute('aria-sort'); });
        th.setAttribute('aria-sort', order);
        if (status) status.textContent = button.getAttribute('data-oa-say-' + order);
      });
    });
  });
})();
