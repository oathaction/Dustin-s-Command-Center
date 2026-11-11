// The head script. Copy these lines, without the slashes, into a script element of their own in the page's head,
// before the stylesheets. It applies a stored Light or Dark before the first paint; with nothing stored, tokens.css
// follows the device. A page that offers the switch also declares <meta name="color-scheme" content="light dark">.
//
//   try { var t = localStorage.getItem('oa-theme');
//     if (t === 'light' || t === 'dark') document.documentElement.setAttribute('data-oa-theme', t); } catch (e) {}
//
// The switch. Light and Dark set data-oa-theme on the target and Match my device sets "device", which follows the
// device on the page's root. Only a switch that sets the root stores the choice: Light or Dark under the key oa-theme,
// and Match my device removes the key. Storage can be refused, so each read and write sits in try and catch, and the
// switch still works for the visit.
(function () {
  var KEY = 'oa-theme';
  function stored() {
    try { var t = localStorage.getItem(KEY); return t === 'light' || t === 'dark' ? t : null; } catch (e) { return null; }
  }
  function store(value) {
    try { if (value === 'light' || value === 'dark') localStorage.setItem(KEY, value); else localStorage.removeItem(KEY); } catch (e) {}
  }
  function targetOf(box) {
    var id = box.getAttribute('data-oa-theme-for');
    // a switch that names a missing target sets nothing, never the page's root
    return id ? document.getElementById(id) : document.documentElement;
  }
  function show(box, value) {
    var input = box.querySelector('.oa-theme-input[value="' + (value === 'light' || value === 'dark' ? value : 'device') + '"]');
    if (input) input.checked = true;
  }
  var boxes = Array.prototype.slice.call(document.querySelectorAll('.oa-theme'));
  boxes.forEach(function (box) {
    var target = targetOf(box);
    if (!target) return;
    var root = target === document.documentElement;
    var now = target.getAttribute('data-oa-theme');
    if (root && now !== 'light' && now !== 'dark') {
      now = stored();
      if (now) target.setAttribute('data-oa-theme', now);
    }
    show(box, now);
    box.addEventListener('change', function (event) {
      var value = event.target.value;
      target.setAttribute('data-oa-theme', value);
      if (root) store(value);
      // every other switch that sets the same element shows the same choice
      boxes.forEach(function (other) { if (other !== box && targetOf(other) === target) show(other, value); });
    });
  });
})();
