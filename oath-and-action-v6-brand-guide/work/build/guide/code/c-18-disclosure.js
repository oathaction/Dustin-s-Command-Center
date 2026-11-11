// A disclosure built on a button: each press flips aria-expanded and shows or hides the part it controls. A disclosure
// built on details and summary needs no script.
(function () {
  document.querySelectorAll('[data-oa-disclosure] .oa-disclosure-button').forEach(function (button) {
    var part = document.getElementById(button.getAttribute('aria-controls'));
    if (!part) return;
    button.addEventListener('click', function () {
      var open = button.getAttribute('aria-expanded') !== 'true';
      button.setAttribute('aria-expanded', String(open));
      part.hidden = !open;
    });
  });
})();
