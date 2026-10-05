(function () {
  var doc = document.documentElement;
  doc.classList.remove('no-js');

  // Header background on scroll + sticky mobile CTA
  var header = document.querySelector('[data-header]');
  var sticky = document.querySelector('[data-sticky-cta]');
  var hero = document.querySelector('.hero');
  var finalCta = document.querySelector('.final-cta');

  function onScroll() {
    var y = window.scrollY;
    header.classList.toggle('is-scrolled', y > 40);
    if (sticky && hero) {
      var pastHero = y > hero.offsetHeight - 100;
      var atEnd = finalCta && finalCta.getBoundingClientRect().top < window.innerHeight;
      sticky.classList.toggle('is-visible', pastHero && !atEnd);
    }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Mobile nav
  var toggle = document.querySelector('[data-nav-toggle]');
  var nav = document.querySelector('[data-nav]');
  function setNav(open) {
    document.body.classList.toggle('nav-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Lukk meny' : 'Åpne meny');
    document.body.style.overflow = open ? 'hidden' : '';
  }
  toggle.addEventListener('click', function () {
    setNav(!document.body.classList.contains('nav-open'));
  });
  nav.addEventListener('click', function (e) {
    if (e.target.closest('a')) setNav(false);
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') setNav(false);
  });

  // Reveal on scroll
  var items = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    items.forEach(function (el, i) {
      el.style.transitionDelay = (i % 4) * 70 + 'ms';
      io.observe(el);
    });
  } else {
    items.forEach(function (el) { el.classList.add('is-visible'); });
  }

  // FAQ: only one open at a time
  var faqs = document.querySelectorAll('.faq details');
  faqs.forEach(function (d) {
    d.addEventListener('toggle', function () {
      if (d.open) faqs.forEach(function (o) { if (o !== d) o.open = false; });
    });
  });

  var year = document.querySelector('[data-year]');
  if (year) year.textContent = new Date().getFullYear();
})();
