// Block right-click
document.addEventListener('contextmenu', e => e.preventDefault());

// Block text selection
document.addEventListener('DOMContentLoaded', () => {
  document.body.style.userSelect = 'none';
});

// Block keyboard shortcuts for inspect/save/view source
document.addEventListener('keydown', function (e) {
  if (
    e.key === 'F12' || 
    (e.ctrlKey && e.shiftKey && ['I', 'J', 'C'].includes(e.key.toUpperCase())) ||
    (e.ctrlKey && ['U', 'S'].includes(e.key.toUpperCase()))
  ) {
    e.preventDefault();
  }
});
