/* Mini Blog client-side enhancements (progressive enhancement, no build chain). */
(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    // Reading progress bar (article page)
    var progress = document.getElementById('reading-progress');
    if (progress) {
      window.addEventListener('scroll', function () {
        var doc = document.documentElement;
        var total = doc.scrollHeight - doc.clientHeight;
        progress.style.width = (total > 0 ? (doc.scrollTop / total) * 100 : 0) + '%';
      }, { passive: true });
    }

    // Back-to-top button (article page)
    var backToTop = document.getElementById('back-to-top');
    if (backToTop) {
      window.addEventListener('scroll', function () {
        backToTop.style.display = window.scrollY > 400 ? 'block' : 'none';
      }, { passive: true });
      backToTop.addEventListener('click', function () {
        window.scrollTo({ top: 0, behavior: 'smooth' });
      });
    }

    // Code block copy buttons
    document.querySelectorAll('.markdown-body pre').forEach(function (pre) {
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'copy-code-btn';
      btn.textContent = '复制';
      pre.appendChild(btn);
      btn.addEventListener('click', function () {
        var code = pre.innerText.replace(/\n$/, '');
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(code).then(function () {
            btn.textContent = '已复制';
            setTimeout(function () { btn.textContent = '复制'; }, 1500);
          });
        }
      });
    });
  });
})();
