export {};
// Dialog detail di beranda. Pemicu: <a href="/#kunci" data-open="kunci">; isi dari <template id="t-kunci">.
// Tautan langsung: /#kunci membuka dialog saat halaman dimuat; hash diperbarui saat dibuka/ditutup.
const sheet = document.getElementById('sheet') as HTMLDialogElement | null;
const lightbox = document.getElementById('lightbox') as HTMLDialogElement | null;
const body = document.getElementById('sheet-body');
const eyebrow = document.getElementById('sheet-eyebrow');
let lastTrigger: HTMLElement | null = null;

function open(key: string, from?: HTMLElement | null): boolean {
  const t = document.getElementById(`t-${key}`) as HTMLTemplateElement | null;
  if (!sheet || !body || !eyebrow || !t) return false;
  body.replaceChildren();
  const h = document.createElement('h2'); h.id = 'sheet-title'; h.className = 'sheet-title'; h.textContent = t.dataset.title ?? '';
  body.append(h, t.content.cloneNode(true));
  eyebrow.textContent = t.dataset.eyebrow ?? '';
  if (from && !sheet.open) lastTrigger = from;
  if (!sheet.open) sheet.showModal();
  sheet.scrollTop = 0; body.scrollTop = 0;
  history.replaceState(null, '', `#${key}`);
  return true;
}
function close() { if (sheet?.open) sheet.close(); }
sheet?.addEventListener('close', () => {
  if (location.hash && document.getElementById(`t-${location.hash.slice(1)}`)) history.replaceState(null, '', location.pathname + location.search);
  lastTrigger?.focus({ preventScroll: true }); lastTrigger = null;
});
sheet?.addEventListener('click', (e) => { if (e.target === sheet) close(); });
sheet?.querySelector('.close-dialog')?.addEventListener('click', close);

document.addEventListener('click', (e) => {
  const el = (e.target as HTMLElement).closest<HTMLElement>('[data-open]');
  if (el && !(e as MouseEvent).metaKey && !(e as MouseEvent).ctrlKey) {
    if (document.getElementById(`t-${el.dataset.open}`)) {
      e.preventDefault();
      const menu = document.getElementById('menu');
      if (menu && !menu.hidden) document.getElementById('menu-toggle')?.click();   // tutup menu lebih dulu
      open(el.dataset.open!, el);
    }
    return;
  }
  const g = (e.target as HTMLElement).closest<HTMLButtonElement>('.gallery-btn');
  if (g && lightbox) {
    const im = lightbox.querySelector('img')!; const cap = lightbox.querySelector('p')!;
    im.src = g.dataset.full!; im.alt = g.dataset.caption!; cap.textContent = g.dataset.caption!; lightbox.showModal();
  }
  const wa = (e.target as HTMLElement).closest<HTMLAnchorElement>('a[href^="https://wa.me/"]');
  if (wa) {   // sebut dialog/halaman asal di pesan WhatsApp
    try {
      const u = new URL(wa.href); const t = u.searchParams.get('text')?.replace(/\nHalaman:.*$/s, '');
      if (t) { u.searchParams.set('text', `${t}\nHalaman: ${location.pathname}${location.hash}`); wa.href = u.toString(); }
    } catch { /* biarkan tautan apa adanya */ }
  }
});
lightbox?.querySelector('.close-dialog')?.addEventListener('click', () => lightbox.close());
lightbox?.addEventListener('click', (e) => { if (e.target === lightbox) lightbox.close(); });

const fromHash = () => { const k = location.hash.slice(1); if (k && document.getElementById(`t-${k}`)) open(k); else if (!k) close(); };
addEventListener('hashchange', fromHash);
fromHash();
