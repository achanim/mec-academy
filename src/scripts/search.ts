// Muat Pagefind dengan skeleton dan pesan fallback bila gagal.
const box = document.getElementById('search');
if (box) {
  const fail = () => {
    box.innerHTML = '<p class="search-fallback">Pencarian belum tersedia. Jelajahi artikel lewat kategori di bawah ini.</p>';
  };
  const css = document.createElement('link');
  css.rel = 'stylesheet'; css.href = '/pagefind/pagefind-ui.css';
  document.head.append(css);
  const js = document.createElement('script');
  js.src = '/pagefind/pagefind-ui.js';
  const timer = setTimeout(fail, 10000);
  js.onload = () => {
    clearTimeout(timer);
    try {
      box.replaceChildren();
      // @ts-expect-error PagefindUI dari script eksternal
      new PagefindUI({ element: '#search', showSubResults: false, translations: { placeholder: 'Cari artikel…' } });
    } catch { fail(); }
  };
  js.onerror = () => { clearTimeout(timer); fail(); };
  document.head.append(js);
}
