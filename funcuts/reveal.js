document.addEventListener('DOMContentLoaded', () => {
  const revealCallback = (entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('active');
        observer.unobserve(entry.target);
      }
    });
  };

  const revealObserver = new IntersectionObserver(revealCallback, {
    root: null,
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  });

  document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

  const navToggle = document.getElementById('navToggle');
  const mobileDrawer = document.getElementById('mobileDrawer');
  const drawerClose = document.getElementById('drawerClose');
  const setDrawer = open => {
    if (!mobileDrawer || !navToggle) return;
    mobileDrawer.classList.toggle('open', open);
    navToggle.setAttribute('aria-expanded', String(open));
    navToggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    document.body.classList.toggle('menu-open', open);
  };

  if (navToggle && mobileDrawer) {
    navToggle.setAttribute('aria-controls', 'mobileDrawer');
    navToggle.setAttribute('aria-expanded', 'false');
    navToggle.addEventListener('click', () => setDrawer(!mobileDrawer.classList.contains('open')));
    drawerClose?.addEventListener('click', () => setDrawer(false));
    mobileDrawer.querySelectorAll('a').forEach(link => link.addEventListener('click', () => setDrawer(false)));
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && mobileDrawer.classList.contains('open')) setDrawer(false);
    });
  }
});
