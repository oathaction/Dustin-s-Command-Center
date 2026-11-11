// Masthead. Menu opens the phone menu as a modal dialog (showModal), which keeps Tab inside and closes on Escape;
// focus goes to the link for the part the reader is in. Close the menu, Escape or a link closes it, and focus returns
// to Menu. A row button in the menu opens and closes its list (aria-expanded).
(function () {
  document.querySelectorAll('[data-oa-masthead]').forEach(function (head) {
    var menu = head.querySelector('.oa-masthead-menu');
    var dialog = document.getElementById(menu.getAttribute('aria-controls'));
    if (!dialog || !dialog.showModal) return;
    var close = dialog.querySelector('.oa-masthead-close');
    menu.addEventListener('click', function () {
      dialog.showModal();
      menu.setAttribute('aria-expanded', 'true');
      var here = dialog.querySelector('[aria-current]') || close;
      here.focus();
    });
    close.addEventListener('click', function () { dialog.close(); });
    dialog.addEventListener('close', function () {
      menu.setAttribute('aria-expanded', 'false');
      menu.focus();
    });
    dialog.querySelectorAll('a[href]').forEach(function (a) {
      a.addEventListener('click', function () { dialog.close(); });
    });
    dialog.querySelectorAll('.oa-masthead-row').forEach(function (row) {
      var list = document.getElementById(row.getAttribute('aria-controls'));
      row.addEventListener('click', function () {
        var open = row.getAttribute('aria-expanded') !== 'true';
        row.setAttribute('aria-expanded', String(open));
        if (list) list.hidden = !open;
      });
    });
  });
})();
