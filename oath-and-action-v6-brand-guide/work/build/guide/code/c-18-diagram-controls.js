// Diagram controls. The drawing's parts are one Tab stop: the arrow keys, Home and End move between them, and the
// readout repeats the name of the part in view. Enter, Space or a press chooses a part (aria-pressed), mutes the
// others and opens its panel, whose name takes focus. Escape or Close the panel closes it and returns focus to the
// part. View the drawing full size opens a modal dialog; Escape or Close full size returns focus to that button.
(function () {
  document.querySelectorAll('[data-oa-diagram]').forEach(function (box) {
    var drawing = box.querySelector('.oa-diagram-drawing');
    var items = Array.prototype.slice.call(drawing.querySelectorAll('.oa-diagram-item'));
    var readout = box.querySelector('.oa-diagram-readout');
    var panel = box.querySelector('.oa-diagram-panel');
    var panelName = panel.querySelector('.oa-diagram-panel-name');
    var chosen = null;
    function nameOf(item) { return item.querySelector('.oa-diagram-name').textContent.replace(/\s+/g, ' ').trim(); }
    function detailOf(item) { return item.getAttribute('data-oa-detail').replace(/\s+/g, ' ').trim(); }
    function focusItem(item) {
      items.forEach(function (x) { x.setAttribute('tabindex', x === item ? '0' : '-1'); });
      item.focus();
    }
    function choose(item) {
      chosen = item;
      items.forEach(function (x) { x.setAttribute('aria-pressed', String(x === item)); });
      drawing.toggleAttribute('data-oa-chosen', !!item);
      if (!item) { panel.hidden = true; return; }
      panelName.textContent = nameOf(item);
      panel.querySelector('.oa-diagram-panel-text').textContent = detailOf(item);
      panel.hidden = false;
      panelName.focus();
    }
    function closePanel() {
      var back = chosen;
      choose(null);
      if (back) focusItem(back);
    }
    items.forEach(function (item, i) {
      item.addEventListener('focus', function () { readout.textContent = nameOf(item) + '. ' + detailOf(item); });
      item.addEventListener('click', function () { focusItem(item); choose(item); });
      item.addEventListener('keydown', function (e) {
        var to = null;
        if (e.key === 'ArrowRight' || e.key === 'ArrowDown') to = items[(i + 1) % items.length];
        else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') to = items[(i - 1 + items.length) % items.length];
        else if (e.key === 'Home') to = items[0];
        else if (e.key === 'End') to = items[items.length - 1];
        if (!to) return;
        e.preventDefault();
        focusItem(to);
      });
    });
    box.querySelector('.oa-diagram-close').addEventListener('click', closePanel);
    box.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && chosen) { e.preventDefault(); closePanel(); }
    });
    var open = box.querySelector('.oa-diagram-open');
    var dialog = document.getElementById(open.getAttribute('aria-controls'));
    if (dialog && dialog.showModal) {
      open.addEventListener('click', function () { dialog.showModal(); dialog.querySelector('.oa-diagram-shut').focus(); });
      dialog.querySelector('.oa-diagram-shut').addEventListener('click', function () { dialog.close(); });
      dialog.addEventListener('close', function () { open.focus(); });
    }
  });
})();
