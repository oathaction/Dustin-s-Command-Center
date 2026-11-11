// A live bill tracker. Each update redraws the marks from its steps' states, writes the new status words to the polite
// status line once, and ends the take-part mark when the step to take part in has passed. An update that fails shows an
// error with "Error:" in an alert and leaves the marks as they were. In this example a button plays the updates the
// list .oa-tracker-news holds; a product calls update() when its data changes.
(function () {
  var WORDS = { done: 'done', now: 'now', ahead: 'not yet', never: 'never happened', stopped: 'stopped' };
  document.querySelectorAll('[data-oa-tracker]').forEach(function (box) {
    var card = box.querySelector('.oa-tracker-card');
    var steps = Array.prototype.slice.call(card.querySelectorAll('.oa-tracker-step'));
    var status = card.querySelector('.oa-tracker-status');
    var alert = card.querySelector('.oa-tracker-alert');
    var take = card.querySelector('.oa-tracker-take');
    var check = card.querySelector('.oa-tracker-check');
    var next = card.querySelector('.oa-tracker-next');
    var why = card.querySelector('.oa-tracker-why');
    var news = Array.prototype.slice.call(card.querySelectorAll('.oa-tracker-news > li'));
    var shown = 0;
    function copy(from, to) {
      to.textContent = '';
      Array.prototype.forEach.call(from.childNodes, function (n) { to.appendChild(n.cloneNode(true)); });
    }
    function update(item) {
      if (item.hasAttribute('data-oa-error')) {
        copy(item, alert);
        alert.setAttribute('data-red', 'working');
        alert.setAttribute('data-red-job', 'error');
        return;
      }
      alert.textContent = '';
      alert.removeAttribute('data-red');
      alert.removeAttribute('data-red-job');
      item.getAttribute('data-oa-steps').split(' ').forEach(function (state, k) {
        var step = steps[k];
        step.setAttribute('data-oa-state', state);
        step.querySelector('.oa-tracker-said').textContent = ': ' + WORDS[state] + '.';
        // the take-part mark stays only on a step that is still the one the bill is at
        if (state !== 'now') ['data-oa-take-part', 'data-red', 'data-red-job'].forEach(function (a) { step.removeAttribute(a); });
      });
      if (take && !card.querySelector('[data-oa-take-part]')) take.hidden = true;
      if (check) check.hidden = true;
      copy(item, status);
    }
    next.addEventListener('click', function () {
      if (next.getAttribute('aria-disabled') === 'true' || shown >= news.length) return;
      update(news[shown]);
      shown++;
      if (shown >= news.length) {
        next.setAttribute('aria-disabled', 'true');
        why.textContent = 'That was the last update in this example.';
      }
    });
  });
})();
