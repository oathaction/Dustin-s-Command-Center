// Loop stepper. Next step and Previous step move one step; Reset the loop goes back to the start; Play holds each step
// for its data-oa-hold (about 250 ms a word, never under 6 seconds, with reduced motion too) and becomes Pause while it
// plays. Next, Previous and Reset stop playback. The status line says each step; the current step carries
// aria-current="step". A button that cannot act keeps focus, takes aria-disabled and points to the line that says why.
(function () {
  document.querySelectorAll('[data-oa-stepper]').forEach(function (box) {
    var steps = Array.prototype.slice.call(box.querySelectorAll('.oa-stepper-step'));
    var play = box.querySelector('.oa-stepper-play');
    var word = play.querySelector('.oa-stepper-word');
    var reset = box.querySelector('.oa-stepper-reset');
    var prev = box.querySelector('.oa-stepper-prev');
    var next = box.querySelector('.oa-stepper-next');
    var status = box.querySelector('.oa-stepper-status');
    var why = box.querySelector('.oa-stepper-why');
    var i = 0, timer = null;
    // the words as a reader hears them, whatever line breaks the markup holds
    function words(el) { return el.textContent.replace(/\s+/g, ' ').trim(); }
    function off(button, unavailable) {
      if (unavailable) {
        button.setAttribute('aria-disabled', 'true');
        button.setAttribute('aria-describedby', why.id);
      } else {
        button.removeAttribute('aria-disabled');
        button.removeAttribute('aria-describedby');
      }
    }
    function show() {
      steps.forEach(function (s, k) {
        if (k === i - 1) s.setAttribute('aria-current', 'step'); else s.removeAttribute('aria-current');
        if (k >= i) s.setAttribute('data-oa-ahead', ''); else s.removeAttribute('data-oa-ahead');
      });
      var step = steps[i - 1];
      status.textContent = i ? 'Step ' + i + ' of ' + steps.length + ': ' + words(step.querySelector('.oa-stepper-line')) + ' ' +
        words(step.querySelector('.oa-stepper-more')) : status.getAttribute('data-oa-ready').replace(/\s+/g, ' ').trim();
      off(prev, !i);
      off(reset, !i);
      off(next, i === steps.length);
      why.textContent = !i ? 'Previous step and Reset the loop work once you press Next step or Play.' :
        (i === steps.length ? 'At the last step. Reset the loop to start again.' : '');
      play.toggleAttribute('data-oa-playing', !!timer);
      word.textContent = timer ? 'Pause' : (i === steps.length ? 'Play again' : 'Play');
    }
    function stop() { if (timer) { clearTimeout(timer); timer = null; } }
    function go() {
      timer = null;
      if (i < steps.length) i++;
      if (i < steps.length) timer = setTimeout(go, Number(steps[i - 1].getAttribute('data-oa-hold')) || 9000);
      show();
    }
    play.addEventListener('click', function () {
      if (timer) { stop(); show(); return; }
      if (i === steps.length) i = 0;
      go();
    });
    next.addEventListener('click', function () { if (i < steps.length) { stop(); i++; show(); } });
    prev.addEventListener('click', function () { if (i > 0) { stop(); i--; show(); } });
    reset.addEventListener('click', function () { if (i > 0) { stop(); i = 0; show(); } });
    show();
  });
})();
