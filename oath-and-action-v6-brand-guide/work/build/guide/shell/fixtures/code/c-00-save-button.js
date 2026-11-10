// Each Save button on the page toggles its pressed state and says what happened in its status line.
document.querySelectorAll('.oa-save').forEach(function (box) {
  var button = box.querySelector('.oa-save-btn');
  var note = box.querySelector('.oa-save-note');
  button.addEventListener('click', function () {
    var on = button.getAttribute('aria-pressed') !== 'true';
    button.setAttribute('aria-pressed', String(on));
    note.textContent = on ? 'Saved. Find it under Saved guides.' : 'Removed from Saved guides.';
  });
});
