// Progressive enhancement: semua konten tetap terbaca tanpa JS.
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

// Reveal saat scroll
const targets = document.querySelectorAll<HTMLElement>('[data-reveal]');
if (!reduced && 'IntersectionObserver' in window) {
  document.documentElement.classList.add('motion-ok');
  const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { rootMargin: '0px 0px -10% 0px' });
  targets.forEach((t) => io.observe(t));
}

// Hero parallax ringan
const hero = document.querySelector<HTMLElement>('[data-parallax]');
if (hero && !reduced) {
  let ticking = false;
  addEventListener('scroll', () => {
    if (ticking) return; ticking = true;
    requestAnimationFrame(() => { hero.style.setProperty('--py', `${Math.min(scrollY, 900) * 0.12}px`); ticking = false; });
  }, { passive: true });
}

// Tab sistem mesin
const tabs = document.querySelectorAll<HTMLButtonElement>('[data-tab]');
const panels = document.querySelectorAll<HTMLElement>('[data-panel]');
function selectTab(i: number, focus = false) {
  tabs.forEach((t, n) => { t.setAttribute('aria-selected', String(n === i)); t.tabIndex = n === i ? 0 : -1; });
  panels.forEach((p, n) => (p.hidden = n !== i));
  if (focus) tabs[i].focus();
}
tabs.forEach((t, i) => {
  t.addEventListener('click', () => selectTab(i));
  t.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight') { e.preventDefault(); selectTab((i + 1) % tabs.length, true); }
    if (e.key === 'ArrowLeft') { e.preventDefault(); selectTab((i - 1 + tabs.length) % tabs.length, true); }
  });
});

// Rail pembelajaran
const rail = document.querySelector<HTMLElement>('[data-rail]');
if (rail) {
  const step = () => (rail.firstElementChild as HTMLElement).getBoundingClientRect().width + 24;
  document.querySelector('[data-rail-prev]')?.addEventListener('click', () => rail.scrollBy({ left: -step(), behavior: reduced ? 'auto' : 'smooth' }));
  document.querySelector('[data-rail-next]')?.addEventListener('click', () => rail.scrollBy({ left: step(), behavior: reduced ? 'auto' : 'smooth' }));
}

// Video facade — iframe baru dimuat saat diklik
document.querySelectorAll<HTMLButtonElement>('[data-video]').forEach((b) => b.addEventListener('click', () => {
  const f = document.createElement('iframe');
  f.src = `https://www.youtube-nocookie.com/embed/${b.dataset.video}?autoplay=1&rel=0`;
  f.title = 'Company Profile MEC Academy';
  f.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
  f.allowFullscreen = true;
  f.className = 'absolute inset-0 h-full w-full';
  b.replaceWith(f);
}));
