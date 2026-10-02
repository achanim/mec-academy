// UI global: menu dan mode gerak (tenang).
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
