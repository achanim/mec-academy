// UI global: menu, mode gerak (tenang), dan layar intro.
const root = document.documentElement;
const CALM_KEY = 'mec-calm';
const store = {
  get: (k: string) => { try { return localStorage.getItem(k); } catch { return null; } },
  set: (k: string, v: string) => { try { localStorage.setItem(k, v); } catch { /* abaikan */ } },
  sget: (k: string) => { try { return sessionStorage.getItem(k); } catch { return null; } },
  sset: (k: string, v: string) => { try { sessionStorage.setItem(k, v); } catch { /* abaikan */ } },
};

/* ---------- menu ---------- */
const menu = document.getElementById('menu');
const menuBtn = document.getElementById('menu-toggle') as HTMLButtonElement | null;
function setMenu(open: boolean) {
  if (!menu || !menuBtn) return;
  menu.hidden = !open;
  root.classList.toggle('menu-open', open);
  menuBtn.setAttribute('aria-expanded', String(open));
  menuBtn.setAttribute('aria-label', open ? 'Tutup menu' : 'Buka menu');
  if (open) menu.querySelector<HTMLElement>('a')?.focus(); else menuBtn.focus({ preventScroll: true });
}
menuBtn?.addEventListener('click', () => setMenu(!!menu?.hidden));
menu?.addEventListener('click', (e) => { if ((e.target as HTMLElement).closest('a')) setMenu(false); });
addEventListener('keydown', (e) => { if (e.key === 'Escape' && menu && !menu.hidden) setMenu(false); });

/* ---------- mode gerak ---------- */
export const isCalm = () => store.get(CALM_KEY) === '1';
const motionBtn = document.getElementById('motion-toggle') as HTMLButtonElement | null;
function paintMotionBtn() {
  if (!motionBtn) return;
  const calm = isCalm();
  motionBtn.setAttribute('aria-pressed', String(calm));
  motionBtn.setAttribute('aria-label', calm ? 'Aktifkan kembali animasi' : 'Aktifkan mode tenang, kurangi animasi');
  const span = motionBtn.querySelector('em span'); if (span) span.textContent = calm ? 'tenang' : 'aktif';
  root.classList.toggle('calm', calm);
}
paintMotionBtn();
motionBtn?.addEventListener('click', () => { store.set(CALM_KEY, isCalm() ? '0' : '1'); paintMotionBtn(); dispatchEvent(new CustomEvent('mec:motion')); });

/* ---------- intro / loader ---------- */
const loader = document.getElementById('loader');
if (loader) {
  const fill = document.getElementById('load-fill')!;
  const pct = document.getElementById('load-percent')!;
  const status = document.getElementById('load-status')!;
  const enter = document.getElementById('enter-mec') as HTMLButtonElement;
  const enterLabel = document.getElementById('enter-label')!;
  const calmBtn = document.getElementById('enter-calm')!;
  const AUTO_MS = 1400;
  let loadedOnce = false, auto = 0, interacted = false;

  function progress() {
    const imgs = [...document.querySelectorAll<HTMLImageElement>('img[loading="eager"], img[fetchpriority="high"]')];
    const total = imgs.length + 1; let done = 0;
    const tick = () => {
      const p = Math.round((done / total) * 100);
      fill.style.transform = `scaleX(${p / 100})`; pct.textContent = `${p}%`;
      if (done >= total && !loadedOnce) {
        loadedOnce = true;
        status.textContent = interacted ? 'Siap dijelajahi' : 'Siap dijelajahi · masuk otomatis…';
        enterLabel.textContent = 'Mulai perjalanan';
        enter.focus({ preventScroll: true });
        // Jangan memaksa klik: lanjut sendiri kecuali pengunjung sedang berinteraksi dengan tombol
        if (!interacted) auto = window.setTimeout(close, AUTO_MS);
      }
    };
    const one = () => { done++; tick(); };
    imgs.forEach((im) => (im.complete ? one() : (im.addEventListener('load', one, { once: true }), im.addEventListener('error', one, { once: true }))));
    (document.fonts?.ready ?? Promise.resolve()).then(one, one);
    tick();
    setTimeout(() => { if (!loadedOnce) { done = total; tick(); } }, 5000);   // jangan tahan pengunjung
  }
  function close() {
    clearTimeout(auto);
    root.classList.remove('intro-pending');
    store.sset('mec-intro', '1');
    dispatchEvent(new CustomEvent('mec:enter'));
  }
  function open() {
    clearTimeout(auto); loadedOnce = false; interacted = false;
    fill.style.transform = 'scaleX(0)'; pct.textContent = '0%'; status.textContent = 'Menyiapkan pengalaman MEC'; enterLabel.textContent = 'Langsung masuk';
    root.classList.add('intro-pending'); scrollTo(0, 0); progress();
  }
  // Tahan masuk otomatis bila pengunjung mengarahkan kursor/fokus ke tombol
  [enter, calmBtn].forEach((b) => {
    b.addEventListener('pointerenter', () => { interacted = true; clearTimeout(auto); status.textContent = 'Siap dijelajahi'; });
    b.addEventListener('focus', () => { if (loadedOnce && auto) return; });
  });
  enter.addEventListener('click', close);
  calmBtn.addEventListener('click', () => { store.set(CALM_KEY, '1'); paintMotionBtn(); dispatchEvent(new CustomEvent('mec:motion')); close(); });
  addEventListener('keydown', (e) => { if (e.key === 'Escape' && root.classList.contains('intro-pending')) close(); });
  document.getElementById('replay-loader')?.addEventListener('click', open);
  if (root.classList.contains('intro-pending')) progress();
}
