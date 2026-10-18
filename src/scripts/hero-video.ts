/* Video profil di latar hero: dimuat setelah halaman selesai (foto tetap jadi poster/LCP), tanpa zoom atau gerak. */
const box = document.querySelector<HTMLElement>('[data-hero-video]');
const root = document.documentElement;

type Conn = { saveData?: boolean; effectiveType?: string };
const conn = (navigator as Navigator & { connection?: Conn }).connection;
const slow = !!conn && (conn.saveData === true || /(^|-)2g$|^3g$/.test(conn.effectiveType ?? ''));
const bot = /bot|crawl|spider|slurp|lighthouse|pagespeed|headless|prerender/i.test(navigator.userAgent);
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
let calm = false;
try { calm = localStorage.getItem('mec-calm') === '1'; } catch { /* abaikan */ }

if (box && !slow && !bot && !reduced && !calm) {
  const id = box.dataset.heroVideo!;
  let frame: HTMLIFrameElement | null = null;
  const send = (func: string, args: string | string[] = '') => frame?.contentWindow?.postMessage(JSON.stringify({ event: 'command', func, args }), '*');
  // Pastikan subtitle (termasuk otomatis) tidak tampil, meski akun penonton mengaktifkannya.
  const noCaptions = () => { send('unloadModule', ['captions']); send('unloadModule', ['cc']); };
  const start = () => {
    if (frame) return;
    frame = document.createElement('iframe');
    const q = new URLSearchParams({ autoplay: '1', mute: '1', controls: '0', loop: '1', playlist: id, playsinline: '1', rel: '0', modestbranding: '1', disablekb: '1', fs: '0', iv_load_policy: '3', cc_load_policy: '0', enablejsapi: '1' });
    frame.src = `https://www.youtube-nocookie.com/embed/${id}?${q}`;
    frame.title = 'Video company profile MEC Academy (latar)';
    frame.setAttribute('aria-hidden', 'true');
    frame.tabIndex = -1;
    frame.allow = 'autoplay; encrypted-media';
    frame.referrerPolicy = 'strict-origin-when-cross-origin';
    const show = () => { box.classList.add('playing'); noCaptions(); };
    addEventListener('message', (e) => {
      if (e.source !== frame?.contentWindow) return;
      try { const d = typeof e.data === 'string' ? JSON.parse(e.data) : e.data; if (d?.event === 'onStateChange' && d.info === 1) show(); else if (d?.info?.playerState === 1) show(); } catch { /* abaikan */ }
    });
    frame.addEventListener('load', () => { frame?.contentWindow?.postMessage(JSON.stringify({ event: 'listening', id: 1 }), '*'); noCaptions(); setTimeout(show, 4000); });
    box.appendChild(frame);
    // Jeda saat hero keluar layar atau tab disembunyikan (hemat CPU dan kuota).
    let inView = true;
    const sync = () => send(inView && !document.hidden && !root.classList.contains('calm') ? 'playVideo' : 'pauseVideo');
    new IntersectionObserver((es) => { inView = es[0].isIntersecting; sync(); }, { threshold: 0.05 }).observe(box);
    document.addEventListener('visibilitychange', sync);
    addEventListener('mec:motion', sync);
  };
  const later = () => ('requestIdleCallback' in window ? requestIdleCallback(start, { timeout: 3000 }) : setTimeout(start, 1500));
  if (document.readyState === 'complete') setTimeout(later, 800); else addEventListener('load', () => setTimeout(later, 800), { once: true });
}
export {};
