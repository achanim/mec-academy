// Skeleton gambar, fallback gambar rusak, penanganan error global, dan banner offline.
const PLACEHOLDER = 'data:image/svg+xml;utf8,' + encodeURIComponent(
  '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300"><rect width="400" height="300" fill="#0c3438"/><path d="M130 190l40-50 30 36 24-28 46 42z" fill="#54716b"/><circle cx="160" cy="112" r="14" fill="#54716b"/></svg>');

export function toast(message: string, ms = 5000) {
  const box = document.getElementById('toast');
  if (!box) return;
  const el = document.createElement('div');
  el.className = 'toast-item';
  el.textContent = message;
  box.append(el);
  setTimeout(() => el.remove(), ms);
}

function watchImage(img: HTMLImageElement) {
  if (img.dataset.watched) return;
  img.dataset.watched = '1';
  const fail = () => {
    if (img.dataset.failed) return;
    img.dataset.failed = '1';
    img.classList.remove('is-loading');
    img.classList.add('img-failed');
    img.removeAttribute('srcset');
    img.removeAttribute('sizes');
    img.src = PLACEHOLDER;
  };
  if (img.complete) { if (img.naturalWidth === 0 && img.currentSrc) fail(); return; }
  img.classList.add('is-loading');
  img.addEventListener('load', () => img.classList.remove('is-loading'), { once: true });
  img.addEventListener('error', fail, { once: true });
}
document.querySelectorAll('img').forEach(watchImage);
// gambar yang ditambahkan belakangan
new MutationObserver((ms) => ms.forEach((m) => m.addedNodes.forEach((n) => {
  if (n instanceof HTMLImageElement) watchImage(n);
  else if (n instanceof HTMLElement) n.querySelectorAll('img').forEach(watchImage);
}))).observe(document.body, { childList: true, subtree: true });

// Error global: jangan biarkan animasi rusak merusak halaman; cukup catat.
let reported = 0;
function onError(e: ErrorEvent | PromiseRejectionEvent) {
  const detail = 'reason' in e ? e.reason : e.error ?? e.message;
  console.error('[mec] error tak tertangani:', detail);
  if (reported++ === 0) document.documentElement.classList.add('js-error'); // hook untuk CSS fallback
}
addEventListener('error', onError);
addEventListener('unhandledrejection', onError);

// Offline / online
addEventListener('offline', () => toast('Kamu sedang offline. Beberapa konten mungkin tidak termuat.', 8000));
addEventListener('online', () => toast('Koneksi kembali normal.', 3000));
