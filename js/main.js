// ReaR project page — small progressive-enhancement script.
// No frameworks, no build step: this file is loaded directly via <script>.

document.addEventListener('DOMContentLoaded', function () {
  // ---- copy BibTeX to clipboard ----
  var copyBtn = document.getElementById('copy-bibtex');
  var bibtexEl = document.getElementById('bibtex-text');
  if (copyBtn && bibtexEl) {
    copyBtn.addEventListener('click', function () {
      var text = bibtexEl.textContent;
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(showCopied, function () {
          fallbackCopy(text);
        });
      } else {
        fallbackCopy(text);
      }
    });
  }

  function fallbackCopy(text) {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand('copy'); } catch (e) {}
    document.body.removeChild(ta);
    showCopied();
  }

  function showCopied() {
    copyBtn.textContent = 'Copied';
    copyBtn.classList.add('copied');
    setTimeout(function () {
      copyBtn.textContent = 'Copy';
      copyBtn.classList.remove('copied');
    }, 1800);
  }

  // ---- lightweight scroll-spy for the nav bar ----
  var sections = Array.prototype.slice.call(document.querySelectorAll('main section[id]'));
  var navLinks = Array.prototype.slice.call(document.querySelectorAll('.nav-links a'));
  if (sections.length && navLinks.length && 'IntersectionObserver' in window) {
    var byId = {};
    navLinks.forEach(function (a) {
      var id = a.getAttribute('href').replace('#', '');
      byId[id] = a;
    });
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        var link = byId[entry.target.id];
        if (!link) return;
        if (entry.isIntersecting) {
          navLinks.forEach(function (a) { a.style.color = ''; });
          link.style.color = 'var(--amber-deep)';
        }
      });
    }, { rootMargin: '-45% 0px -50% 0px', threshold: 0 });
    sections.forEach(function (s) { observer.observe(s); });
  }
});
