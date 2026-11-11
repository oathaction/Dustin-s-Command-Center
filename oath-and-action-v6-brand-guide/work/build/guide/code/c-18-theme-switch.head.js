// The head script: put it in a script element of its own in the page's head, before the stylesheets. It applies a
// stored Light or Dark before the first paint; with nothing stored, tokens.css follows the device. Reading storage can
// throw, so it sits in try and catch.
(function () {
  try {
    var t = localStorage.getItem('oa-theme');
    if (t === 'light' || t === 'dark') document.documentElement.setAttribute('data-oa-theme', t);
  } catch (e) {}
})();
